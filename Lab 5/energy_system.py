"""Manage meter readings, tariffs, and consumption spikes.
Detect spikes in meter consumption.
"""

import json
from datetime import datetime


RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5
SPIKE_LIMIT = 500


def record_reading(
    meter_data: dict[str, float],
    meter_id: str,
    units: float,
    history: list[tuple[str, float, str]],
) -> list[tuple[str, float, str]]:
    """Record a non-negative meter reading and update its total."""
    if units < 0:
        raise ValueError("Meter units cannot be negative.")

    history.append((meter_id, units, datetime.now().isoformat()))
    meter_data[meter_id] = meter_data.get(meter_id, 0.0) + units
    return history


def compute_bill(
    meter_data: dict[str, float],
    meter_id: str,
    tier_rates: list[float],
) -> float:
    """Calculate a meter's bill using three consumption tiers."""
    units = meter_data[meter_id]

    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return (
            100 * tier_rates[0]
            + (units - 100) * tier_rates[1]
        )

    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )


def raise_rates(
    percent: float, tier_rates: list[float]
) -> list[float]:
    """Return a new list of rates increased by the given percentage."""
    multiplier = 1 + percent / 100
    return [rate * multiplier for rate in tier_rates]


def flag_spikes(meter_data: dict[str, float]) -> list[str]:
    """Return meter IDs whose recorded totals exceed the spike limit."""
    return [
        meter_id
        for meter_id, units in meter_data.items()
        if units > SPIKE_LIMIT
    ]


def load_meter_data(file: str = "meters.json") -> dict[str, float]:
    """Load meter totals from JSON, returning an empty dictionary if absent."""
    try:
        with open(file, "r", encoding="utf-8") as meter_file:
            data = json.load(meter_file)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load meter data: {error}")
        return {}

    if not isinstance(data, dict):
        print("Could not load meter data: expected a JSON object.")
        return {}

    return data


def save_meter_data(
    meter_data: dict[str, float],
    file: str = "meters.json",
) -> None:
    """Save meter totals to a JSON file."""
    with open(file, "w", encoding="utf-8") as meter_file:
        json.dump(meter_data, meter_file, indent=2)


def main() -> None:
    """Run the sample energy-meter workflow."""
    meters: dict[str, float] = {}
    history: list[tuple[str, float, str]] = []

    record_reading(meters, "M-01", 120, history)
    record_reading(meters, "M-02", 640, history)
    record_reading(meters, "M-03", 50, history)

    print("Readings stored so far:", len(history))

    base_rates = [RATE_TIER_1, RATE_TIER_2, RATE_TIER_3]
    rates = raise_rates(10, base_rates)

    print(f"Bill M-01: {compute_bill(meters, 'M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill(meters, 'M-03', rates):.2f}")
    print("Spikes:", flag_spikes(meters))

    adjustment_text = (
        input("Extra units for M-01 (number, Enter for 0): ").strip()
        or "0"
    )

    try:
        adjustment = float(adjustment_text)
        if adjustment < 0:
            raise ValueError("Extra units cannot be negative.")
    except ValueError as error:
        print(f"Invalid adjustment: {error}")
        adjustment = 0.0

    record_reading(meters, "M-01", adjustment, history)
    save_meter_data(meters)

    reloaded_meters = load_meter_data()
    if "M-01" in reloaded_meters:
        print(
            "Bill M-01 after reload: "
            f"{compute_bill(reloaded_meters, 'M-01', rates):.2f}"
        )


if __name__ == "__main__":
    main()
