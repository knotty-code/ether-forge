#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from utils.log import log_msg


class SrlBaseConfigHandler:
    def handle_cr(self, cr_obj: CircuitGenie, node_cr=None, interface=None, ip_prefix=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")
        log_msg(f"interface: {interface}, ip_prefix: {ip_prefix}")

        # Safety check: skip config generation if required parameters are missing
        if interface is None or ip_prefix is None:
            log_msg("ERROR: interface or ip_prefix is None - skipping NodeConfig generation for this node")
            return

        node_name = node_cr[Y_METADATA][Y_NAME]
        self._generate_config(configs, interface, ip_prefix)
        eda.update_cr(
            schema=s.CONFIG_SCHEMA,
            name=f"circuitgenie-{cr_obj.metadata.name}-{node_name}",
            spec={"node-endpoint": node_name, "configs": configs},
        )

    def _generate_config(self, configs: list, interface: str, ip_prefix: str):
        subInterface = 0  # Assume subinterface 0 for p2p links
        self._enable_interface_admin(interface, configs)
        self._enable_interface(interface, subInterface, configs)
        self._enable_ipv4(interface, subInterface, configs)
        self._add_ip_prefix(interface, subInterface, ip_prefix, configs)

    def _enable_interface_admin(self, interface: str, configs: list):
        log_msg(f"Enabling interface {interface}")
        _config = {"admin-state": "enable"}
        path = f".interface{{.name==\"{interface}\"}}"
        configs.append({
            "path": path,
            "config": json.dumps(_config),
            "operation": "Create"  # Use Update to avoid issues if interface exists
        })

    def _enable_interface(self, interface: str, subInterface: int, configs: list):
        log_msg(f"Generating subinterface config for {interface}.{subInterface}")
        _config = {"admin-state": "enable"}
        path = f".interface{{.name==\"{interface}\"}}.subinterface{{.index==\"{subInterface}\"}}"
        configs.append({
            "path": path,
            "config": json.dumps(_config),
            "operation": "Create"
        })

    def _enable_ipv4(self, interface: str, subInterface: int, configs: list):
        log_msg(f"Enabling ipv4 on {interface}.{subInterface}")
        _config = {"admin-state": "enable"}
        path = f".interface{{.name==\"{interface}\"}}.subinterface{{.index==\"{subInterface}\"}}.ipv4"
        configs.append({
            "path": path,
            "config": json.dumps(_config),
            "operation": "Create"
        })

    def _add_ip_prefix(self, interface: str, subInterface: int, ip_prefix: str, configs: list):
        log_msg(f"Adding ip_prefix {ip_prefix} to {interface}.{subInterface}")
        _config = {}  # Optional: mark as primary address
        path = f".interface{{.name==\"{interface}\"}}.subinterface{{.index==\"{subInterface}\"}}.ipv4.address{{.ip-prefix==\"{ip_prefix}\"}}"
        configs.append({
            "path": path,
            "config": json.dumps(_config),
            "operation": "Create"
        })