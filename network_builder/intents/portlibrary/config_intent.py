#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.portlibrary import PortLibrary
from network_builder.intents.portlibrary.agent import PortLibraryAgent
from network_builder.intents.portlibrary.init import validate, init_globals_defaults


def process_cr(cr):
    """Process PortLibrary CR."""
    log_msg("PortLibrary CR:", dict=cr)
    """Entry point — now just delegates to the orchestrator."""
    log_msg("PortLibrary CR received. Handing off to the orchestrator...")
    cr_obj = PortLibrary.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    agent = PortLibraryAgent(cr_obj)
    agent.run()