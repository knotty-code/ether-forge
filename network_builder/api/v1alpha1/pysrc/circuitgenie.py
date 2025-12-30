#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_PORTA = 'portA'
Y_PORTB = 'portB'
Y_SUPERNET = 'supernet'
Y_PORTAIP = 'portAIP'
Y_PORTBIP = 'portBIP'
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
CIRCUITGENIE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='CircuitGenie')


class CircuitGenieSpec:
    def __init__(
        self,
        portA: list[str] | None = None,
        portB: list[str] | None = None,
        supernet: list[str] | None = None,
        portAIP: str | None = None,
        portBIP: str | None = None,
    ):
        self.portA = portA
        self.portB = portB
        self.supernet = supernet
        self.portAIP = portAIP
        self.portBIP = portBIP

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.portA is not None:
            _rval[Y_PORTA] = self.portA
        if self.portB is not None:
            _rval[Y_PORTB] = self.portB
        if self.supernet is not None:
            _rval[Y_SUPERNET] = self.supernet
        if self.portAIP is not None:
            _rval[Y_PORTAIP] = self.portAIP
        if self.portBIP is not None:
            _rval[Y_PORTBIP] = self.portBIP
        return _rval

    @staticmethod
    def from_input(obj) -> 'CircuitGenieSpec | None':
        if obj:
            _portA = obj.get(Y_PORTA)
            _portB = obj.get(Y_PORTB)
            _supernet = obj.get(Y_SUPERNET)
            _portAIP = obj.get(Y_PORTAIP)
            _portBIP = obj.get(Y_PORTBIP)
            return CircuitGenieSpec(
                portA=_portA,
                portB=_portB,
                supernet=_supernet,
                portAIP=_portAIP,
                portBIP=_portBIP,
            )
        return None  # pragma: no cover


class CircuitGenieStatus:
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
    def from_input(obj) -> 'CircuitGenieStatus | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return CircuitGenieStatus(
                nodes=_nodes,
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
