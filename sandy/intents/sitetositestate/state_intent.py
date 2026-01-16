#!/usr/bin/env python3
import eda_common as eda
from common.constants import PLATFORM_EDA
from utils.log import log_msg
from sandy.api.v1alpha1.pysrc.sitetositestate import SiteToSiteState
from sandy.intents.sitetositestate.state_handlers import get_state_handler
from sandy.intents.sitetositestate.init import init_globals_defaults, validate


def process_state_cr(cr):
    log_msg('SiteToSiteState CR:', dict=cr)
    cr_obj = SiteToSiteState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(cr_obj)
