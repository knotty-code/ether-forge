#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
ORCHESTRATORSTATE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='OrchestratorState')


class OrchestratorStateSpec:
    def __init__(
        self,
        nodes: list[str] | None = None,
    ):
        self.nodes = nodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorStateSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return OrchestratorStateSpec(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class OrchestratorStateStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorStateStatus | None':
        if obj:
            return OrchestratorStateStatus(
            )
        return None  # pragma: no cover


class OrchestratorState:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: OrchestratorStateSpec | None = None,
        status: OrchestratorStateStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ORCHESTRATORSTATE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorState | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = OrchestratorStateSpec.from_input(obj.get(Y_SPEC, None))
            _status = OrchestratorStateStatus.from_input(obj.get(Y_STATUS))
            return OrchestratorState(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class OrchestratorStateList:
    def __init__(
        self,
        items: list[OrchestratorState],
        listMeta: object | None = None
    ):
        self.items = items
        self.listMeta = listMeta

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.items is not None:
            _rval[Y_ITEMS] = self.items
        if self.listMeta is not None:
            _rval[Y_METADATA] = self.listMeta
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorStateList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return OrchestratorStateList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
