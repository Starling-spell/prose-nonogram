**Contribution type** Builder → Intelligent Contracts

**Title** ProseNonogram — Consensus-Verified Clues and Exact Puzzle Solving

ProseNonogram compiles published natural-language clues into the row and column
runs of a nonogram. The leader and validators independently fetch the full
commit-pinned document, verify its SHA-256, and interpret every run. Consensus
compares the source text and exact clue arrays. Those arrays determine the
number of valid boards and the cells that have the same value in every board.

Read-only queries recompute both results for a hypothetical partial board.
The contract handles rectangular boards up to 5×5.

The StudioNet demonstration uses three authored puzzles. The compiled clues
yielded one, two, and zero solutions. On the two-solution puzzle, one partial
mark selected a unique solution and a conflicting mark yielded zero. Nine
direct tests passed, including comparison against all 512 possible 3×3 boards.

- [Repository](https://github.com/Starling-spell/prose-nonogram)
- [Pinned deployed source](https://github.com/Starling-spell/prose-nonogram/blob/d18912796039259ff0da1f4bbf9fe39a28be7b9b/contracts/ProseNonogram.py)
- [StudioNet deployment](https://explorer-studio.genlayer.com/address/0x66c2D199a6e29f16117744736068574622D13C87)
- [Finalized receipts and puzzle readbacks](https://github.com/Starling-spell/prose-nonogram/blob/main/LIVE_PROOFS.md)
