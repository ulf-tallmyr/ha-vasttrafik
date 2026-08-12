"""Icons and display names for Västtrafik transport modes."""

from __future__ import annotations

TRANSPORT_MODE_NAMES: dict[str, str] = {
    "bus": "Bus",
    "tram": "Tram",
    "train": "Train",
    "ferry": "Ferry",
    "taxi": "Taxi",
}

TRANSPORT_MODE_ICONS: dict[str, str] = {
    "bus": "mdi:bus",
    "tram": "mdi:tram",
    "train": "mdi:train",
    "ferry": "mdi:ferry",
    "taxi": "mdi:taxi",
}


def transport_mode_name(mode: object | None) -> str | None:
    """Return a user-friendly transport mode name."""
    if mode is None:
        return None

    value = str(mode)
    return TRANSPORT_MODE_NAMES.get(
        value.casefold(),
        value.replace("_", " ").title(),
    )


def transport_mode_icon(mode: object | None) -> str:
    """Return an icon matching a transport mode."""
    if mode is None:
        return "mdi:transit-connection-variant"

    return TRANSPORT_MODE_ICONS.get(
        str(mode).casefold(),
        "mdi:transit-connection-variant",
    )
