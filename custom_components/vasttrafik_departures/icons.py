"""Icons and display helpers for Västtrafik transport modes."""

from __future__ import annotations

TRANSPORT_MODE_ICONS: dict[str, str] = {
    "bus": "mdi:bus",
    "tram": "mdi:tram",
    "train": "mdi:train",
    "ferry": "mdi:ferry",
    "taxi": "mdi:taxi",
}


def transport_mode_icon(mode: object | None) -> str:
    """Return an icon matching a transport mode."""
    if mode is None:
        return "mdi:transit-connection-variant"
    return TRANSPORT_MODE_ICONS.get(
        str(mode).casefold(),
        "mdi:transit-connection-variant",
    )


def transport_mode_state(mode: object | None) -> str | None:
    """Return a translation-friendly transport state."""
    if mode is None:
        return None
    return str(mode).casefold().replace(" ", "_")
