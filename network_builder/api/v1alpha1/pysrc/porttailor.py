#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_PORTS = 'ports'
Y_PORTDESCRIPTION = 'portDescription'
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
PORTTAILOR_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='PortTailor')


class PortTailorSpec:
    def __init__(
        self,
        ports: list[str] | None = None,
        portDescription: str | None = None,
    ):
        self.ports = ports
        self.portDescription = portDescription

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.ports is not None:
            _rval[Y_PORTS] = self.ports
        if self.portDescription is not None:
            _rval[Y_PORTDESCRIPTION] = self.portDescription
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortTailorSpec | None':
        if obj:
            _ports = obj.get(Y_PORTS)
            _portDescription = obj.get(Y_PORTDESCRIPTION)
            return PortTailorSpec(
                ports=_ports,
                portDescription=_portDescription,
            )
        return None  # pragma: no cover


class PortTailorStatus:
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
    def from_input(obj) -> 'PortTailorStatus | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return PortTailorStatus(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class PortTailor:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: PortTailorSpec | None = None,
        status: PortTailorStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = PORTTAILOR_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'PortTailor | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = PortTailorSpec.from_input(obj.get(Y_SPEC, None))
            _status = PortTailorStatus.from_input(obj.get(Y_STATUS))
            return PortTailor(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class PortTailorList:
    def __init__(
        self,
        items: list[PortTailor],
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
    def from_input(obj) -> 'PortTailorList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return PortTailorList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
