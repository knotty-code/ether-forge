#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.subnetgenie import SUBNETGENIE_SCHEMA
from network_builder.api.v1alpha1.pysrc.subnetgeniestate import Y_NODES, SubnetGenieState


class EdaStateHandler:
    def handle_cr(self, cr_obj: SubnetGenieState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=SUBNETGENIE_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
