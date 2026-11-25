# ProseNonogram

ProseNonogram compiles a published puzzle description into row and column clues.
The leader and each validator fetch the entire commit-pinned GitHub document,
verify its SHA-256, and independently interpret the prose into ordered runs of
filled cells. Exact agreement covers the source text and every run on both axes.
The caller submits a source coordinate and digest.

The contract enumerates matching row patterns while pruning impossible column
prefixes. It stores the full source, agreed clues, exact number of solutions,
and cells shared by all solutions. A puzzle may have one solution, multiple
solutions, or inconsistent clues. If interpretation is unresolved, the
contract stores the source with an UNKNOWN decision.

Anyone can query a hypothetical partial board without changing stored state.
For example, `#??/???/???` constrains the top-left cell of a 3×3 board to filled.
Use `.` for empty, `#` for filled, and `?` for unknown. Separate rows with `/`.
The response repeats the exact solution count and fixed cells for completions
that respect those marks. Incompatible marks yield zero completions.

- `compile_clues(coordinate, expected_sha256)` returns the immutable puzzle ID.
- `get_puzzle(key)` retrieves the source, clues, and unmarked result.
- `analyze_marks(key, marks)` evaluates a hypothetical partial board.

Documents use exactly `height`, `width`, and `clues`. The board is 2–5 rows by
2–5 columns. The full UTF-8 document is limited to 4096 bytes and the clue prose
to 1800 bytes. Model interpretation determines the stored mathematical problem.
The fixtures are authored examples with unique, ambiguous, and inconsistent clues.
[GenLayer equivalence principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)

```sh
python -m pip install -r requirements-dev.txt
genvm-lint check contracts/ProseNonogram.py
python -m pytest tests -q
```

[Deployment and proof ledger](LIVE_PROOFS.md) · [Submission text](SUBMISSION.md)

To replay the recorded receipts, deployed source check, and puzzle readbacks:

```sh
npm ci --ignore-scripts
node scripts/live.mjs --verify-only
```
