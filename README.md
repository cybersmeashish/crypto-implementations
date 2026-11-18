# Cryptographic inventory and post-quantum readiness

A read-only planning tool and reference guide for the transition to post-quantum cryptography. Start by identifying cryptographic dependencies, owners, purposes, and the lifetime of the information they protect.

**Status:** inventory review lab and migration research. This repository does not implement a cryptographic primitive or certify that a system is quantum-safe.

## Reproduce the example

```bash
git clone https://github.com/cybersmeashish/crypto-implementations.git
cd crypto-implementations
python3 inventory_review.py examples/synthetic-inventory.json
python3 -m unittest discover -s tests -v
```

Python 3.10 or later. No external dependencies, keys, network calls, or cloud account are required. The input contains synthetic asset records.

| Artifact | Purpose |
| --- | --- |
| [inventory_review.py](inventory_review.py) | Expose missing owners and dependencies; separate classical public-key, PQC-labelled, symmetric, and unknown records |
| [Synthetic inventory](examples/synthetic-inventory.json) | Transport, signing, and pilot examples |
| [Migration decision guide](docs/migration-decisions.md) | Define the evidence needed before choosing a migration |
| [Tests](tests/test_inventory_review.py) | Unknowns, invalid lifetimes, duplicate IDs, ownership gaps, and unverified PQC labels |
| [Verification record](docs/verification.md) | Local test conditions and limits |

## Primary standards

- [NIST FIPS 203: ML-KEM](https://csrc.nist.gov/pubs/fips/203/final), a key-encapsulation standard.
- [NIST FIPS 204: ML-DSA](https://csrc.nist.gov/pubs/fips/204/final), a digital-signature standard.
- [NIST FIPS 205: SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final), a digital-signature standard.

The categorization and review workflow are original planning choices. Algorithm names in a register do not establish correct implementations, validated modules, integration security, or interoperability.

## Business question

Which dependency needs an owner, a supplier decision, and a tested migration path before it becomes expensive to replace?

The tool deliberately reports `readiness_attested: false` for every record. Follow the [decision guide](docs/migration-decisions.md) to assemble evidence.

[Security portfolio](https://github.com/cybersmeashish) · [Connected security research](https://github.com/cybersmeashish/Ashish-research)
