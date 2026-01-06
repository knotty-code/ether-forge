#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.portgenie import PortGenie
from network_builder.intents.portgenie.agent import PortConfigAgent
from network_builder.intents.portgenie.init import validate, init_globals_defaults


def process_cr(cr):
    """Entry point — now just delegates to the orchestrator."""
    log_msg("PortGenie CR received. Handing off to the orchestrator...")
    cr_obj = PortGenie.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    agent = PortConfigAgent(cr_obj)
    agent.run()