#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_SUBNET = 'subnet'
Y_SUBNETLENGTH = 'subnetLength'
Y_NODES = 'nodes'
# Package objects (GVK Schemas)
SUBNETGENIE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='SubnetGenie')


class SubnetGenieSpec:
    def __init__(
        self,
        subnet: str | None = None,
        subnetLength: int | None = None,
    ):
        self.subnet = subnet
        self.subnetLength = subnetLength

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.subnet is not None:
            _rval[Y_SUBNET] = self.subnet
        if self.subnetLength is not None:
            _rval[Y_SUBNETLENGTH] = self.subnetLength
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenieSpec | None':
        if obj:
            _subnet = obj.get(Y_SUBNET, "'10.0.0.0/29'")
            _subnetLength = obj.get(Y_SUBNETLENGTH, 30)
            return SubnetGenieSpec(
                subnet=_subnet,
                subnetLength=_subnetLength,
            )
        return None  # pragma: no cover


class SubnetGenieStatus:
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
    def from_input(obj) -> 'SubnetGenieStatus | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return SubnetGenieStatus(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class SubnetGenie:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SubnetGenieSpec | None = None,
        status: SubnetGenieStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SUBNETGENIE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenie | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SubnetGenieSpec.from_input(obj.get(Y_SPEC, None))
            _status = SubnetGenieStatus.from_input(obj.get(Y_STATUS))
            return SubnetGenie(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SubnetGenieList:
    def __init__(
        self,
        items: list[SubnetGenie],
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
    def from_input(obj) -> 'SubnetGenieList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SubnetGenieList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
