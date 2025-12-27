#!/usr/bin/env python3
from common.constants import PLATFORM_EDA
from .eda_state import EdaStateHandler

_state_handlers = {
    PLATFORM_EDA: EdaStateHandler(),
}


def get_state_handler(platform):
    if platform == PLATFORM_EDA:
        return _state_handlers[PLATFORM_EDA]
    else:  # pragma: no cover
        raise NotImplementedError(f"Platform {platform} not supported")
