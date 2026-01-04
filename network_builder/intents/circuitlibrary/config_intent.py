#!/usr/bin/env python3
from utils.log import log_msg
from network_builder.api.v1alpha1.pysrc.circuitlibrary import CircuitLibrary
from network_builder.intents.circuitlibrary.orchestrator import CircuitLibraryOrchestrator
from network_builder.intents.circuitlibrary.init import validate, init_globals_defaults


def process_cr(cr):
    """Process CircuitLibrary CR."""
    log_msg("CircuitLibrary CR:", dict=cr)
    """Entry point — now just delegates to the orchestrator."""
    log_msg("CircuitLibrary CR received. Handing off to the orchestrator...")
    cr_obj = CircuitLibrary.from_input(cr)
    if cr_obj is None:
        log_msg("Invalid CR. Rejecting with extreme prejudice.")
        return

    validate(cr_obj)
    init_globals_defaults(cr_obj)

    orchestrator = CircuitLibraryOrchestrator(cr_obj)
    orchestrator.run()