#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from network_builder.api.v1alpha1.pysrc.circuitlibrary import CircuitLibrary
from utils.log import log_msg


class SrlBaseConfigHandler:
    def handle_cr(self, cr_obj: CircuitLibrary, node_cr=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")

