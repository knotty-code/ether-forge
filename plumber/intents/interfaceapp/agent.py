#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda
import utils.node_utils as nutils

from plumber.api.v1alpha1.pysrc.interfaceapp import InterfaceApp
from plumber.intents.utils.network_utils import expand_port_ranges
from utils.log import log_msg

INTERFACELIBRARY_SCHEMA = eda.Schema(group='interfaces.eda.nokia.com', version='v1alpha1', kind='Interface')

class InterfaceAppAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: InterfaceApp):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"InterfaceApp received CR'{self.cr_name}'")

        self._create_ports()

    def _create_ports(self):
        """Process PortGenie CR - create one PortLibrary per selected port on each node."""
        log_msg("Happy now? We're working to build CR:", dict=self.cr_obj)

        nodes = {}

        if self.cr_obj.spec.nodes is not None and len(self.cr_obj.spec.nodes) > 0:
            for node in self.cr_obj.spec.nodes:
                if node not in nodes:
                    node_cr = nutils.get_node(name=node)
                    if node_cr is None:
                        msg = f"Node {node} not found"
                        raise e.InvalidInput(msg)
                    nodes[node] = node_cr
        else:
            raise e.InvalidInput("No nodes specified in spec.nodes")

        # Get values from Interface App form
        enabled = getattr(self.cr_obj.spec, "enabled")
        lldp = getattr(self.cr_obj.spec, "lldp")
        encap_type = getattr(self.cr_obj.spec, "encapType", None)
        speed = getattr(self.cr_obj.spec, "speed")
        lacp = 32768  # Use int, not str (matches YAML example)
        int_type = getattr(self.cr_obj.spec, "type")

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
                intf_name = f"ethernet-1-{port_num}"
                safe_intf = intf_name.replace("/", "-")  # Safer for CR names
                dest_name = f"{node_name}-{safe_intf}"

                log_msg(f"Creating PortLibrary: {dest_name} for {intf_name} on {node_name}")

                eda.update_cr(
                    schema=INTERFACELIBRARY_SCHEMA,
                    name=dest_name,
                    spec={
                        "enabled": True,
                        "encapType": encap_type,
                        "ethernet": {
                            "speed": speed,
                        },
                        "lldp": lldp,
                        "members": [  # Changed to list
                            {
                                "enabled": enabled,
                                "lacpPortPriority": lacp,
                                "interface": intf_name,
                                "node": node_name,  # Changed to str (not list)
                            }
                        ],
                        "type": int_type,
                    },
                )
                created_count += 1

        log_msg(f"Created {created_count} PortLibrary CRs from selected ports")