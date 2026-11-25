import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BASE = "Starling-spell/prose-nonogram/" + "a" * 40 + "/fixtures/"


@pytest.fixture
def nonogram(direct_deploy):
    contract = direct_deploy(str(ROOT / "contracts/ProseNonogram.py"))
    return contract, sys.modules[type(contract._instance).__module__]


def mock(vm, coordinate, body, clues, status=200):
    vm.clear_mocks()
    vm.mock_web(re.escape("https://raw.githubusercontent.com/" + coordinate) + "$", {
        "method": "GET", "response": {"status": status, "headers": {}, "body": body},
    })
    vm.mock_llm(r".*PROSE NONOGRAM CLUE EXTRACTION.*", json.dumps(clues))


def test_ambiguous_puzzle_and_partial_marks(nonogram, direct_vm):
    contract, mod = nonogram
    body = (ROOT / "fixtures/two-options.json").read_bytes()
    coordinate = BASE + "two-options.json"
    digest = hashlib.sha256(body).hexdigest()
    clues = {"status": "READY", "rows": [[2], [2], []], "columns": [[1], [2], [1]]}
    mock(direct_vm, coordinate, body, clues)
    key = contract.compile_clues(coordinate, digest)
    assert direct_vm.run_validator()
    record = contract.get_puzzle(key)
    assert record["clues"] == clues
    assert record["result"] == {"status": "AMBIGUOUS", "count": 2, "fixed": ["?#?", "?#?", "..."]}
    forged = {k: v for k, v in record.items() if k != "result"}
    forged["clues"] = {**clues, "columns": [[2], [1], [1]]}
    assert not direct_vm.run_validator(leader_result=mod.canonical(forged))
    mock(direct_vm, coordinate, body + b" ", clues)
    assert not direct_vm.run_validator()
    assert contract.compile_clues(coordinate, digest) == key
    assert contract.analyze_marks(key, "#??/???/???") == {
        "status": "UNIQUE", "count": 1, "fixed": ["##.", ".##", "..."],
    }
    assert contract.analyze_marks(key, "?.?/???/???") == {
        "status": "INCONSISTENT", "count": 0, "fixed": [],
    }
    with direct_vm.expect_revert("Invalid partial grid"):
        contract.analyze_marks(key, "#??/???/??x")
    assert contract.get_puzzle(key) == record


def test_solution_count_and_forced_cells_against_all_three_by_three_grids(nonogram):
    _, mod = nonogram
    by_clue = {}
    for cells in itertools.product(".#", repeat=9):
        rows = ["".join(cells[i:i + 3]) for i in (0, 3, 6)]
        columns = ["".join(column) for column in zip(*rows)]
        pair = tuple(tuple(len(run) for run in re.findall(r"#+", line)) for line in rows + columns)
        by_clue.setdefault(pair, []).append(cells)
    for pair, boards in by_clue.items():
        clues = list(map(list, pair))
        fixed = ["".join(column[0] if len(set(column)) == 1 else "?"
                         for column in list(zip(*boards))[i:i + 3]) for i in (0, 3, 6)]
        assert mod.analyze(clues[:3], clues[3:], ["???"] * 3) == {
            "status": "UNIQUE" if len(boards) == 1 else "AMBIGUOUS",
            "count": len(boards), "fixed": fixed,
        }


def test_contradiction_with_equal_total_and_largest_grid(nonogram):
    _, mod = nonogram
    assert mod.analyze([[3], [], []], [[], [2], [1]], ["???"] * 3) == {
        "status": "INCONSISTENT", "count": 0, "fixed": [],
    }
    assert mod.analyze([[1]] * 5, [[1]] * 5, ["?????"] * 5) == {
        "status": "AMBIGUOUS", "count": 120, "fixed": ["?????"] * 5,
    }
    assert mod.analyze([[3], []], [[1], [1], [1]], ["???"] * 2) == {
        "status": "UNIQUE", "count": 1, "fixed": ["###", "..."],
    }


@pytest.mark.parametrize("clue", [[0], [True], [2, 1], [4], "two"])
def test_malformed_clues_rejected(nonogram, clue):
    _, mod = nonogram
    with pytest.raises(ValueError):
        mod.parse_clues({"status": "READY", "rows": [clue, [], []],
                         "columns": [[], [], []]}, 3, 3)


def test_unresolved_and_failed_acquisition(nonogram, direct_vm):
    contract, _ = nonogram
    body = (ROOT / "fixtures/cross.json").read_bytes()
    coordinate = BASE + "cross.json"
    digest = hashlib.sha256(body).hexdigest()
    unknown = {"status": "UNKNOWN", "rows": [], "columns": []}
    mock(direct_vm, coordinate, body, unknown, status=404)
    with direct_vm.expect_revert("Clue acquisition or interpretation failed"):
        contract.compile_clues(coordinate, digest)
    mock(direct_vm, coordinate, body, unknown)
    key = contract.compile_clues(coordinate, digest)
    assert contract.get_puzzle(key)["result"] == {"status": "UNKNOWN", "count": None, "fixed": []}
    with direct_vm.expect_revert("Unresolved clue prose"):
        contract.analyze_marks(key, "???/???/???")
