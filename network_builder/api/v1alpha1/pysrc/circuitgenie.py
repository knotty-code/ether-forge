#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_PORT = 'port'
Y_NODE = 'node'
Y_IPADDRESS = 'ipAddress'
Y_ENDPOINTS = 'endpoints'
Y_SUPERNET = 'supernet'
Y_SUBNETS = 'subnets'
# Package objects (GVK Schemas)
CIRCUITGENIE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='CircuitGenie')


class EndpointSpec:
    def __init__(
        self,
        port: str,
        node: str,
        ipAddress: str | None = None,
    ):
        self.port = port
        self.node = node
        self.ipAddress = ipAddress

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.ipAddress is not None:
            _rval[Y_IPADDRESS] = self.ipAddress
        return _rval

    @staticmethod
    def from_input(obj) -> 'EndpointSpec | None':
        if obj:
            _port = obj.get(Y_PORT)
            _node = obj.get(Y_NODE)
            _ipAddress = obj.get(Y_IPADDRESS)
            return EndpointSpec(
                port=_port,
                node=_node,
                ipAddress=_ipAddress,
            )
        return None  # pragma: no cover


class CircuitGenieSpec:
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
    def from_input(obj) -> 'CircuitGenieSpec | None':
        if obj:
            _endpoints = []
            if obj.get(Y_ENDPOINTS) is not None:
                for x in obj.get(Y_ENDPOINTS):
                    _endpoints.append(EndpointSpec.from_input(x))
            _supernet = obj.get(Y_SUPERNET)
            _subnets = obj.get(Y_SUBNETS)
            return CircuitGenieSpec(
                endpoints=_endpoints,
                supernet=_supernet,
                subnets=_subnets,
            )
        return None  # pragma: no cover


class CircuitGenieStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitGenieStatus | None':
        if obj:
            return CircuitGenieStatus(
            )
        return None  # pragma: no cover


class CircuitGenie:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: CircuitGenieSpec | None = None,
        status: CircuitGenieStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = CIRCUITGENIE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitGenie | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = CircuitGenieSpec.from_input(obj.get(Y_SPEC, None))
            _status = CircuitGenieStatus.from_input(obj.get(Y_STATUS))
            return CircuitGenie(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class CircuitGenieList:
    def __init__(
        self,
        items: list[CircuitGenie],
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
    def from_input(obj) -> 'CircuitGenieList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return CircuitGenieList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
