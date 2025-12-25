#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.portgenie import PORTGENIE_SCHEMA
from network_builder.api.v1alpha1.pysrc.portgeniestate import Y_NODES, PortGenieState


class EdaStateHandler:
    def handle_cr(self, cr_obj: PortGenieState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=PORTGENIE_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
