#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SubnetLibrary
from network_builder.api.v1alpha1.pysrc.subnetlibrarystate import SUBNETLIBRARYSTATE_SCHEMA
from network_builder.intents.subnetlibrary.handlers import get_config_handler
from network_builder.intents.subnetlibrary.init import init_globals_defaults, validate

def process_cr(cr):
    """Process SubnetLibrary CR."""
    log_msg("SubnetLibrary CR:", dict=cr)
    cr_obj = SubnetLibrary.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)
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
        schema=SUBNETLIBRARYSTATE_SCHEMA,
        name=cr_name,
        spec={
            "nodes": list(nodes.keys()),
        },
    )
