#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.orchestrator import Orchestrator

from utils.log import log_msg


class OrchestratorAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: Orchestrator):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"Agent started for '{self.cr_name}'")
