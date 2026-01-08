#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.porttailor import PortTailor
from network_builder.intents.porttailor.agent import PortTailorAgent
from network_builder.intents.porttailor.init import validate, init_globals_defaults


def process_cr(cr):
    """Process PortTailor CR."""
    log_msg("PortTailor CR:", dict=cr)
    """Entry point — now just delegates to the orchestrator."""
    log_msg("PortTailor CR received. Handing off to the orchestrator...")
    cr_obj = PortTailor.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    agent = PortTailorAgent(cr_obj)
    agent.run()