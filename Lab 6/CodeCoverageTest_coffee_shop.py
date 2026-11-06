
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def test_invalid_orders():
    with pytest.raises(ValueError):
        process_order_batch("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


def test_all_coffee_sizes():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"}
    ]
    result = process_order_batch(orders, 0)
    assert result["total"] == 13.5
    assert result["status"] == "COMPLETED"


def test_unpaid_order_is_skipped():
    orders = [{"paid": False, "size": "large"}]
    result = process_order_batch(orders, 0.1)
    assert result["status"] == "NO_SALE"


def test_invalid_size():
    orders = [{"paid": True, "size": "extra_large"}]
    result = process_order_batch(orders, 0)
    assert result["status"] == "NO_SALE"


def test_negative_customization_cost():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "syrup", "cost": -1}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 4.5


def test_allergen_without_strict_mode():
    orders = [{
        "paid": True,
        "size": "medium",
        "strict_allergy": False,
        "customizations": [{"type": "allergen_alert"}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 4.5
    assert result["status"] == "COMPLETED"


def test_allergen_with_strict_mode():
    orders = [{
        "paid": True,
        "size": "medium",
        "strict_allergy": True,
        "customizations": [{"type": "allergen_alert"}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 0
    assert result["status"] == "NO_SALE"


def test_syrup_cost_within_limit():
    orders = [{
        "paid": True,
        "size": "small",
        "customizations": [{"type": "syrup", "cost": 1.0}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 4.0


def test_syrup_cost_above_limit():
    orders = [{
        "paid": True,
        "size": "small",
        "customizations": [{"type": "syrup", "cost": 2.5}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 4.5


def test_standard_customization():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "standard", "cost": 0.5}]
    }]
    result = process_order_batch(orders, 0)
    assert result["total"] == 5.0


def test_member_discount():
    orders = [{"paid": True, "size": "large", "is_member": True}]
    result = process_order_batch(orders, 0)
    assert result["total"] == 5.4


def test_tax_calculation():
    orders = [{"paid": True, "size": "medium"}]
    result = process_order_batch(orders, 0.1)
    assert result["total"] == 4.95


def test_audit_rejected():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [
            {"type": "allergen_alert"},
            {"type": "allergen_alert"},
            {"type": "allergen_alert"},
            {"type": "allergen_alert"},
            {"type": "allergen_alert"}
        ]
    }]
    result = process_order_batch(orders, 0)
    assert result["status"] == "AUDIT_REJECTED"


def test_empty_orders():
    result = process_order_batch([], 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_empty_temperature_cycles():
    assert check_espresso_machine([]) == "NO_DATA"


def test_optimal_temperature():
    cycles = [[90.0, 94.0, 95.0], [92.0, 96.0]]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_single_overheating_reading():
    cycles = [[97.0, 95.0]]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_consecutive_overheating():
    cycles = [[97.0, 98.0]]
    assert check_espresso_machine(cycles) == "SHUTDOWN"
