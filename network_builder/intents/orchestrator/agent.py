#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.orchestrator import Orchestrator
from network_builder.api.v1alpha1.pysrc.subnetgeniestate import SUBNETGENIESTATE_SCHEMA
from network_builder.api.v1alpha1.pysrc.circuitlibrary import CIRCUITLIBRARY_SCHEMA
from network_builder.api.v1alpha1.pysrc.orchestrator import ORCHESTRATOR_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetlibrarystate import SUBNETLIBRARYSTATE_SCHEMA
from network_builder.intents.circuitgenie.utils.network_utils import int_to_ip

from utils.log import log_msg


class OrchestratorAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: Orchestrator):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"CircuitLibrary orchestrator started for '{self.cr_name}'")

        # If already allocated, skip
        if self.cr_obj.spec.subnets and len(self.cr_obj.spec.subnets) > 0:
            log_msg("Configuration complete (already allocated)")
            return

        # Single allocation + reservation + circuit creation
        ip_a, ip_b, subnet_name, network_addr, desired_length = self._allocate_subnet()

        # Create the CircuitLibrary entry
        # self._create_circuit(ip_a, ip_b, subnet_name, network_addr, desired_length)

        log_msg(f"CircuitLibrary orchestrator complete for '{self.cr_name}'")
        
        # self._update_subnet()
        # log_msg("Subnet Libary Usedby status updated")

    def _create_circuit(self, ip_a, ip_b, subnet_name, network_addr, desired_length):
        supernet_name = self.cr_obj.spec.supernet[0]

        eda.update_cr(
            schema=CIRCUITLIBRARY_SCHEMA,
            name=self.cr_name,
            spec={
                "supernet": [supernet_name],
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
        log_msg(f"CircuitLibrary updated with subnet '{subnet_name}' and IPs {ip_a} ↔ {ip_b}")

    def _allocate_subnet(self):
        log_msg("Starting subnet allocation from SubnetLibrary")

        if not self.cr_obj.spec.supernet or len(self.cr_obj.spec.supernet) == 0:
            self._error("supernet is required but missing")

        supernet_name = self.cr_obj.spec.supernet[0]
        desired_length = self.cr_obj.spec.subnetLength or 30
        log_msg(f"Looking for /{desired_length} subnets from pool '{supernet_name}'")

        # List SubnetLibrary CRs
        all_raw_crs = eda.list_crs(schema=SUBNETLIBRARY_SCHEMA, filter=[], ns=self.ns)

        from network_builder.api.v1alpha1.pysrc.subnetlibrary import SubnetLibrary  # Make sure this is imported

        candidates = []
        for raw_cr in all_raw_crs:
            try:
                cr_obj = SubnetLibrary.from_input(raw_cr)  # Use the correct model!
                # Adjust checks based on your actual SubnetLibrary spec
                if (getattr(cr_obj.spec, 'supernet', None) == supernet_name and
                    getattr(cr_obj.spec, 'subnetLength', None) == desired_length and
                    getattr(cr_obj.spec, 'subnets', None)):  # Just check it exists and is truthy
                    candidates.append(cr_obj)
            except Exception as exc:
                log_msg(f"Skipping invalid SubnetLibrary CR: {exc}")
                continue

        log_msg(f"Found {len(candidates)} available subnet candidates")

        if not candidates:
            self._error(f"No available subnets in SubnetLibrary for pool '{supernet_name}'")

        # Pick first
        selected_cr = candidates[0]
        subnet_name = selected_cr.metadata.name

        # Handle subnets as string (not list)
        network_addr_str = getattr(selected_cr.spec, 'subnets', None)
        if not network_addr_str:
            self._error(f"Selected SubnetLibrary '{subnet_name}' has no subnet defined")
        # In case it's "10.1.0.0/30", strip mask; otherwise keep as is
        network_addr = network_addr_str.split('/')[0]

        # Calculate IPs
        octets = list(map(int, network_addr.split('.')))
        network_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
        ip_a = int_to_ip(network_int + 1) + f"/{desired_length}"
        ip_b = int_to_ip(network_int + 2) + f"/{desired_length}"

        log_msg(f"Allocated from SubnetLibrary '{subnet_name}': {network_addr}/{desired_length}")
        log_msg(f"IPs: {ip_a} ↔ {ip_b}")

        return ip_a, ip_b, subnet_name, network_addr, desired_length

    def _update_subnet(self):
            # Keep CloneInitState update
        sub_libary_name = "p2p-subnet"
        status_test = ["test1234", "teddydog"]
        eda.update_cr(
            schema=SUBNETGENIESTATE_SCHEMA,
            name=sub_libary_name,
            spec={"usedsubnets": list(status_test)},
        )