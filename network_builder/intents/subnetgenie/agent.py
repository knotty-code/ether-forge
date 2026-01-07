#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda
import utils.node_utils as nutils

from network_builder.api.v1alpha1.pysrc.subnetgenie import SubnetGenie
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA
from network_builder.intents.subnetgenie.utils.network_utils import subnet_split

from utils.log import log_msg

class SubnetGenieAgent:
    """Orchestrates the SubnetGenie configuration flow."""

    def _error(self, msg: str):
        raise e.InvalidInput(f"[SubnetGenie '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")

    def __init__(self, cr_obj: SubnetGenie):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        """Main orchestration entry point."""
        log_msg(f"SubnetGenie orchestrator awakened for CR '{self.cr_name}'. Let the games begin.")

        self._create_subnets()

        log_msg(f"Orchestrator complete for '{self.cr_name}'. Another flawless victory.")

    def _create_subnets(self):
        """Create multiple subdivided SubnetLibrary CRs from the SubnetGenie CR."""
        log_msg("Processing SubnetGenie CR:", dict=self.cr_obj)

        supernets = subnet_split(self.cr_obj.spec.supernet, self.cr_obj.spec.subnetLength)
        log_msg(f"Generated {len(supernets)} subnets: {supernets}")

        for i, subnet_cidr in enumerate(supernets):
            child_name = f"{self.cr_name}-{i}"
            subnet_ip = subnet_cidr.split('/')[0]
            supernet = self.cr_obj.metadata.name
            subnet_length = self.cr_obj.spec.subnetLength

            log_msg(f"Creating SubnetLibrary '{child_name}' with subnet {subnet_cidr}")

            eda.update_cr(
                schema=SUBNETLIBRARY_SCHEMA,
                name=child_name,
                spec={
                    "subnets": subnet_ip,
                    "subnetLength": subnet_length,
                    "supernet": supernet,
                },
            )

        log_msg(f"Created {len(supernets)} SubnetLibrary CRs")