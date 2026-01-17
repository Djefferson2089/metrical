from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite


class Units(str, Enum):
    imperial = "imperial"
    metric = "metric"


class Sex(str, Enum):
    male = "male"
    female = "female"


class ActivityLevel(str, Enum):
    sedentary = "sedentary"  # little/no exercise
    light = "light"  # 1–3 days/week
    moderate = "moderate"  # 3–5 days/week
    very_active = "very-active"  # 6–7 days/week
    extra_active = "extra-active"  # physical job + training


_ACTIVITY_MULTIPLIERS: dict[ActivityLevel, float] = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.very_active: 1.725,
    ActivityLevel.extra_active: 1.9,
}


@dataclass(frozen=True)
class Inputs:
    units: Units
    sex: Sex
    age_years: int

    # metric
    weight_kg: float | None = None
    height_cm: float | None = None

    # imperial
    weight_lb: float | None = None
    height_ft: int | None = None
    height_in: int | None = None


@dataclass(frozen=True)
class Results:
    bmi: float
    bmi_category: str
    bmr: float
    tdee: float
    activity_multiplier: float


def _require(condition: bool, msg: str) -> None:
    if not condition:
        raise ValueError(msg)


def pounds_to_kg(lb: float) -> float:
    _require(isfinite(lb) and lb > 0, "Weight must be a positive number.")
    return lb * 0.45359237


def inches_to_cm(inches: float) -> float:
    _require(isfinite(inches) and inches > 0, "Height must be a positive number.")
    return inches * 2.54


def ft_in_to_cm(ft: int, inches: int) -> float:
    _require(ft >= 0 and inches >= 0, "Height cannot be negative.")
    total_inches = (ft * 12) + inches
    _require(total_inches > 0, "Height must be greater than 0.")
    return inches_to_cm(total_inches)


def bmi_from_metric(weight_kg: float, height_cm: float) -> float:
    _require(isfinite(weight_kg) and weight_kg > 0, "Weight must be a positive number.")
    _require(isfinite(height_cm) and height_cm > 0, "Height must be a positive number.")
    height_m = height_cm / 100.0
    return weight_kg / (height_m**2)


def bmi_category(bmi: float) -> str:
    _require(isfinite(bmi) and bmi > 0, "BMI must be a positive number.")
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def bmr_mifflin_st_jeor(weight_kg: float, height_cm: float, age_years: int, sex: Sex) -> float:
    _require(isfinite(weight_kg) and weight_kg > 0, "Weight must be a positive number.")
    _require(isfinite(height_cm) and height_cm > 0, "Height must be a positive number.")
    _require(isinstance(age_years, int) and age_years > 0, "Age must be a positive integer.")
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years)
    return base + 5 if sex == Sex.male else base - 161


def tdee_from_bmr(bmr: float, activity: ActivityLevel) -> tuple[float, float]:
    _require(isfinite(bmr) and bmr > 0, "BMR must be a positive number.")
    mult = _ACTIVITY_MULTIPLIERS[activity]
    return bmr * mult, mult


def normalize_inputs(inp: Inputs) -> tuple[float, float]:
    """
    Returns (weight_kg, height_cm) from either metric or imperial inputs.
    """
    _require(
        isinstance(inp.age_years, int) and inp.age_years > 0, "Age must be a positive integer."
    )

    if inp.units == Units.metric:
        _require(inp.weight_kg is not None and inp.height_cm is not None, "Metric inputs required.")
        return float(inp.weight_kg), float(inp.height_cm)

    _require(inp.weight_lb is not None, "Imperial weight (lb) is required.")
    _require(
        inp.height_ft is not None and inp.height_in is not None,
        "Imperial height (ft/in) is required.",
    )
    weight_kg = pounds_to_kg(float(inp.weight_lb))
    height_cm = ft_in_to_cm(int(inp.height_ft), int(inp.height_in))
    return weight_kg, height_cm


def calculate_all(inp: Inputs, activity: ActivityLevel) -> Results:
    """
    Main entry point for the CLI: computes BMI, BMR, and TDEE.
    """
    weight_kg, height_cm = normalize_inputs(inp)
    bmi = bmi_from_metric(weight_kg, height_cm)
    cat = bmi_category(bmi)
    bmr = bmr_mifflin_st_jeor(weight_kg, height_cm, inp.age_years, inp.sex)
    tdee, mult = tdee_from_bmr(bmr, activity)
    return Results(
        bmi=bmi,
        bmi_category=cat,
        bmr=bmr,
        tdee=tdee,
        activity_multiplier=mult,
    )
