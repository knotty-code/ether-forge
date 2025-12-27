#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
SUBNETLIBRARYSTATE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='SubnetLibraryState')


class SubnetLibraryStateSpec:
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
    def from_input(obj) -> 'SubnetLibraryStateSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return SubnetLibraryStateSpec(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class SubnetLibraryStateStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetLibraryStateStatus | None':
        if obj:
            return SubnetLibraryStateStatus(
            )
        return None  # pragma: no cover


class SubnetLibraryState:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SubnetLibraryStateSpec | None = None,
        status: SubnetLibraryStateStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SUBNETLIBRARYSTATE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetLibraryState | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SubnetLibraryStateSpec.from_input(obj.get(Y_SPEC, None))
            _status = SubnetLibraryStateStatus.from_input(obj.get(Y_STATUS))
            return SubnetLibraryState(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SubnetLibraryStateList:
    def __init__(
        self,
        items: list[SubnetLibraryState],
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
    def from_input(obj) -> 'SubnetLibraryStateList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SubnetLibraryStateList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
