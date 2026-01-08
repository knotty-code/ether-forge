#!/usr/bin/env python3
import eda_common as eda

from plumber.api.v1alpha1.pysrc.linkapp import LINKAPP_SCHEMA
from plumber.api.v1alpha1.pysrc.linkappstate import Y_NODES, LinkAppState


class EdaStateHandler:
    def handle_cr(self, cr_obj: LinkAppState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=LINKAPP_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
