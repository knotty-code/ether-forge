#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
SUBNETGENIESTATE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='SubnetGenieState')


class SubnetGenieStateSpec:
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
    def from_input(obj) -> 'SubnetGenieStateSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return SubnetGenieStateSpec(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class SubnetGenieStateStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenieStateStatus | None':
        if obj:
            return SubnetGenieStateStatus(
            )
        return None  # pragma: no cover


class SubnetGenieState:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SubnetGenieStateSpec | None = None,
        status: SubnetGenieStateStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SUBNETGENIESTATE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenieState | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SubnetGenieStateSpec.from_input(obj.get(Y_SPEC, None))
            _status = SubnetGenieStateStatus.from_input(obj.get(Y_STATUS))
            return SubnetGenieState(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SubnetGenieStateList:
    def __init__(
        self,
        items: list[SubnetGenieState],
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
    def from_input(obj) -> 'SubnetGenieStateList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SubnetGenieStateList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
