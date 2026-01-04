#!/usr/bin/env python3
import eda_common as eda
import utils.node_utils as nutils
import utils.exceptions as e

from common.constants import PLATFORM_SRL, PLATFORM_SROS
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.circuitlibrary import CircuitLibrary
from network_builder.api.v1alpha1.pysrc.circuitlibrarystate import CIRCUITLIBRARYSTATE_SCHEMA
from network_builder.intents.circuitlibrary.handlers import get_config_handler
from network_builder.intents.circuitlibrary.init import init_globals_defaults, validate

def process_cr(cr):
    """Process CircuitLibrary CR."""
    log_msg("CircuitLibrary CR:", dict=cr)

