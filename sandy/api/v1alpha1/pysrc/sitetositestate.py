#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
SITETOSITESTATE_SCHEMA = eda.Schema(group='sandy.eda.local', version='v1alpha1', kind='SiteToSiteState')


class SiteToSiteStateSpec:
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
    def from_input(obj) -> 'SiteToSiteStateSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return SiteToSiteStateSpec(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class SiteToSiteStateStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SiteToSiteStateStatus | None':
        if obj:
            return SiteToSiteStateStatus(
            )
        return None  # pragma: no cover


class SiteToSiteState:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SiteToSiteStateSpec | None = None,
        status: SiteToSiteStateStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SITETOSITESTATE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SiteToSiteState | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SiteToSiteStateSpec.from_input(obj.get(Y_SPEC, None))
            _status = SiteToSiteStateStatus.from_input(obj.get(Y_STATUS))
            return SiteToSiteState(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SiteToSiteStateList:
    def __init__(
        self,
        items: list[SiteToSiteState],
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
    def from_input(obj) -> 'SiteToSiteStateList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SiteToSiteStateList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
