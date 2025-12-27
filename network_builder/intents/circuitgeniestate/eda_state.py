#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.circuitgenie import CIRCUITGENIE_SCHEMA
from network_builder.api.v1alpha1.pysrc.circuitgeniestate import Y_NODES, CircuitGenieState


class EdaStateHandler:
    def handle_cr(self, cr_obj: CircuitGenieState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=CIRCUITGENIE_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
