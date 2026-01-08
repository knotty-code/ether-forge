#!/usr/bin/env python3
import eda_common as eda

from plumber.api.v1alpha1.pysrc.interfaceapp import INTERFACEAPP_SCHEMA
from plumber.api.v1alpha1.pysrc.interfaceappstate import Y_NODES, InterfaceAppState


class EdaStateHandler:
    def handle_cr(self, cr_obj: InterfaceAppState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=INTERFACEAPP_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
