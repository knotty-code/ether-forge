#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.subnetgenie import SubnetGenie
from network_builder.intents.subnetgenie.agent import SubnetGenieAgent
from network_builder.intents.subnetgenie.init import validate, init_globals_defaults


def process_cr(cr):
    """Entry point — now just delegates to the orchestrator."""
    log_msg("PortGenie CR received. Handing off to the orchestrator...")
    cr_obj = SubnetGenie.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    agent = SubnetGenieAgent(cr_obj)
    agent.run()