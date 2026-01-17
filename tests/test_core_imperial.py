from metrical.core import ActivityLevel, Inputs, Sex, Units, calculate_all


def test_imperial_reasonable_bmi_range():
    inp = Inputs(
        units=Units.imperial,
        sex=Sex.male,
        age_years=30,
        weight_lb=180,
        height_ft=5,
        height_in=10,
    )
    r = calculate_all(inp, ActivityLevel.sedentary)
    assert 25.0 < r.bmi < 26.5
