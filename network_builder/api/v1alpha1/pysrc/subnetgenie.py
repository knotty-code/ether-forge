#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_SUPERNET = 'supernet'
Y_PURPOSE = 'purpose'
Y_SUBNETLENGTH = 'subnetLength'
Y_AVAILABLE = 'available'
# Package objects (GVK Schemas)
SUBNETGENIE_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='SubnetGenie')


class SubnetGenieSpec:
    def __init__(
        self,
        supernet: str | None = None,
        purpose: str | None = None,
        subnetLength: int | None = None,
    ):
        self.supernet = supernet
        self.purpose = purpose
        self.subnetLength = subnetLength

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.supernet is not None:
            _rval[Y_SUPERNET] = self.supernet
        if self.purpose is not None:
            _rval[Y_PURPOSE] = self.purpose
        if self.subnetLength is not None:
            _rval[Y_SUBNETLENGTH] = self.subnetLength
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenieSpec | None':
        if obj:
            _supernet = obj.get(Y_SUPERNET, "'10.0.0.0/29'")
            _purpose = obj.get(Y_PURPOSE)
            _subnetLength = obj.get(Y_SUBNETLENGTH, 30)
            return SubnetGenieSpec(
                supernet=_supernet,
                purpose=_purpose,
                subnetLength=_subnetLength,
            )
        return None  # pragma: no cover


class SubnetGenieStatus:
    def __init__(
        self,
        available: int | None = None,
    ):
        self.available = available

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.available is not None:
            _rval[Y_AVAILABLE] = self.available
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetGenieStatus | None':
        if obj:
            _available = obj.get(Y_AVAILABLE)
            return SubnetGenieStatus(
                available=_available,
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
