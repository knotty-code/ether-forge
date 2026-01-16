#!/usr/bin/env python3
import eda_common as eda

from sandy.api.v1alpha1.pysrc.edgerouter import EDGEROUTER_SCHEMA
from sandy.api.v1alpha1.pysrc.edgerouterstate import Y_NODES, EdgeRouterState


class EdaStateHandler:
    def handle_cr(self, cr_obj: EdgeRouterState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=EDGEROUTER_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
