#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_INTERFACEAPPSPECTYPE_LAG = 'lag'
ENUM_INTERFACEAPPSPECTYPE_INTERFACE = 'interface'
ENUM_INTERFACEAPPSPECTYPE_LOOPBACK = 'loopback'

ENUM_INTERFACEAPPSPECENCAPTYPE_NULL = 'null'
ENUM_INTERFACEAPPSPECENCAPTYPE_DOT1Q = 'dot1q'

ENUM_INTERFACEAPPSPECSPEED_1G = '1G'
ENUM_INTERFACEAPPSPECSPEED_10G = '10G'
ENUM_INTERFACEAPPSPECSPEED_25G = '25G'
ENUM_INTERFACEAPPSPECSPEED_40G = '40G'
ENUM_INTERFACEAPPSPECSPEED_50G = '50G'
ENUM_INTERFACEAPPSPECSPEED_100G = '100G'
ENUM_INTERFACEAPPSPECSPEED_400G = '400G'
Y_NODES = 'nodes'
Y_PORTSELECTOR = 'portselector'
Y_ENABLED = 'enabled'
Y_TYPE = 'type'
Y_ENCAPTYPE = 'encapType'
Y_LLDP = 'lldp'
Y_SPEED = 'speed'
# Package objects (GVK Schemas)
INTERFACEAPP_SCHEMA = eda.Schema(group='plumber.eda.local', version='v1alpha1', kind='InterfaceApp')


class InterfaceAppSpec:
    def __init__(
        self,
        nodes: list[str] | None = None,
        portselector: str | None = None,
        enabled: bool | None = None,
        type: str | None = None,
        encapType: str | None = None,
        lldp: bool | None = None,
        speed: str | None = None,
    ):
        self.nodes = nodes
        self.portselector = portselector
        self.enabled = enabled
        self.type = type
        self.encapType = encapType
        self.lldp = lldp
        self.speed = speed

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        if self.portselector is not None:
            _rval[Y_PORTSELECTOR] = self.portselector
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.encapType is not None:
            _rval[Y_ENCAPTYPE] = self.encapType
        if self.lldp is not None:
            _rval[Y_LLDP] = self.lldp
        if self.speed is not None:
            _rval[Y_SPEED] = self.speed
        return _rval

    @staticmethod
    def from_input(obj) -> 'InterfaceAppSpec | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            _portselector = obj.get(Y_PORTSELECTOR)
            _enabled = obj.get(Y_ENABLED, True)
            _type = obj.get(Y_TYPE, "interface")
            _encapType = obj.get(Y_ENCAPTYPE, "null")
            _lldp = obj.get(Y_LLDP, True)
            _speed = obj.get(Y_SPEED, "1G")
            return InterfaceAppSpec(
                nodes=_nodes,
                portselector=_portselector,
                enabled=_enabled,
                type=_type,
                encapType=_encapType,
                lldp=_lldp,
                speed=_speed,
            )
        return None  # pragma: no cover


class InterfaceAppStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'InterfaceAppStatus | None':
        if obj:
            return InterfaceAppStatus(
            )
        return None  # pragma: no cover


class InterfaceApp:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: InterfaceAppSpec | None = None,
        status: InterfaceAppStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = INTERFACEAPP_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'InterfaceApp | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = InterfaceAppSpec.from_input(obj.get(Y_SPEC, None))
            _status = InterfaceAppStatus.from_input(obj.get(Y_STATUS))
            return InterfaceApp(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class InterfaceAppList:
    def __init__(
        self,
        items: list[InterfaceApp],
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
    def from_input(obj) -> 'InterfaceAppList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return InterfaceAppList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
