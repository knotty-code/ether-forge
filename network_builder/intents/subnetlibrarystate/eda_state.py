#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.subnetlibrary import SUBNETLIBRARY_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetlibrarystate import Y_NODES, SubnetLibraryState


class EdaStateHandler:
    def handle_cr(self, cr_obj: SubnetLibraryState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=SUBNETLIBRARY_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
