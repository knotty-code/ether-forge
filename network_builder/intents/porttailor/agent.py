#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.porttailor import PortTailor

from utils.log import log_msg


class PortTailorAgent:
    log_msg("PortTailorAgent has reported for duty")
    def _error(self, msg: str):
        """Raise a properly contextualized tantrum. Because context matters."""
        raise e.InvalidInput(f"[PortTailor '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: PortTailor):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace
    def run(self):
        log_msg("PortTailor is running")
