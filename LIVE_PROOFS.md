# StudioNet proofs

The deployed source matches the pinned repository source. All four
transactions below finalized with successful execution and majority agreement.
The proof journal includes the verified contract digest, each puzzle's
source text and interpreted clues, plus transaction signers, nonces, and fee
quotes.
[Deployment](https://explorer-studio.genlayer.com/address/0x66c2D199a6e29f16117744736068574622D13C87) ·
[Pinned source](https://github.com/Starling-spell/prose-nonogram/blob/d18912796039259ff0da1f4bbf9fe39a28be7b9b/contracts/ProseNonogram.py) ·
[Machine-readable journal](PROOFS.json)

| Transaction | Verified result |
| --- | --- |
| [Deploy](https://explorer-studio.genlayer.com/tx/0xbefc263197ea005754f8585f8d80fbda3a90979dbd62a3db9af3d344cd9a2432) | Source matched the pinned Python contract. |
| [Compile cross](https://explorer-studio.genlayer.com/tx/0x5c0dd5c054bd7bcf347d0b44227fd4de16bfe562b12432643b21e5db13c91ed7) | One solution. Fixed rows `.#.`, `###`, `.#.`. |
| [Compile two options](https://explorer-studio.genlayer.com/tx/0xcf0aafea5d11c736afaa2eaea8fe87647c5bb4dbb6db9a6219ba3d8c972ae9b5) | Two solutions. Fixed rows `?#?`, `?#?`, `...`. |
| [Compile contradictory clues](https://explorer-studio.genlayer.com/tx/0xe6a50a290ce75db1b96e8e20b445103581dc9675943ab117e8376f9c86dad3bf) | Zero solutions. The clue arrays are well formed and their totals agree, but the axes cannot coexist. |

The read-only mark query `#??/???/???` narrowed the two-solution puzzle to
one board with rows `##.`, `.##`, `...`. Query `?.?/???/???` produced zero
solutions. The stored puzzle still reports two solutions.

The first deployment attempt was rejected at submission with
`FeesDistributionMissing`. The accepted deployment used GenLayer SDK 2.0.0
with the StudioNet fee quote and test GEN from the built-in faucet.
[Rejected attempt journal](REJECTED_DEPLOYMENT.json)
