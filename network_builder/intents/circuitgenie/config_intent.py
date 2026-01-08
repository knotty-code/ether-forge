#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from network_builder.intents.circuitgenie.agent import CircuitGenieAgent
from network_builder.intents.circuitgenie.init import validate, init_globals_defaults


def process_cr(cr):
    """Process CircuitGenie CR."""
    log_msg("CircuitGenie CR:", dict=cr)
    """Entry point — now just delegates to the orchestrator."""
    log_msg("CircuitGenie CR received. Handing off to the orchestrator...")
    cr_obj = CircuitGenie.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    agent = CircuitGenieAgent(cr_obj)
    agent.run()