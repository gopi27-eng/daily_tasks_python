import pytest
from hypothesis import given, strategies as st

# --- 1. THE BUSINESS LOGIC ---
def calculate_fee(weight_kg: float, distance_km: float) -> float:
    """Calculates cargo fee. Cannot accept negative values."""
    if weight_kg < 0 or distance_km < 0:
        raise ValueError("Weight and distance cannot be negative.")
    
    base_fee = 10.0
    return base_fee + (weight_kg * 2.0) + (distance_km * 0.5)


# --- 2. STANDARD PYTEST (Example-Based) ---
def test_calculate_fee_standard():
    # Example 1: Known good values
    assert calculate_fee(10, 100) == 80.0  # 10 + (10*2) + (100*0.5)

    # Example 2: Testing the exception
    with pytest.raises(ValueError):
        calculate_fee(-5, 50)  # negative weight
    with pytest.raises(ValueError):
        calculate_fee(10, -20)  # negative distance
# --- 3. HYPOTHESIS TEST (Property-Based) ---
@given(
    weight=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False),
    distance=st.floats(min_value=0.0, max_value=10000.0, allow_nan=False)
)
def test_calculate_fee_properties(weight, distance):
    fee = calculate_fee(weight, distance)

    # Property 1: Fee must always be at least the base fee of 10.0
    assert fee >= 10.0

    # Property 2: Fee must always be a float
    assert isinstance(fee, float)

    # Property 3: Fee increases monotonically with weight and distance
    # (not strictly tested here, but implied by formula)
    assert fee == 10.0 + (weight * 2.0) + (distance * 0.5)