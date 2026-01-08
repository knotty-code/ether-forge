#!/usr/bin/env python3
import sys
import json
from utils.log import log_msg
import utils.exceptions as e
from network_builder.api.v1alpha1.pysrc.subnetlibrary import SubnetLibrary
from network_builder.api.v1alpha1.pysrc.subnetlibrarystate import SUBNETLIBRARYSTATE_SCHEMA
import eda_common as eda  # For update_cr


class SubnetLibraryAgent:
    """Orchestrates the full Subnetlibrary configuration flow.  
    Because chaos is only fun in logs, not in code."""
    def _error(self, msg: str):
            """Raise a properly contextualized tantrum. Because context matters."""
            raise e.InvalidInput(f"[Subnetlibrary '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: SubnetLibrary):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        """Main orchestration — the new process_cr."""
        log_msg(f"Orchestrator awakened for CR '{self.cr_name}'. Let the games begin.")
        
        # self._update_state()

        log_msg(f"Orchestrator complete for '{self.cr_name}'. Another flawless victory.")


