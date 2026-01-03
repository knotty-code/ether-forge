#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_SUBNET = 'subnet'
Y_SUBNETLENGTH = 'subnetLength'
Y_SUPERNET = 'supernet'
Y_USEDBY = 'usedby'
# Package objects (GVK Schemas)
SUBNETLIBRARY_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='SubnetLibrary')


class SubnetLibrarySpec:
    def __init__(
        self,
        subnet: str | None = None,
        subnetLength: int | None = None,
        supernet: str | None = None,
        usedby: list[str] | None = None,
    ):
        self.subnet = subnet
        self.subnetLength = subnetLength
        self.supernet = supernet
        self.usedby = usedby

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.subnet is not None:
            _rval[Y_SUBNET] = self.subnet
        if self.subnetLength is not None:
            _rval[Y_SUBNETLENGTH] = self.subnetLength
        if self.supernet is not None:
            _rval[Y_SUPERNET] = self.supernet
        if self.usedby is not None:
            _rval[Y_USEDBY] = self.usedby
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetLibrarySpec | None':
        if obj:
            _subnet = obj.get(Y_SUBNET, "'10.0.0.0/29'")
            _subnetLength = obj.get(Y_SUBNETLENGTH, 30)
            _supernet = obj.get(Y_SUPERNET)
            _usedby = obj.get(Y_USEDBY)
            return SubnetLibrarySpec(
                subnet=_subnet,
                subnetLength=_subnetLength,
                supernet=_supernet,
                usedby=_usedby,
            )
        return None  # pragma: no cover


class SubnetLibraryStatus:
    def __init__(
        self,
        usedby: list[str] | None = None,
    ):
        self.usedby = usedby

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.usedby is not None:
            _rval[Y_USEDBY] = self.usedby
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetLibraryStatus | None':
        if obj:
            _usedby = obj.get(Y_USEDBY)
            return SubnetLibraryStatus(
                usedby=_usedby,
            )
        return None  # pragma: no cover


class SubnetLibrary:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SubnetLibrarySpec | None = None,
        status: SubnetLibraryStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SUBNETLIBRARY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetLibrary | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SubnetLibrarySpec.from_input(obj.get(Y_SPEC, None))
            _status = SubnetLibraryStatus.from_input(obj.get(Y_STATUS))
            return SubnetLibrary(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SubnetLibraryList:
    def __init__(
        self,
        items: list[SubnetLibrary],
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
    def from_input(obj) -> 'SubnetLibraryList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SubnetLibraryList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
