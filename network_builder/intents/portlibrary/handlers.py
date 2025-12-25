#!/usr/bin/env python3
from common.constants import PLATFORM_SRL, PLATFORM_SROS
from .srl import SrlBaseConfigHandler
from .sros import SrosBaseConfigHandler

_config_handlers = {
    f"{PLATFORM_SRL}": SrlBaseConfigHandler(),
    f"{PLATFORM_SROS}": SrosBaseConfigHandler(),
}


def get_config_handler(os) -> SrlBaseConfigHandler | SrosBaseConfigHandler | None:
    return _config_handlers.get(os)  # pragma: no cover
