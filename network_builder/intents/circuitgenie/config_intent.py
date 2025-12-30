#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from network_builder.api.v1alpha1.pysrc.circuitgeniestate import CIRCUITGENIESTATE_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA, SubnetLibrary  # <-- Added these imports
from network_builder.intents.circuitgenie.handlers import get_config_handler
from network_builder.intents.circuitgenie.init import init_globals_defaults, validate

def process_cr(cr):
    """Process CircuitGenie CR - now also lists and prints all subnets from SubnetLibrary CRs."""
    log_msg("CircuitGenie CR:", dict=cr)
    cr_obj = CircuitGenie.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)

    # --- NEW: List all SubnetLibrary CRs and print their subnets ---
    log_msg("=== Listing all SubnetLibrary CRs ===")
    subnet_crs = eda.list_crs(schema=SUBNETLIBRARY_SCHEMA, filter=[])

    if not subnet_crs:
        log_msg("No SubnetLibrary CRs found.")
    else:
        log_msg(f"Found {len(subnet_crs)} SubnetLibrary CR(s):")
        for subnet_cr_dict in subnet_crs:
            # Parse into typed object for easier access and validation
            subnet_obj = SubnetLibrary.from_input(subnet_cr_dict)
            if subnet_obj:
                subnet_cidr = f"{subnet_obj.spec.subnet}/{subnet_obj.spec.subnetLength}"
                log_msg(
                    f"SubnetLibrary '{subnet_obj.metadata.name}' -> subnet: {subnet_cidr}"
                )
            else:
                log_msg("Failed to parse a SubnetLibrary CR:", dict=subnet_cr_dict)
    log_msg("=== End of SubnetLibrary listing ===")

    # --- Existing code below (unchanged for now) ---
    nodes = {}

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
        schema=CIRCUITGENIESTATE_SCHEMA,
        name=cr_name,
        spec={"nodes": []},
    )