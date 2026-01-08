#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda
import utils.node_utils as nutils

from network_builder.api.v1alpha1.pysrc.portgenie import PortGenie
from network_builder.api.v1alpha1.pysrc.portlibrary import PORTLIBRARY_SCHEMA
from network_builder.intents.portgenie.utils.network_utils import expand_port_ranges
from network_builder.intents.portgenie.init import init_globals_defaults, validate

from utils.log import log_msg


class PortConfigAgent:
    """Orchestrates the full CircuitGenie configuration flow.  
    Because chaos is only fun in logs, not in code."""
    def _error(self, msg: str):
            """Raise a properly contextualized tantrum. Because context matters."""
            raise e.InvalidInput(f"[CircuitGenie '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: PortGenie):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        """Main orchestration — the new process_cr."""
        log_msg(f"Port Genie orchestrator awakened for CR '{self.cr_name}'. Let the games begin.")
        
        self._create_ports()

        log_msg(f"Orchestrator complete for '{self.cr_name}'. Another flawless victory.")

    def _create_ports(self):
        """Process PortGenie CR - create one PortLibrary per selected port on each node."""
        log_msg("Happy now? We're working to build CR:", dict=self.cr_obj)  # Changed from 'cr' to 'self.cr_obj'
        # Removed duplicate 'from_input', 'validate', and 'init_globals_defaults' calls - already done in config_intent.py

        nodes = {}

        if self.cr_obj.spec.nodes is not None and len(self.cr_obj.spec.nodes) > 0:
            for node in self.cr_obj.spec.nodes:
                if node not in nodes:
                    node_cr = nutils.get_node(name=node)
                    if node_cr is None:
                        msg = f"Node {node} not found"
                        raise e.InvalidInput(msg)
                    nodes[node] = node_cr

        # Get and expand port ranges
        port_selector = getattr(self.cr_obj.spec, "portselector", None) or ""
        selected_ports = expand_port_ranges(port_selector)
        log_msg(f"Port selector '{port_selector}' expanded to: {selected_ports}")

        # Fallback: if no portSelector, use a default set
        if not selected_ports:
            log_msg("No portSelector provided - using default common ports")
            selected_ports = [str(i) for i in range(1, 11)]  # 1-10 as default

        created_count = 0

        for node_name in nodes.keys():
            for port_num in selected_ports:
                intf_name = f"ethernet-1/{port_num}"
                safe_intf = intf_name.replace("/", "-")
                dest_name = f"{node_name}-{safe_intf}"

                log_msg(f"Creating PortLibrary: {dest_name} for {intf_name} on {node_name}")

                eda.update_cr(
                    schema=PORTLIBRARY_SCHEMA,
                    name=dest_name,
                    spec={
                        "nodes": [node_name],
                        "port": intf_name,
                    },
                )
                created_count += 1

        log_msg(f"Created {created_count} PortLibrary CRs from selected ports")