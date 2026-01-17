![CI](../../actions/workflows/ci.yml/badge.svg)


# MetriCal

MetriCal is a Python CLI for calculating **BMI**, **BMR**, and **TDEE** with **metric or imperial** inputs.

---

## Install

pip install metrical-cli

## Usage

## Imperial (pounds, feet & inches)

metrical calc \
  --units imperial \
  --sex male \
  --age 30 \
  --weight-lb 180 \
  --height-ft 5 \
  --height-in 10 \
  --activity moderate


## Metric (kilograms, centimeters)

metrical calc \
  --units metric \
  --sex female \
  --age 28 \
  --weight-kg 65 \
  --height-cm 165 \
  --activity light


## JSON Output (for scripts & automation)

metrical calc \
  --units imperial \
  --sex male \
  --age 30 \
  --weight-lb 180 \
  --height-ft 5 \
  --height-in 10 \
  --json


## Activity Levels

| Level        | Multiplier | Description             |
| ------------ | ---------- | ----------------------- |
| sedentary    | 1.2        | little or no exercise   |
| light        | 1.375      | 1–3 days/week           |
| moderate     | 1.55       | 3–5 days/week           |
| very-active  | 1.725      | 6–7 days/week           |
| extra-active | 1.9        | physical job + training |


## Development

python -m venv .venv
## Windows
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
