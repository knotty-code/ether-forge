#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from network_builder.api.v1alpha1.pysrc.porttailor import PortTailor
from utils.log import log_msg


class SrlBaseConfigHandler:
    def handle_cr(self, cr_obj: PortTailor, node_cr=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")

        node_name = node_cr[Y_METADATA][Y_NAME]
        self._generate_config(cr_obj, configs, node_name)
        eda.update_cr(
            schema=s.CONFIG_SCHEMA,
            name=f"porttailor-{cr_obj.metadata.name}-{node_name}",
            spec={"node-endpoint": node_name, "configs": configs},
        )

    def _generate_config(self, cr_obj: PortTailor, configs: list, node_name: str):
        # Filter ports for this node (e.g., "leaf1-ethernet-1-1" -> "ethernet-1-1")
        local_ports = []
        for port in cr_obj.spec.ports or []:
            if port.startswith(node_name + "-"):
                interface = port.split('-', 1)[1]
                parts = interface.split('-')
                if len(parts) < 2:
                    continue  # Skip invalid formats
                transformed = parts[0] + '-' + '/'.join(parts[1:])
                local_ports.append(transformed)

        for local_port in local_ports:
            _config = {
                "description": cr_obj.spec.portDescription
            }
            path = f".interface{{.name==\"{local_port}\"}}"
            configs.append(
                {
                    "path": path,
                    "config": json.dumps(_config),
                    "operation": "Create",
                },
            )