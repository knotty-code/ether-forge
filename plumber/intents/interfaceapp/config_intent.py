#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from plumber.api.v1alpha1.pysrc.interfaceapp import InterfaceApp
from plumber.api.v1alpha1.pysrc.interfaceappstate import INTERFACEAPPSTATE_SCHEMA
from plumber.intents.interfaceapp.handlers import get_config_handler
from plumber.intents.interfaceapp.init import init_globals_defaults, validate
from plumber.intents.interfaceapp.agent import InterfaceAppAgent


def process_cr(cr):
    log_msg("CR:", dict=cr)
    log_msg("CR received. Handing off to the Agent...")
    cr_obj = InterfaceApp.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    Agent = InterfaceAppAgent(cr_obj)
    Agent.run()

    # eda.update_cr(
    #     schema=INTERFACEAPPSTATE_SCHEMA,
    #     name=cr_name,
    #     spec={
    #         "nodes": list(nodes.keys()),
    #     },
    # )
