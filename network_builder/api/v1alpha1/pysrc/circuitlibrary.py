#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .circuitgenie import EndpointSpec
Y_ENDPOINTS = 'endpoints'
Y_SUPERNET = 'supernet'
Y_SUBNETS = 'subnets'
# Package objects (GVK Schemas)
CIRCUITLIBRARY_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='CircuitLibrary')


class CircuitLibrarySpec:
    def __init__(
        self,
        endpoints: list[EndpointSpec],
        supernet: list[str] | None = None,
        subnets: list[str] | None = None,
    ):
        self.endpoints = endpoints
        self.supernet = supernet
        self.subnets = subnets

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.endpoints is not None:
            _rval[Y_ENDPOINTS] = [x.to_input() for x in self.endpoints]
        if self.supernet is not None:
            _rval[Y_SUPERNET] = self.supernet
        if self.subnets is not None:
            _rval[Y_SUBNETS] = self.subnets
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitLibrarySpec | None':
        if obj:
            _endpoints = []
            if obj.get(Y_ENDPOINTS) is not None:
                for x in obj.get(Y_ENDPOINTS):
                    _endpoints.append(EndpointSpec.from_input(x))
            _supernet = obj.get(Y_SUPERNET)
            _subnets = obj.get(Y_SUBNETS)
            return CircuitLibrarySpec(
                endpoints=_endpoints,
                supernet=_supernet,
                subnets=_subnets,
            )
        return None  # pragma: no cover


class CircuitLibraryStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitLibraryStatus | None':
        if obj:
            return CircuitLibraryStatus(
            )
        return None  # pragma: no cover


class CircuitLibrary:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: CircuitLibrarySpec | None = None,
        status: CircuitLibraryStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = CIRCUITLIBRARY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitLibrary | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = CircuitLibrarySpec.from_input(obj.get(Y_SPEC, None))
            _status = CircuitLibraryStatus.from_input(obj.get(Y_STATUS))
            return CircuitLibrary(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class CircuitLibraryList:
    def __init__(
        self,
        items: list[CircuitLibrary],
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
    def from_input(obj) -> 'CircuitLibraryList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return CircuitLibraryList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
