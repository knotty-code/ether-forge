#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.porttailor import PortTailor
from network_builder.api.v1alpha1.pysrc.porttailorstate import PORTTAILORSTATE_SCHEMA
from network_builder.intents.porttailor.handlers import get_config_handler
from network_builder.intents.porttailor.init import init_globals_defaults, validate

def process_cr(cr):
    """Process PortTailor CR."""
    log_msg("PortTailor CR:", dict=cr)
    cr_obj = PortTailor.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    nodes = {}

    # Derive unique nodes from ports (format: "node-interface")
    derived_nodes = set()
    for port in cr_obj.spec.ports or []:
        parts = port.split('-', 1)  # Split on first '-', e.g., "leaf1-ethernet-1-1" -> ["leaf1", "ethernet-1-1"]
        if len(parts) == 2:
            derived_nodes.add(parts[0])
        else:
            raise e.InvalidInput(f"Invalid port format: {port}. Expected 'node-interface'.")

    if not derived_nodes:
        raise e.InvalidInput("No valid nodes derived from ports.")

    for node in derived_nodes:
        node_cr = nutils.get_node(name=node)
        if node_cr is None:
            msg = f"Node {node} not found"
            raise e.InvalidInput(msg)
        nodes[node] = node_cr

    for node, node_cr in nodes.items():
        if node_cr is not None:
            node_spec = node_cr["spec"]
            if node_spec.get("operatingSystem", None) is not None:
                if node_spec.get("operatingSystem") == PLATFORM_SRL:
                    srl_handler = get_config_handler(PLATFORM_SRL)
                    if srl_handler is not None:
                        srl_handler.handle_cr(cr_obj, node_cr)
                elif node_spec.get("operatingSystem") == PLATFORM_SROS:
                    sros_handler = get_config_handler(PLATFORM_SROS)
                    if sros_handler is not None:
                        sros_handler.handle_cr(cr_obj, node_cr)
                else:
                    msg = f'Operating system unsupported for {node}, os is {node_spec.get("operatingSystem", None)}'
                    raise e.InvalidInput(msg)
            else:
                msg = f'Operating system unsupported for {node}, os is {node_spec.get("operatingSystem", None)}'
                raise e.InvalidInput(msg)

    eda.update_cr(
        schema=PORTTAILORSTATE_SCHEMA,
        name=cr_name,
        spec={
            "nodes": list(nodes.keys()),
        },
    )