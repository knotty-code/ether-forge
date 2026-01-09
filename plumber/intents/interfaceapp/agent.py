#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda
import utils.node_utils as nutils

from plumber.api.v1alpha1.pysrc.interfaceapp import InterfaceApp
from plumber.intents.utils.network_utils import expand_port_ranges
from utils.log import log_msg

INTERFACELIBRARY_SCHEMA = eda.Schema(group='interfaces.eda.nokia.com', version='v1alpha1', kind='Interface')


class InterfaceAppAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: InterfaceApp):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"This is Jack Burton talkin'. Somebody just tossed me an InterfaceApp CR called '{self.cr_name}' in namespace '{self.ns}'. Big trouble? Nah, just another day haulin' freight on the Pork Chop Express.")

        self._create_ports()

    def _create_ports(self):
        log_msg("Alright, let's crack open this crate and see what kinda ports you want me to wire up.", dict=self.cr_obj)

        nodes = {}

        if not (self.cr_obj.spec.nodes and len(self.cr_obj.spec.nodes) > 0):
            self._error("No nodes in the spec? What is this, amateur hour? Gimme some nodes to work with!")

        for node in self.cr_obj.spec.nodes:
            log_msg(f"Checkin' if node '{node}' is real or just some ancient Chinese ghost story.")
            try:
                node_cr = nutils.get_node(name=node)
                if node_cr is None:
                    self._error(f"Node '{node}'? Never heard of it. It's gone, man. Like tears in rain.")
                nodes[node] = node_cr
            except Exception as err:
                self._error(f"Somethin' went sideways lookin' up node '{node}'. Blame Lo Pan. Error: {err}")

        log_msg(f"Got {len(nodes)} solid nodes locked and loaded. Everybody relax — Jack's on the case.")

        # Pull the goodies from the spec
        enabled = getattr(self.cr_obj.spec, "enabled")
        lldp = getattr(self.cr_obj.spec, "lldp")
        encap_type = getattr(self.cr_obj.spec, "encapType", None)
        speed = getattr(self.cr_obj.spec, "speed")
        lacp = 32768
        int_type = getattr(self.cr_obj.spec, "type")
        
        raw_mtu = getattr(self.cr_obj.spec, "mtu", None)
        mtu = int(raw_mtu) if raw_mtu is not None else None

        port_selector = getattr(self.cr_obj.spec, "portselector", None) or ""
        selected_ports = expand_port_ranges(port_selector)
        log_msg(f"You said ports '{port_selector}' — I expanded that to {selected_ports}. Not bad for a guy who just drives a truck.")

        if not selected_ports:
            log_msg("No port selector? Fine, I'll just take the usual suspects: 1 through 10.")
            selected_ports = [str(i) for i in range(1, 11)]

        created_count = 0

        for node_name in nodes.keys():
            log_msg(f"Rollin' into node '{node_name}'. Time to light these ports up like the Fourth of July.")
            for port_num in selected_ports:
                intf_name = f"ethernet-1-{port_num}"
                safe_intf = intf_name.replace("/", "-")
                dest_name = f"{node_name}-{safe_intf}"

                log_msg(f"Configurin' interface '{intf_name}' on '{node_name}' — callin' the new CR '{dest_name}'. It's all in the reflexes.")

                eda.update_cr(
                    schema=INTERFACELIBRARY_SCHEMA,
                    name=dest_name,
                    spec={
                        "enabled": True,
                        "encapType": encap_type,
                        "ethernet": {"speed": speed},
                        "lldp": lldp,
                        "members": [
                            {
                                "enabled": enabled,
                                "lacpPortPriority": lacp,
                                "interface": intf_name,
                                "node": node_name,
                            }
                        ],
                        "type": int_type,
                    },
                )
                created_count += 1

        log_msg(f"Done. Created {created_count} shiny new Interface CRs. Network's runnin' smoother than the Pork Chop Express on a downhill grade.")
        log_msg("You know what ol' Jack Burton always says at a time like this?")
        log_msg("It's all in the reflexes.")
        log_msg("Now somebody owe me some money for all this heavy liftin'.")