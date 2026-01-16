#!/usr/bin/env python3
import eda_common as eda
from common.constants import PLATFORM_EDA
from utils.log import log_msg
from sandy.api.v1alpha1.pysrc.edgerouterstate import EdgeRouterState
from sandy.intents.edgerouterstate.state_handlers import get_state_handler
from sandy.intents.edgerouterstate.init import init_globals_defaults, validate


def process_state_cr(cr):
    log_msg('EdgeRouterState CR:', dict=cr)
    cr_obj = EdgeRouterState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(cr_obj)
