#!/usr/bin/env python3
import eda_common as eda

from network_builder.api.v1alpha1.pysrc.orchestrator import ORCHESTRATOR_SCHEMA
from network_builder.api.v1alpha1.pysrc.orchestratorstate import Y_NODES, OrchestratorState


class EdaStateHandler:
    def handle_cr(self, cr_obj: OrchestratorState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=ORCHESTRATOR_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
