#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from network_builder.api.v1alpha1.pysrc.circuitgenie import CircuitGenie
from utils.log import log_msg


class SrlBaseConfigHandler:
    """Handler for generating SRL configuration from CircuitGenie CRs.  
    Because nothing says 'fun' like wrestling YANG paths at 3 AM."""
    
    class Interface:
        """Fluent builder for physical SRL interfaces.  
        You know, the things that actually carry packets when everything else fails."""
        
        def __init__(self, interface_name: str, configs: list):
            self.interface_name = interface_name
            self.configs = configs
            self.base_path = f".interface{{.name==\"{interface_name}\"}}"
            self._subinterfaces = {}

        def enable(self):
            """Finally giving this poor interface permission to exist.  
            Was it just sitting there blinking sadly before? Probably."""
            log_msg(f"Oh look, we're *graciously* enabling interface {self.interface_name}. How generous of us.")
            self.configs.append({
                "path": self.base_path,
                "config": json.dumps({"admin-state": "enable"}),
                "operation": "Create"
            })
            return self

        def subinterface(self, index: int = 0):
            """Spawning a subinterface because one layer of abstraction wasn't enough."""
            if index not in self._subinterfaces:
                self._subinterfaces[index] = self.Subinterface(
                    interface_name=self.interface_name,
                    index=index,
                    configs=self.configs
                )
            return self._subinterfaces[index]

        class Subinterface:
            """Subinterfaces: where the real magic happens.  
            Or where we pretend VLANs make sense. One or the other."""
            
            def __init__(self, interface_name: str, index: int, configs: list):
                self.interface_name = interface_name
                self.index = index
                self.configs = configs
                self.path = f".interface{{.name==\"{interface_name}\"}}.subinterface{{.index==\"{index}\"}}"

            def enable(self):
                """Enabling the subinterface.  
                Because apparently the physical one being up wasn't sufficient drama."""
                log_msg(f"Subinterface {self.interface_name}.{self.index} demands attention. Fine, it's enabled. Happy now?")
                self.configs.append({
                    "path": self.path,
                    "config": json.dumps({"admin-state": "enable"}),
                    "operation": "Create"
                })
                return self

            @property
            def ipv4(self):
                """IPv4 configuration.  
                Yes, in 2026 we're still doing this. Don't @ me."""
                return self.Ipv4(self, self.configs)

            class Ipv4:
                """IPv4: the protocol that refuses to die.  
                Like that one coworker who won't retire."""
                
                def __init__(self, parent_subif, configs: list):
                    self.parent = parent_subif
                    self.configs = configs
                    self.ipv4_path = f"{parent_subif.path}.ipv4"

                def enable(self):
                    """Officially allowing IPv4.  
                    As if the internet was going to enforce that anyway."""
                    log_msg(f"Enabling IPv4 on {self.parent.interface_name}.{self.parent.index} because IPv6 is apparently too scary.")
                    self.configs.append({
                        "path": self.ipv4_path,
                        "config": json.dumps({"admin-state": "enable"}),
                        "operation": "Create"
                    })
                    return self

                def address(self, ip_prefix: str):
                    """Assigning an actual IP.  
                    The moment this subinterface finally feels special."""
                    log_msg(f"Bestowing the sacred IP {ip_prefix} upon {self.parent.interface_name}.{self.parent.index}. You're welcome.")
                    path = f"{self.ipv4_path}.address{{.ip-prefix==\"{ip_prefix}\"}}"
                    self.configs.append({
                        "path": path,
                        "config": json.dumps({}),
                        "operation": "Create"
                    })
                    return self

    # Main handler — where the real suffering begins

    def handle_cr(self, cr_obj: CircuitGenie, node_cr=None, interface=None, ip_prefix=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")
        log_msg(f"interface: {interface}, ip_prefix: {ip_prefix}")

        if interface is None or ip_prefix is None:
            log_msg("ERROR: Someone forgot to pass interface or ip_prefix. Shocking. Absolutely shocking. Skipping this node like it owes us money.")
            return

        node_name = node_cr[Y_METADATA][Y_NAME]
        self._generate_config(configs, interface, ip_prefix)
        eda.update_cr(
            schema=s.CONFIG_SCHEMA,
            name=f"circuitgenie-{cr_obj.metadata.name}-{node_name}",
            spec={"node-endpoint": node_name, "configs": configs},
        )

    def _generate_config(self, configs: list, interface: str, ip_prefix: str):
        """Generate p2p circuit config.  
        Watch in sarcastic awe as four lines of Python pretend to be networking expertise."""
        (
            SrlBaseConfigHandler.Interface(interface, configs)
            .enable()
            .subinterface(0)
                .enable()
                .ipv4.enable()
                .address(ip_prefix)
        )