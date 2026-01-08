#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_LOCAL = 'local'
Y_REMOTE = 'remote'
# Package objects (GVK Schemas)
LINKAPP_SCHEMA = eda.Schema(group='plumber.eda.local', version='v1alpha1', kind='LinkApp')


class LinkAppSpec:
    def __init__(
        self,
        local: str | None = None,
        remote: str | None = None,
    ):
        self.local = local
        self.remote = remote

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.local is not None:
            _rval[Y_LOCAL] = self.local
        if self.remote is not None:
            _rval[Y_REMOTE] = self.remote
        return _rval

    @staticmethod
    def from_input(obj) -> 'LinkAppSpec | None':
        if obj:
            _local = obj.get(Y_LOCAL)
            _remote = obj.get(Y_REMOTE)
            return LinkAppSpec(
                local=_local,
                remote=_remote,
            )
        return None  # pragma: no cover


class LinkAppStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'LinkAppStatus | None':
        if obj:
            return LinkAppStatus(
            )
        return None  # pragma: no cover


class LinkApp:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: LinkAppSpec | None = None,
        status: LinkAppStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = LINKAPP_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'LinkApp | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = LinkAppSpec.from_input(obj.get(Y_SPEC, None))
            _status = LinkAppStatus.from_input(obj.get(Y_STATUS))
            return LinkApp(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class LinkAppList:
    def __init__(
        self,
        items: list[LinkApp],
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
    def from_input(obj) -> 'LinkAppList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return LinkAppList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
