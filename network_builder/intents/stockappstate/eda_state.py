#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.stockapp import STOCKAPP_SCHEMA
from network_builder.api.v1alpha1.pysrc.stockappstate import Y_NODES, StockAppState


class EdaStateHandler:
    def handle_cr(self, cr_obj: StockAppState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=STOCKAPP_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
