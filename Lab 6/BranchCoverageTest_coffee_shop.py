
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def test_invalid_orders_type():
    with pytest.raises(ValueError):
        process_order_batch("invalid", 0.1)


def test_negative_tax():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


def test_paid_and_unpaid_orders():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": False, "size": "large"}
    ]
    assert process_order_batch(orders, 0)["total"] == 3.0


def test_all_coffee_sizes_and_invalid_size():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"},
        {"paid": True, "size": "extra_large"}
    ]
    assert process_order_batch(orders, 0)["total"] == 13.5


def test_negative_customization_cost():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "syrup", "cost": -1}]
    }]
    assert process_order_batch(orders, 0)["total"] == 4.5


def test_allergen_strict_and_non_strict():
    orders = [
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": False,
            "customizations": [{"type": "allergen_alert"}]
        },
        {
            "paid": True,
            "size": "medium",
            "strict_allergy": True,
            "customizations": [{"type": "allergen_alert"}]
        }
    ]
    result = process_order_batch(orders, 0)
    assert result["total"] == 4.5


def test_syrup_below_and_above_limit():
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 1.0}]
        },
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "syrup", "cost": 2.5}]
        }
    ]
    assert process_order_batch(orders, 0)["total"] == 8.5


def test_other_customization():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "standard", "cost": 0.5}]
    }]
    assert process_order_batch(orders, 0)["total"] == 5.0


def test_member_and_non_member():
    orders = [
        {"paid": True, "size": "large", "is_member": True},
        {"paid": True, "size": "large", "is_member": False}
    ]
    assert process_order_batch(orders, 0)["total"] == 11.4


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
    assert process_order_batch(orders, 0)["status"] == "AUDIT_REJECTED"


def test_completed_order():
    orders = [{"paid": True, "size": "small"}]
    assert process_order_batch(orders, 0)["status"] == "COMPLETED"


def test_no_sale():
    assert process_order_batch([], 0.1)["status"] == "NO_SALE"


def test_no_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_temperature_stays_optimal():
    cycles = [[90.0, 94.0, 95.0], [92.0, 96.0]]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_single_overheat_then_normal():
    cycles = [[97.0, 95.0]]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_consecutive_overheating_shutdown():
    cycles = [[97.0, 98.0]]
    assert check_espresso_machine(cycles) == "SHUTDOWN"
