#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
Y_NODESELECTOR = 'nodeSelector'
Y_LOGINBANNER = 'loginBanner'
Y_OPSTATE = 'opstate'
# Package objects (GVK Schemas)
PORTLIBRARY_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='PortLibrary')


class PortLibrarySpec:
    def __init__(
        self,
        nodes: list[str] | None = None,
        nodeSelector: list[str] | None = None,
        loginBanner: str | None = None,
    ):
        self.nodes = nodes
        self.nodeSelector = nodeSelector
        self.loginBanner = loginBanner

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        if self.nodeSelector is not None:
            _rval[Y_NODESELECTOR] = self.nodeSelector
        if self.loginBanner is not None:
            _rval[Y_LOGINBANNER] = self.loginBanner
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortLibrarySpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            _nodeSelector = obj.get(Y_NODESELECTOR)
            _loginBanner = obj.get(Y_LOGINBANNER)
            return PortLibrarySpec(
                nodes=_nodes,
                nodeSelector=_nodeSelector,
                loginBanner=_loginBanner,
            )
        return None  # pragma: no cover


class PortLibraryStatus:
    def __init__(
        self,
        nodes: list[str] | None = None,
        opstate: str | None = None,
    ):
        self.nodes = nodes
        self.opstate = opstate

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        if self.opstate is not None:
            _rval[Y_OPSTATE] = self.opstate
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortLibraryStatus | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            _opstate = obj.get(Y_OPSTATE)
            return PortLibraryStatus(
                nodes=_nodes,
                opstate=_opstate,
            )
        return None  # pragma: no cover


class PortLibrary:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: PortLibrarySpec | None = None,
        status: PortLibraryStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = PORTLIBRARY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortLibrary | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = PortLibrarySpec.from_input(obj.get(Y_SPEC, None))
            _status = PortLibraryStatus.from_input(obj.get(Y_STATUS))
            return PortLibrary(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class PortLibraryList:
    def __init__(
        self,
        items: list[PortLibrary],
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
    def from_input(obj) -> 'PortLibraryList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return PortLibraryList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
