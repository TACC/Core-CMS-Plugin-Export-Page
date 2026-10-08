"""Dispatch plugin export by ``CMSPlugin.plugin_type``."""

from __future__ import annotations

from typing import Callable, Optional

Reader = Callable[[object, object, object], None]

_READERS: dict[str, Reader] = {}
_FALLBACK: Optional[Reader] = None


def register_reader(plugin_type: str, reader: Reader) -> None:
    _READERS[plugin_type] = reader


def register_fallback(reader: Reader) -> None:
    global _FALLBACK
    _FALLBACK = reader


def reader_for(plugin_type: str) -> Optional[Reader]:
    return _READERS.get(plugin_type)


def read_plugin(plugin, context) -> None:
    instance, plugin_class = plugin.get_plugin_instance()
    if instance is None:
        return
    plugin_type = plugin.plugin_type
    reader = reader_for(plugin_type)
    if reader is not None:
        reader(plugin, instance, context)
        return
    if _FALLBACK is not None:
        _FALLBACK(plugin, instance, context)
