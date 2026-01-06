#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.circuitlibrary import CIRCUITLIBRARY_SCHEMA, CircuitLibrary
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA, SubnetLibrary
from network_builder.intents.circuitgenie.utils.network_utils import int_to_ip
from network_builder.intents.circuitgenie.utils.config_node import configure_node
from network_builder.intents.circuitgenie.utils.network_utils import parse_port  # if needed for validation

from utils.log import log_msg


class CircuitLibraryAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[CircuitLibrary '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: CircuitLibrary):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"CircuitLibrary orchestrator started for '{self.cr_name}'")

        # If already allocated, just configure nodes
        if self.cr_obj.spec.subnets and len(self.cr_obj.spec.subnets) > 0:
            # self._configure_nodes()  # Commented out to focus on CR creation only
            log_msg("Configuration complete (already allocated)")
            return

        # Otherwise: allocate subnet + IPs
        ip_a, ip_b, subnet_name = self._assign_subnet_and_ips()

        # Update CR with allocation
        eda.update_cr(
            schema=CIRCUITLIBRARY_SCHEMA,
            name=self.cr_name,
            spec={
                "subnets": [subnet_name],
                "endpoints": [
                    {
                        "node": self.cr_obj.spec.endpoints[0].node,
                        "port": self.cr_obj.spec.endpoints[0].port,
                        "ipAddress": ip_a
                    },
                    {
                        "node": self.cr_obj.spec.endpoints[1].node,
                        "port": self.cr_obj.spec.endpoints[1].port,
                        "ipAddress": ip_b
                    }
                ]
            }
        )

        # Configure nodes using the calculated IPs (no need for re-fetch)
        # self._configure_nodes_with_ips(ip_a, ip_b)  # Commented out to focus on CR creation only

        log_msg(f"CircuitLibrary orchestrator complete for '{self.cr_name}'")

    def _assign_subnet_and_ips(self):
        log_msg("Starting subnet allocation")

        if not self.cr_obj.spec.supernet or len(self.cr_obj.spec.supernet) == 0:
            self._error("supernet is required but missing")

        supernet = self.cr_obj.spec.supernet[0]
        log_msg(f"Looking for /30 subnets in supernet '{supernet}'")

        all_subnets_raw = eda.list_crs(schema=SUBNETLIBRARY_SCHEMA, filter=[], ns=self.ns)
        log_msg(f"Found {len(all_subnets_raw)} SubnetLibrary CRs total")

        candidates = [
            SubnetLibrary.from_input(raw_cr)
            for raw_cr in all_subnets_raw
            if (subnet := SubnetLibrary.from_input(raw_cr))
            and subnet.spec.supernet == supernet
            and subnet.spec.subnetLength == 30
        ]

        log_msg(f"Found {len(candidates)} candidate /30 subnets")

        if not candidates:
            self._error(f"No /30 subnets available in supernet '{supernet}'")

        all_circuits_raw = eda.list_crs(schema=CIRCUITLIBRARY_SCHEMA, filter=[], ns=self.ns)
        log_msg(f"Found {len(all_circuits_raw)} existing CircuitLibrary CRs")

        used_subnet_names = {
            name for raw_cr in all_circuits_raw
            for name in (CircuitLibrary.from_input(raw_cr).spec.subnets or [])
        }

        log_msg(f"Currently used subnets: {used_subnet_names}")

        available_subnet = None
        for s in candidates:
            if s.metadata.name not in used_subnet_names:
                available_subnet = s
                break

        if not available_subnet:
            self._error(f"No unused /30 subnet available in supernet '{supernet}'")

        # Allocate IPs
        base_ip = available_subnet.spec.subnet
        octets = list(map(int, base_ip.split('.')))
        ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
        ip_a = int_to_ip(ip_int + 1) + "/30"
        ip_b = int_to_ip(ip_int + 2) + "/30"

        log_msg(f"Allocated subnet '{available_subnet.metadata.name}' with IPs {ip_a} and {ip_b}")

        return ip_a, ip_b, available_subnet.metadata.name

    def _configure_nodes_with_ips(self, ip_a, ip_b):
        """Apply configuration to both endpoints using calculated IPs."""
        if len(self.cr_obj.spec.endpoints) != 2:
            self._error("Exactly 2 endpoints required for p2p circuit")

        endpoint_a = self.cr_obj.spec.endpoints[0]
        endpoint_b = self.cr_obj.spec.endpoints[1]

        import utils.node_utils as nutils

        node_cr_a = nutils.get_node(name=endpoint_a.node)
        node_cr_b = nutils.get_node(name=endpoint_b.node)

        if not node_cr_a or not node_cr_b:
            self._error(f"Node not found: {endpoint_a.node} or {endpoint_b.node}")

        log_msg(f"Configuring node {endpoint_a.node} port {endpoint_a.port} with {ip_a}")
        configure_node(self.cr_obj, endpoint_a.node, node_cr_a, endpoint_a.port, ip_a)

        log_msg(f"Configuring node {endpoint_b.node} port {endpoint_b.port} with {ip_b}")
        configure_node(self.cr_obj, endpoint_b.node, node_cr_b, endpoint_b.port, ip_b)

    def _configure_nodes(self):
        """Apply configuration to both endpoints using stored IPs."""
        if len(self.cr_obj.spec.endpoints) != 2:
            self._error("Exactly 2 endpoints required for p2p circuit")

        endpoint_a = self.cr_obj.spec.endpoints[0]
        endpoint_b = self.cr_obj.spec.endpoints[1]

        ip_a = endpoint_a.ipAddress
        ip_b = endpoint_b.ipAddress

        if not ip_a or not ip_b:
            self._error("IP addresses not allocated yet")

        import utils.node_utils as nutils

        node_cr_a = nutils.get_node(name=endpoint_a.node)
        node_cr_b = nutils.get_node(name=endpoint_b.node)

        if not node_cr_a or not node_cr_b:
            self._error(f"Node not found: {endpoint_a.node} or {endpoint_b.node}")

        log_msg(f"Configuring node {endpoint_a.node} port {endpoint_a.port} with {ip_a}")
        configure_node(self.cr_obj, endpoint_a.node, node_cr_a, endpoint_a.port, ip_a)

        log_msg(f"Configuring node {endpoint_b.node} port {endpoint_b.port} with {ip_b}")
        configure_node(self.cr_obj, endpoint_b.node, node_cr_b, endpoint_b.port, ip_b)