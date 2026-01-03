#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.circuitlibrary import CIRCUITLIBRARY_SCHEMA
from network_builder.api.v1alpha1.pysrc.circuitlibrarystate import Y_NODES, CircuitLibraryState


class EdaStateHandler:
    def handle_cr(self, cr_obj: CircuitLibraryState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=CIRCUITLIBRARY_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
