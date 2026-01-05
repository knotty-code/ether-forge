#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.orchestrator import Orchestrator
from network_builder.api.v1alpha1.pysrc.circuitlibrary import CIRCUITLIBRARY_SCHEMA,

from utils.log import log_msg


class OrchestratorAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: Orchestrator):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"Agent started for '{self.cr_name}'")

        # If already allocated, just configure nodes
        if self.cr_obj.spec.subnets and len(self.cr_obj.spec.subnets) > 0:
            log_msg("Configuration complete (already allocated)")
            return

        # Otherwise: allocate subnet + IPs
        # ip_a, ip_b, subnet_name = self._assign_subnet_and_ips()
        ip_a = "192.168.1.1/30"
        ip_b = "192.168.1.2/30"
        subnet_name = "test-subnet"
        supernet_name = "p2p-subnet"
        
        # Update CR with allocation
        eda.update_cr(
            schema=CIRCUITLIBRARY_SCHEMA,
            name=self.cr_name,
            spec={
                "subnets": [subnet_name],
                "supernet": [supernet_name],
                "endpoints": [
                    {
                        "node": "leaf1",
                        "port": "ethernet-1/1",
                        "ipAddress": ip_a
                    },
                    {
                        "node": "leaf2",
                        "port": "ethernet-1/1",
                        "ipAddress": ip_b
                    }
                ]
            }
        )

        log_msg("Building CR for CircuitLibrary")
