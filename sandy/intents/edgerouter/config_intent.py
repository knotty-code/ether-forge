#!/usr/bin/env python3
import uuid
import logging

import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from sandy.api.v1alpha1.pysrc.edgerouter import EdgeRouter
from sandy.api.v1alpha1.pysrc.edgerouterstate import EDGEROUTERSTATE_SCHEMA
from sandy.intents.edgerouter.handlers import get_config_handler
from sandy.intents.edgerouter.init import init_globals_defaults, validate

# Set up logging (adjust level as needed)
logger = logging.getLogger(__name__)

def process_cr(cr):
    """Process EdgeRouter CR: apply config handlers + trigger post-deploy ping validation."""
    log_msg("EdgeRouter CR:", dict=cr)
    cr_obj = EdgeRouter.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)

    nodes = {}

    # Collect nodes based on selectors (if any)
    if cr_obj.spec.nodeSelector and len(cr_obj.spec.nodeSelector) > 0:
        log_msg("Filtering nodes with node selectors:", dict=cr_obj.spec.nodeSelector)
        for node_cr in nutils.list_nodes(filter=[], label_filter=cr_obj.spec.nodeSelector):
            node_name = node_cr["metadata"]["name"]
            nodes[node_name] = node_cr
            log_msg("Found node:", dict=node_name)

    # Add explicitly specified nodes
    if cr_obj.spec.nodes and len(cr_obj.spec.nodes) > 0:
        for node in cr_obj.spec.nodes:
            if node not in nodes:
                node_cr = nutils.get_node(name=node)
                if node_cr is None:
                    msg = f"Node {node} not found"
                    raise e.InvalidInput(msg)
                nodes[node] = node_cr

    # Apply platform-specific config handlers
    for node_name, node_cr in nodes.items():
        if node_cr is None:
            continue

        node_spec = node_cr["spec"]
        os_type = node_spec.get("operatingSystem")

        if os_type == PLATFORM_SRL:
            srl_handler = get_config_handler(PLATFORM_SRL)
            if srl_handler:
                srl_handler.handle_cr(cr_obj, node_cr)
        elif os_type == PLATFORM_SROS:
            sros_handler = get_config_handler(PLATFORM_SROS)
            if sros_handler:
                sros_handler.handle_cr(cr_obj, node_cr)
        else:
            msg = f'Operating system unsupported for {node_name}, os is {os_type}'
            raise e.InvalidInput(msg)

    # --- Post-deployment validation: Trigger ping workflow ---
    if not nodes:
        log_msg("No nodes found → skipping post-deploy ping validation", level="WARN")
        return

    ping_nodes = list(nodes.keys())  # Use the real collected nodes
    ping_target = "8.8.8.8"          # ← TODO: make dynamic if desired (e.g. from cr_obj.spec)

    try:
        # Load Kubernetes config (in-cluster preferred, fallback for local dev)
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        custom_api = client.CustomObjectsApi()

        workflow_name = f"post-deploy-ping-{cr_name}-{uuid.uuid4().hex[:8]}"

        body = {
            "apiVersion": "core.eda.nokia.com/v1",
            "kind": "Workflow",
            "metadata": {
                "name": workflow_name,
                "namespace": "default",  # ← adjust if your workflows live elsewhere (common: default/eda)
                # Optional: GC when EdgeRouter is deleted
                "ownerReferences": [
                    {
                        "apiVersion": cr_obj.apiVersion,
                        "kind": cr_obj.kind,
                        "name": cr_obj.metadata.name,
                        "uid": cr_obj.metadata.uid,
                        "controller": True,
                        "blockOwnerDeletion": True,
                    }
                ],
            },
            "spec": {
                "type": "oam-ping-gvk",  # Standard WorkflowDefinition name for ping (from Nokia docs)
                "input": {
                    "address": ping_target,
                    "count": 5,              # Slightly higher for better validation stats
                    "timeoutSeconds": 10,
                    "nodes": ping_nodes,
                    # Optional extras (uncomment/adjust as needed per your oam-ping-gvk schema):
                    # "pingType": "system",  # or "isl", "interface", etc.
                    # "sourceInterface": "mgmt0"
                }
            }
        }

        custom_api.create_namespaced_custom_object(
            group="core.eda.nokia.com",
            version="v1",
            namespace="default",
            plural="workflows",
            body=body
        )

        log_msg(f"Successfully triggered post-deployment ping workflow: {workflow_name} "
                f"(target: {ping_target}, nodes: {ping_nodes})", level="INFO")

    except ApiException as api_exc:
        log_msg(f"Kubernetes API error creating Workflow: {api_exc}", level="ERROR")
        # Decide: raise e.WorkflowTriggerFailed(...) or continue (non-critical validation?)
    except Exception as exc:
        log_msg(f"Unexpected error triggering ping workflow: {exc}", level="ERROR")