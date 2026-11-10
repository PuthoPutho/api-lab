import pytest

ALL_TOOLS = ["Knife", "Pizza cutter", "Scissors"]


# The pizza never needs a tool that the customer excluded.
# Blocks covered: 0 excluded, 1 excluded, 2 excluded.
@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Defect 1: excluding all three tools must give 400 and a JSON error, not 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools gives 500 with an empty body",
    strict=True,
)
def test_all_tools_excluded_is_refused_with_400(api, auth):
    res = api.post("/api/pizza", json={"excludedTools": ALL_TOOLS}, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
