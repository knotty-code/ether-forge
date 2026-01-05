#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from network_builder.api.v1alpha1.pysrc.orchestrator import ORCHESTRATOR_SCHEMA
from network_builder.api.v1alpha1.pysrc.portlibrary import PORTLIBRARY_SCHEMA


from utils.log import log_msg


class CircuitConfigOrchestrator:
    """Orchestrates the full CircuitGenie configuration flow.  
    Because chaos is only fun in logs, not in code."""
    def _error(self, msg: str):
            """Raise a properly contextualized tantrum. Because context matters."""
            raise e.InvalidInput(f"[CircuitGenie '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: CircuitGenie):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        if len(self.cr_obj.spec.endpoints) != 2:
            self._error("Exactly 2 endpoints required")

        endpoint_a = self.cr_obj.spec.endpoints[0]
        endpoint_b = self.cr_obj.spec.endpoints[1]

        if not self.cr_obj.spec.supernet:
            self._error("spec.supernet is required")

        supernet = self.cr_obj.spec.supernet

        # Derive nodes only if not in advanced mode (node field empty)
        node_a, real_port_a = self._derive_node_and_port_from_portlibrary(endpoint_a.port)
        node_b, real_port_b = self._derive_node_and_port_from_portlibrary(endpoint_b.port)

        # Use real_port_a / real_port_b in the CircuitLibrary
        eda.update_cr(
            schema=ORCHESTRATOR_SCHEMA,
            name=self.cr_name,
            spec={
                "endpoints": [
                    {"node": node_a, "port": real_port_a},
                    {"node": node_b, "port": real_port_b},
                ],
                "supernet": supernet,
                "subnets": [],
            },
        )

        log_msg("CircuitLibrary created — downstream allocation/config will follow")

    def _parse_ports(self):
        """Parse portA and portB from CircuitGenie spec into node + interface."""
        if not self.cr_obj.spec.portA or not self.cr_obj.spec.portB:
            self._error("Both portA and portB are required")

        # Assuming portA/portB are lists with one entry like "leaf1:ethernet-1/1"
        port_a_str = self.cr_obj.spec.portA[0]
        port_b_str = self.cr_obj.spec.portB[0]

        from network_builder.intents.circuitgenie.utils.network_utils import parse_port

        node_a, intf_a = parse_port(port_a_str)
        node_b, intf_b = parse_port(port_b_str)

        log_msg(f"Parsed ports: A={node_a}/{intf_a}, B={node_b}/{intf_b}")
        return {"A": (node_a, intf_a), "B": (node_b, intf_b)}
    
    def _derive_node_and_port_from_portlibrary(self, portlibrary_name: str):
        port_cr_raw = eda.get_cr(schema=PORTLIBRARY_SCHEMA, name=portlibrary_name, ns=self.ns)
        if not port_cr_raw:
            self._error(f"PortLibrary '{portlibrary_name}' not found")

        spec = port_cr_raw.get('spec', {})
        nodes = spec.get('nodes', [])
        if not nodes:
            self._error(f"PortLibrary '{portlibrary_name}' has no nodes")
        node = nodes[0]

        port = spec.get('port', '')
        if not port:
            self._error(f"PortLibrary '{portlibrary_name}' has no port defined in spec.port")

        log_msg(f"Derived from PortLibrary '{portlibrary_name}': node='{node}', port='{port}'")
        return node, port
    




