#!/usr/bin/env python3

import utils.exceptions as e
import eda_common as eda

from plumber.api.v1alpha1.pysrc.linkapp import LinkApp
from plumber.intents.utils.network_utils import parse_port
from utils.log import log_msg

LINK_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TopoLink')


class LinkAppAgent:
    def _error(self, msg: str):
        raise e.InvalidInput(f"[Agent '{self.cr_name}' in '{self.ns}'] {msg}")

    def __init__(self, cr_obj: LinkApp):
        self.cr_obj = cr_obj
        self.cr_name = cr_obj.metadata.name
        self.ns = cr_obj.metadata.namespace

    def run(self):
        log_msg(f"This is Jack Burton in the Pork Chop Express, and somebody just handed me a LinkApp CR called '{self.cr_name}' in namespace '{self.ns}'. Tall order, but ol' Jack's got this.")

        self._create_link()

    def _create_link(self):
        log_msg("Alright, let's see what kinda storm we're drivin' into today.", dict=self.cr_obj)

        local = getattr(self.cr_obj.spec, "local")
        remote = getattr(self.cr_obj.spec, "remote")

        log_msg(f"Local end says it's '{local}'. Hope that's not some ancient Chinese curse in disguise.")
        log_msg(f"Remote end claims '{remote}'. We'll believe it when the link lights up.")

        try:
            local_node, local_port = parse_port(local)
            remote_node, remote_port = parse_port(remote)
        except Exception as parse_err:
            self._error(f"What in the hell? Can't even read your port scribbles. Fix it, Egg Shen. Error: {parse_err}")

        log_msg(f"Cracked the code: local node '{local_node}', port '{local_port}'.")
        log_msg(f"Remote side: node '{remote_node}', port '{remote_port}'. Not bad for a guy who just drives a truck.")

        safe_local_port = local_port.replace("/", "-")
        safe_remote_port = remote_port.replace("/", "-")

        link_name = f"{local_node}-to-{remote_node}"

        log_msg(f"Time to make these two nodes shake hands whether they like it or not. Callin' this beauty '{link_name}'.")
        log_msg("Slappin' on the official 'interSwitch' label, 'cause that's what the big bosses want. Everybody relax — I'm here.")

        eda.update_cr(
            schema=LINK_SCHEMA,
            name=link_name,
            labels={
                "eda.nokia.com/role": "interSwitch",
            },
            spec={
                "links": [
                    {
                        "local": {
                            "interface": safe_local_port,
                            "interfaceResource": local,
                            "node": local_node,
                        },
                        "remote": {
                            "interface": safe_remote_port,
                            "interfaceResource": remote,
                            "node": remote_node,
                        },
                        "type": "interSwitch",
                    }
                ]
            },
        )

        log_msg(f"Done. One shiny new TopoLink: '{link_name}'. Network's a little less broken now.")
        log_msg("You know what ol' Jack Burton always says at a time like this?")
        log_msg("It's all in the reflexes.")
        log_msg("Now where's my paycheck? This rig don't run on thanks.")