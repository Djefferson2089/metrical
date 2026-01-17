from metrical.core import ActivityLevel, Inputs, Sex, Units, calculate_all


def test_metric_bmi_known_value():
    inp = Inputs(units=Units.metric, sex=Sex.male, age_years=30, weight_kg=82, height_cm=178)
    r = calculate_all(inp, ActivityLevel.sedentary)
    assert round(r.bmi, 2) == 25.88


def test_metric_tdee_greater_than_bmr():
    inp = Inputs(units=Units.metric, sex=Sex.male, age_years=30, weight_kg=82, height_cm=178)
    r = calculate_all(inp, ActivityLevel.moderate)
    assert r.tdee > r.bmr
