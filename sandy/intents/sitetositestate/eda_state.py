#!/usr/bin/env python3
import eda_common as eda

from sandy.api.v1alpha1.pysrc.sitetosite import SITETOSITE_SCHEMA
from sandy.api.v1alpha1.pysrc.sitetositestate import Y_NODES, SiteToSiteState


class EdaStateHandler:
    def handle_cr(self, cr_obj: SiteToSiteState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=SITETOSITE_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
