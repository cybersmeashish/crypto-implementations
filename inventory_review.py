"""Read a supplied cryptographic inventory and expose planning gaps.

This tool does not inspect cryptographic implementations or attest PQ readiness.
"""
import argparse
import json
import math
from pathlib import Path

CLASSICAL_PUBLIC_KEY = {"RSA", "ECDH", "ECDSA", "Ed25519", "X25519"}
PQC_STANDARDS = {"ML-KEM": "FIPS 203", "ML-DSA": "FIPS 204", "SLH-DSA": "FIPS 205"}
SYMMETRIC = {"AES-256", "HMAC-SHA-256"}


def review(inventory):
    if not isinstance(inventory, list):
        raise ValueError("Inventory must be a list")
    seen = set()
    results = []
    for item in inventory:
        if not isinstance(item, dict):
            raise ValueError("Each inventory record must be an object")
        asset_id = item.get("asset_id")
        if not isinstance(asset_id, str) or not asset_id.strip() or asset_id in seen:
            raise ValueError("Asset IDs must be unique non-empty strings")
        seen.add(asset_id)
        years = item.get("confidentiality_years")
        if years is not None and (
            isinstance(years, bool) or not isinstance(years, (int, float))
            or not math.isfinite(years) or years < 0
        ):
            raise ValueError("Confidentiality lifetime must be a non-negative number")
        algorithm = item.get("algorithm")
        if not isinstance(algorithm, str):
            raise ValueError("Algorithm must be a string")
        owner = item.get("owner")
        gaps = []
        if not isinstance(owner, str) or not owner.strip():
            gaps.append("Assign an accountable owner")
        if not isinstance(item.get("purpose"), str) or not item["purpose"].strip():
            gaps.append("Record the cryptographic purpose")
        if not isinstance(item.get("dependency"), str) or not item["dependency"].strip():
            gaps.append("Record the implementation or supplier dependency")
        if years is None:
            gaps.append("Record the required confidentiality lifetime")
        if algorithm in CLASSICAL_PUBLIC_KEY:
            category = "classical-public-key-migration-review"
            next_step = "Review replacement options, interoperability, and vendor support"
        elif algorithm in PQC_STANDARDS:
            category = "pqc-labelled-verification-required"
            next_step = f"Verify the implementation and integration against {PQC_STANDARDS[algorithm]}"
        elif algorithm in SYMMETRIC:
            category = "symmetric-separate-review"
            next_step = "Review key strength, key management, and the surrounding public-key dependencies"
        else:
            category = "unclassified-review-required"
            next_step = "Identify the algorithm, parameters, and implementation before deciding"
        results.append({
            "asset_id": asset_id, "algorithm": algorithm, "category": category,
            "confidentiality_years": years, "gaps": gaps, "next_step": next_step,
            "readiness_attested": False,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    print(json.dumps(review(json.loads(args.inventory.read_text())), indent=2))


if __name__ == "__main__":
    main()
