#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.portlibrary import PORTLIBRARY_SCHEMA
from network_builder.api.v1alpha1.pysrc.portlibrarystate import Y_NODES, PortLibraryState


class EdaStateHandler:
    def handle_cr(self, cr_obj: PortLibraryState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=PORTLIBRARY_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
