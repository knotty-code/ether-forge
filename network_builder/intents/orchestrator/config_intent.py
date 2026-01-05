#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.orchestrator import Orchestrator
from network_builder.intents.orchestrator.agent import OrchestratorAgent
from network_builder.intents.orchestrator.init import validate, init_globals_defaults


def process_cr(cr):
    log_msg("CR:", dict=cr)
    log_msg("CR received. Handing off to the Agent...")
    cr_obj = Orchestrator.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    Agent = OrchestratorAgent(cr_obj)
    Agent.run()