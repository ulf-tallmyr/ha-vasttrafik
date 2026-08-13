"""Data helpers for Västtrafik Departures."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from .coordinator import VasttrafikRouteCoordinator
from .icons import transport_mode_state


def isoformat(value: datetime | None) -> str | None:
    """Return an ISO formatted datetime when available."""
    return value.isoformat() if value is not None else None


def journey_duration_minutes(journey: Any) -> int | None:
    """Return total journey duration in whole minutes."""
    departure_time = journey.departure_time
    arrival_time = journey.arrival_time
    if departure_time is None or arrival_time is None:
        return None
    return max(
        0,
        round((arrival_time - departure_time).total_seconds() / 60),
    )


def departure_rows(
    coordinator: VasttrafikRouteCoordinator,
    minutes_until: Callable[[datetime | None], int | None],
) -> list[dict[str, Any]]:
    """Build structured departure rows for dashboards."""
    rows: list[dict[str, Any]] = []

    for journey in coordinator.data or []:
        if not journey.legs:
            continue

        leg = journey.legs[0]
        departure_time = leg.effective_departure_time
        delay = leg.delay_minutes or 0

        if leg.cancelled:
            status = "cancelled"
        elif delay > 0:
            status = "delayed"
        else:
            status = "on_time"

        rows.append(
            {
                "time": isoformat(departure_time),
                "display_time": (
                    departure_time.strftime("%H:%M")
                    if departure_time is not None
                    else None
                ),
                "planned_time": isoformat(leg.planned_departure_time),
                "estimated_time": isoformat(leg.estimated_departure_time),
                "minutes_until": minutes_until(departure_time),
                "line": leg.line_designation,
                "direction": leg.direction,
                "line_destination": leg.short_direction,
                "transport_mode": transport_mode_state(leg.transport_mode),
                "platform": leg.origin.platform if leg.origin else None,
                "delay_minutes": delay,
                "cancelled": leg.cancelled,
                "status": status,
                "number_of_changes": journey.number_of_changes,
                "travel_duration": journey_duration_minutes(journey),
            }
        )

    return rows
