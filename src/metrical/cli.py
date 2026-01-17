from __future__ import annotations

import json
from typing import Optional

import typer

from .core import ActivityLevel, Inputs, Sex, Units, calculate_all

app = typer.Typer(
    add_completion=False,
    help="MetriCal — BMI/BMR/TDEE calculator with metric/imperial support.",
)


def _print_human(results, activity: ActivityLevel) -> None:
    typer.echo("\n📊 Results")
    typer.echo("-" * 40)
    typer.echo(f"BMI:  {results.bmi:.2f}  ({results.bmi_category})")
    typer.echo(f"BMR:  {results.bmr:.0f} kcal/day")
    typer.echo(
        f"TDEE: {results.tdee:.0f} kcal/day  ({activity.value}, x{results.activity_multiplier})"
    )


def _print_json(results, activity: ActivityLevel) -> None:
    payload = {
        "bmi": round(results.bmi, 2),
        "bmi_category": results.bmi_category,
        "bmr_kcal_per_day": round(results.bmr),
        "tdee_kcal_per_day": round(results.tdee),
        "activity_level": activity.value,
        "activity_multiplier": results.activity_multiplier,
    }
    typer.echo(json.dumps(payload, indent=2))


@app.command("calc")
def calc(
    sex: Sex = typer.Option(..., help="Biological sex used by the BMR equation."),
    age: int = typer.Option(..., min=1, help="Age in years."),
    units: Units = typer.Option(
        Units.imperial,
        "--units",
        "-u",
        help="Input units for weight/height.",
        case_sensitive=False,
    ),
    weight_kg: Optional[float] = typer.Option(None, help="Weight in kilograms (metric)."),
    height_cm: Optional[float] = typer.Option(None, help="Height in centimeters (metric)."),
    weight_lb: Optional[float] = typer.Option(None, help="Weight in pounds (imperial)."),
    height_ft: Optional[int] = typer.Option(None, help="Height feet (imperial)."),
    height_in: Optional[int] = typer.Option(None, help="Height inches (imperial)."),
    activity: ActivityLevel = typer.Option(
        ActivityLevel.moderate,
        help="Activity level used to compute TDEE.",
        case_sensitive=False,
    ),
    json_out: bool = typer.Option(False, "--json", help="Print machine-readable JSON output."),
):
    """
    Calculate BMI, BMR, and TDEE.
    """
    inp = Inputs(
        units=units,
        sex=sex,
        age_years=age,
        weight_kg=weight_kg,
        height_cm=height_cm,
        weight_lb=weight_lb,
        height_ft=height_ft,
        height_in=height_in,
    )

    try:
        results = calculate_all(inp, activity)
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e

    if json_out:
        _print_json(results, activity)
    else:
        _print_human(results, activity)


@app.command("activity-levels")
def activity_levels():
    """
    Show activity levels and multipliers.
    """
    typer.echo("Activity levels:")
    typer.echo("- sedentary     (x1.2)   little/no exercise")
    typer.echo("- light         (x1.375) 1–3 days/week")
    typer.echo("- moderate      (x1.55)  3–5 days/week")
    typer.echo("- very-active   (x1.725) 6–7 days/week")
    typer.echo("- extra-active  (x1.9)   physical job + training")
