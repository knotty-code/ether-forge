#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODES = 'nodes'
Y_PORTSELECTOR = 'portselector'
Y_LOGINBANNER = 'loginBanner'
# Package objects (GVK Schemas)
PORTGENIE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='PortGenie')


class PortGenieSpec:
    def __init__(
        self,
        nodes: list[str] | None = None,
        portselector: str | None = None,
        loginBanner: str | None = None,
    ):
        self.nodes = nodes
        self.portselector = portselector
        self.loginBanner = loginBanner

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        if self.portselector is not None:
            _rval[Y_PORTSELECTOR] = self.portselector
        if self.loginBanner is not None:
            _rval[Y_LOGINBANNER] = self.loginBanner
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortGenieSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            _portselector = obj.get(Y_PORTSELECTOR)
            _loginBanner = obj.get(Y_LOGINBANNER)
            return PortGenieSpec(
                nodes=_nodes,
                portselector=_portselector,
                loginBanner=_loginBanner,
            )
        return None  # pragma: no cover


class PortGenieStatus:
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
    def from_input(obj) -> 'PortGenieStatus | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return PortGenieStatus(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class PortGenie:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: PortGenieSpec | None = None,
        status: PortGenieStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = PORTGENIE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortGenie | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = PortGenieSpec.from_input(obj.get(Y_SPEC, None))
            _status = PortGenieStatus.from_input(obj.get(Y_STATUS))
            return PortGenie(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class PortGenieList:
    def __init__(
        self,
        items: list[PortGenie],
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
    def from_input(obj) -> 'PortGenieList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return PortGenieList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
