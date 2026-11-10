# api-lab

API tests for QuickPizza (https://quickpizza.grafana.com) with pytest and requests.

## Install and run

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -v
pytest -v --html=report.html --self-contained-html
```

A full run sends about 140 requests and takes about a minute. Every test creates its own user, so tests are independent.

## Input domain model for POST /api/ratings

| Characteristic | Blocks | Values in the tests | Test that covers the block |
|---|---|---|---|
| C1 Value of `stars` | below 1 | 0 | `test_create_rating.py::test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of `stars` | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_stars_decimal_is_refused` |
| | text | "3" | `test_stars_text_is_refused` |
| | missing | no field | `test_stars_missing_is_refused` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_unknown_pizza_is_refused` |
| C4 Token | the user's own (base) | from `auth` | `test_base_choice_is_saved` |
| | none | no header | `test_no_token_is_refused` |
| | wrong length | `token short` | `test_short_token_is_refused` |

Base choice coverage: 1 + 2 + 3 + 1 + 2 = 9 tests (base test plus one test per non-base block). Boundary values for PUT /api/ratings/{id} (0, 1, 5, 6) are in `test_update_rating.py`.
