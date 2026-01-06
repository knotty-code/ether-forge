#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.portlibrary import PortLibrary

from utils.log import log_msg


class PortLibraryAgent:
    log_msg("PortLibary Agent has reported for duty")
    def _error(self, msg: str):
        """Raise a properly contextualized tantrum. Because context matters."""
        raise e.InvalidInput(f"[PortLibary '{self.cr_name}' in '{self.ns}'] {msg} Seriously.")
    def __init__(self, cr_obj: PortLibrary):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace
