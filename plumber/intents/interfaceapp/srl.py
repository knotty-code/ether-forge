#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from plumber.api.v1alpha1.pysrc.interfaceapp import InterfaceApp
from utils.log import log_msg


class SrlBaseConfigHandler:
    def handle_cr(self, cr_obj: InterfaceApp, node_cr=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")

        node_name = node_cr[Y_METADATA][Y_NAME]
        self._generate_config(cr_obj, configs)
        eda.update_cr(
            schema=s.CONFIG_SCHEMA,
            name=f"banner-{cr_obj.metadata.name}-{node_name}",
            spec={"node-endpoint": node_name, "configs": configs},
        )

    def _generate_config(self, cr_obj: InterfaceApp, configs: list):
        _config = {}
        if cr_obj.spec.loginBanner is not None:
            _config["login-banner"] = cr_obj.spec.loginBanner

        configs.append(
            {
                "path": ".system.banner",
                "config": json.dumps(_config),
                "operation": "Create",
            },
        )
