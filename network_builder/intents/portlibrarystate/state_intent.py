#!/usr/bin/env python3
import eda_common as eda
from common.constants import PLATFORM_EDA
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.portlibrarystate import PortLibraryState
from network_builder.intents.portlibrarystate.state_handlers import get_state_handler
from network_builder.intents.portlibrarystate.init import init_globals_defaults, validate


def process_state_cr(cr):
    log_msg('PortLibraryState CR:', dict=cr)
    cr_obj = PortLibraryState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(cr_obj)
