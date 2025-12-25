#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.porttailor import PORTTAILOR_SCHEMA
from network_builder.api.v1alpha1.pysrc.porttailorstate import Y_NODES, PortTailorState


class EdaStateHandler:
    def handle_cr(self, cr_obj: PortTailorState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=PORTTAILOR_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
