#!/usr/bin/env python3
from network_builder.api.v1alpha1.pysrc.portlibrarystate import PortLibraryState


class EdaStateHandler:
    def handle_cr(self, cr_obj: PortLibraryState):
        # Intentionally do nothing — real logic is in state_intent.py
        pass