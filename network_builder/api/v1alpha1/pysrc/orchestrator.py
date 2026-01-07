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
Y_SOURCE = 'source'
Y_SUBNETLENGTH = 'subnetLength'
Y_PURPOSE = 'purpose'
Y_USEDBY = 'usedby'
# Package objects (GVK Schemas)
ORCHESTRATOR_SCHEMA = eda.Schema(group='network-builder.eda.local', version='v1alpha1', kind='Orchestrator')


class OrchestratorSpec:
    def __init__(
        self,
        endpoints: list[EndpointSpec],
        supernet: list[str] | None = None,
        subnets: list[str] | None = None,
        source: str | None = None,
        subnetLength: int | None = None,
        purpose: str | None = None,
        usedby: str | None = None,
    ):
        self.endpoints = endpoints
        self.supernet = supernet
        self.subnets = subnets
        self.source = source
        self.subnetLength = subnetLength
        self.purpose = purpose
        self.usedby = usedby

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.endpoints is not None:
            _rval[Y_ENDPOINTS] = [x.to_input() for x in self.endpoints]
        if self.supernet is not None:
            _rval[Y_SUPERNET] = self.supernet
        if self.subnets is not None:
            _rval[Y_SUBNETS] = self.subnets
        if self.source is not None:
            _rval[Y_SOURCE] = self.source
        if self.subnetLength is not None:
            _rval[Y_SUBNETLENGTH] = self.subnetLength
        if self.purpose is not None:
            _rval[Y_PURPOSE] = self.purpose
        if self.usedby is not None:
            _rval[Y_USEDBY] = self.usedby
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorSpec | None':
        if obj:
            _endpoints = []
            if obj.get(Y_ENDPOINTS) is not None:
                for x in obj.get(Y_ENDPOINTS):
                    _endpoints.append(EndpointSpec.from_input(x))
            _supernet = obj.get(Y_SUPERNET)
            _subnets = obj.get(Y_SUBNETS)
            _source = obj.get(Y_SOURCE)
            _subnetLength = obj.get(Y_SUBNETLENGTH)
            _purpose = obj.get(Y_PURPOSE)
            _usedby = obj.get(Y_USEDBY)
            return OrchestratorSpec(
                endpoints=_endpoints,
                supernet=_supernet,
                subnets=_subnets,
                source=_source,
                subnetLength=_subnetLength,
                purpose=_purpose,
                usedby=_usedby,
            )
        return None  # pragma: no cover


class OrchestratorStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'OrchestratorStatus | None':
        if obj:
            return OrchestratorStatus(
            )
        return None  # pragma: no cover


class Orchestrator:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: OrchestratorSpec | None = None,
        status: OrchestratorStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ORCHESTRATOR_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Orchestrator | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = OrchestratorSpec.from_input(obj.get(Y_SPEC, None))
            _status = OrchestratorStatus.from_input(obj.get(Y_STATUS))
            return Orchestrator(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class OrchestratorList:
    def __init__(
        self,
        items: list[Orchestrator],
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
    def from_input(obj) -> 'OrchestratorList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return OrchestratorList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
