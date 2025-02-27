---
title: Bitcoin Paper Errata and Details
authors:
  - david-a-harding
date: 2016-07-01
added: 2025-02-27
excerpt: 'A description of known problems in Satoshi Nakamoto''s paper, "Bitcoin: A Peer-to-Peer Electronic Cash System", as well as notes on terminology changes and how Bitcoin''s implementation differs from that described in the paper.'
original_site: David A. Harding's GitHub
original_url: https://gist.github.com/harding/dabea3d83c695e6b937bf090eddf2bb3
---

_A description of known problems in Satoshi Nakamoto's paper, "Bitcoin: A Peer-to-Peer Electronic Cash System", as well as notes on terminology changes and how Bitcoin's implementation differs from that described in the paper._

## Abstract

> The longest chain not only serves as proof of the sequence of events witnessed, but proof that it came from the largest pool of CPU power.

- **Implementation detail:** If each link in the chain (called "blocks" in Bitcoin) was built using the same amount of Proof Of Work (POW), the longest chain would be the one backed by the largest pool of computational power. However, Bitcoin was implemented in such a way that the amount of POW can vary between blocks, so it became important not to check for the "the longest chain" but rather "the chain demonstrating the most POW"; this is often shortened to "strongest chain".

  The [change][work not height] from checking for the longest chain to checking for the most-work chain occurred in July 2010, long after Bitcoin's initial release:

  ```diff
  -    if (pindexNew->nHeight > nBestHeight)
  +    if (pindexNew->bnChainWork > bnBestChainWork)
  ```

- **Terminology change:** General CPUs were used to generate the POW for the earliest Bitcoin blocks but POW generation today is mostly performed by specialist Application Specific Integrated Circuits (ASICs), so instead of saying "CPU power" it is perhaps more correct to say "computational power" or, simply, "hash rate" for the hashing used in generating the POW.

> As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers.

- **Terminology change:** The term "nodes" today is used to refer to full validation nodes, which are programs that enforce all the rules of the system. Programs (and hardware) that extend the chain today are called "miners" based on Nakamoto's analogy to gold miners in section 6 of the paper. Nakamoto expected all miners to be nodes but the software he released did not require all nodes to be miners. In the the original software, a simple menu item in the node GUI allowed toggling the mining function or or off.

  Today it is the case that the overwhelming number of nodes are not miners and that many individuals who own mining hardware do not use it with their own nodes (and even those that do mine with their own nodes often mine for short periods of time on top of newly discovered blocks without ensuring their node considers the new block valid). The early parts of the paper where "nodes" is mostly used without modification refer to mining using a full validation node; the later parts of the paper which refer to "network nodes" is mainly about what nodes can do even if they aren't mining.

- **Post-publication discovery:** When a new block is produced, the miner who produces that block can begin working on its sequel immediately but all other miners must wait for that new block to propagate across the network to them. This gives miners who produce many blocks an edge over miners who produce fewer blocks, and this can be exploited in what's known as the _selfish mining attack_ to allow an attacker with around 30% of total network hash rate to make other miners less profitable, perhaps driving them into following the attacking miner's policy. So instead of saying "a majority of CPU power is controlled by nodes that are not cooperating to attack the network" it is perhaps more correct to say "as long as nodes cooperating to attack the network control less than about 30% of the network".

## 2. Transactions

> We define an electronic coin as a chain of digital signatures. Each owner transfers the coin to the next by digitally signing a hash of the previous transaction and the public key of the next owner and adding these to the end of the coin.

- **Implementation detail:** Bitcoin implements a more general version of this system where digital signatures are not used directly but rather a "deterministic expression" is used instead. Just as a signature that matches a known public key can be used to enable a payment, the data that satisfies an known expression can also enable a payment. Generically, the expression that must be satisfied in Bitcoin in order to spend a coin is known as an "encumbrance". Almost all encumbrances in Bitcoin to date require providing at least one signature. So instead of saying "a chain of digital signatures" it is more correct to say "a chain of encumbrances". Given that transactions often have more than one input and more than one output, the structure is not very chain-like; it's more accurately described as a directed acyclic graph (DAG).

## 4. Proof-of-Work

> we implement the proof-of-work by incrementing a nonce in the block until a value is found that gives the block's hash the required zero bits.

- **Implementation detail:** Adam Back's Hashcash implementation requires finding a hash with the required number of leading zero bits. Bitcoin treats the hash as an integer and requires that it be less than a specified integer, which effectively allows a fractional number of bits to be specified.

> Proof-of-work is essentially one-CPU-one-vote.

- **Important note:** the vote here is not on the rules of the system but merely on the ordering of the transactions in order to provide assurances that an "electronic coin" cannot be easily double spent. This is described in more detail in section 11 of the paper where it says, "We consider the scenario of an attacker trying to generate an alternate chain faster than the honest chain. Even if this is accomplished, it does not throw the system open to arbitrary changes, such as creating value out of thin air or taking money that never belonged to the attacker. Nodes are not going to accept an invalid transaction as payment, and honest nodes will never accept a block containing them."

> proof-of-work difficulty is determined by a moving average targeting an average number of blocks per hour.

- **Implementation detail:** A moving average is not used. Instead, every 2,016th block has its reported generation time compared to the generation time for an earlier block, and the difference between them is used to calculate the average used for adjustment.

  Further, the average implemented in Bitcoin targets an average number of blocks per two weeks (not per hour as might be implied by the text). Other implemented rules may further slow adjustments, such as a rule that the adjustment can not increase block production speed by more than 300% per period, nor slow it by more than 75%.

## 7. Reclaiming Disk Space

> Once the latest transaction in a coin is buried under enough blocks, the spent transactions before it can be discarded to save disk space

- **Possible post-publication discovery:** Although the Merkle Tree structure described in this section can prove a transaction was included in a particular block, there is currently no way in Bitcoin to prove that a transaction has not been spent except to process all subsequent data in the blockchain. This means the method described here cannot be universally used for reclaiming disk space among all nodes, as all new nodes will need to process all transactions.

## 8. Simplified Payment Verification

> One strategy to protect against this would be to accept alerts from network nodes when they detect an invalid block, prompting the user's software to download the full block and alerted transactions to confirm the inconsistency.

- **Important Note:** although software has been produced that implements some parts of this section and calls that Simplified Payment Verification (SPV), none of these programs currently accepts alerts from network nodes (full validation nodes) when invalid blocks have been detected. This has placed bitcoins in so-called SPV wallets at risk in the past.

## 10. Privacy

> Some linking is still unavoidable with multi-input transactions, which necessarily reveal that their inputs were owned by the same owner

- **Post-publication invention:** the revelation of a common owner for different inputs isn't necessary if owners often mix their inputs with inputs belonging to other owners. For example, there's no public difference between Alice and Bob each contributing one of their inputs towards paying Charlie and Dan than there is between just Alice contributing two of her inputs towards paying Charlie and Dan.

  This technique is known today as [CoinJoin][] and software implementing it has been in use since 2015.

[coinjoin]: https://en.bitcoin.it/wiki/CoinJoin

## 11. Calculations

> The receiver generates a new key pair and gives the public key to the sender shortly before signing. This prevents the sender from preparing a chain of blocks ahead of time by working on it continuously until he is lucky enough to get far enough ahead, then executing the transaction at that moment.

- **Post-publication discovery:** nothing about the receiver generating a public key shortly before the spender signs a transaction prevents the spender from preparing a chain of blocks ahead of time. Early Bitcoin user Hal Finney discovered this attack and [described it][finney attack]: "Suppose the attacker is generating blocks occasionally. in each block he generates, he includes a transfer from address A to address B, both of which he controls.

  "To cheat you, when he generates a block, he doesn't broadcast it. Instead, he runs down to your store and makes a payment to your address C with his address A. You wait a few seconds, don't hear anything, and transfer the goods. He broadcasts his block now, and his transaction will take precedence over yours."

  The attack works for any number of confirmations, and is sometimes named the Finney Attack.

---

**Disclaimer:** the author of this document was not the first person to identify any of the problems described here---he has merely collected them into a single document.

**License:** this errata document is released under the [CC0][] 1.0 Universal Public Domain Dedication

**Updates:**

- 2018-06-14: Link to the commit where Nakamoto changed the consensus convergence mechanism from greatest-height to most-work. Credit for [commit archaeology](https://github.com/bitcoin-dot-org/bitcoin.org/issues/1325#issuecomment-230154542) to Gregory Maxwell.

- 2018-06-14: A moving average is not used. Mentioned on an IRC channel where logging is disallowed.

- 2018-06-14: Late key distribution does not prevent attackers from preparing forks, e.g. the Finney Attack. Mentioned by Kalle Rosenbaum [on Twitter](https://twitter.com/kallerosenbaum/status/999916373055684609).

- 2018-06-14: Inputs being spent in the same transaction does not necessarily lead to a privacy degradation thanks to Coinjoin. Mentioned by Chris Belcher in a [GitHub comment](https://gist.github.com/harding/dabea3d83c695e6b937bf090eddf2bb3#gistcomment-1983379).

- 2023-08-01: clarified a sentence about nodes not needing to be miners. Mentioned by Janaka-Steph in a [GitHub comment](https://gist.github.com/harding/dabea3d83c695e6b937bf090eddf2bb3?permalink_comment_id=2802344#gistcomment-2802344).

- 2023-08-01: the "chain of encumbrances" is more accurately described as a DAG. Mentioned by Mark "Murch" Erhardt in a [GitHub comment](https://gist.github.com/harding/dabea3d83c695e6b937bf090eddf2bb3?permalink_comment_id=4041255#gistcomment-4041255).

[cc0]: https://creativecommons.org/publicdomain/zero/1.0/
[finney attack]: https://bitcointalk.org/index.php?topic=3441.msg48384#msg48384
[work not height]: https://github.com/bitcoin/bitcoin/commit/40cd0369419323f8d7385950e20342e998c994e1#diff-623e3fd6da1a45222eeec71496747b31R420
