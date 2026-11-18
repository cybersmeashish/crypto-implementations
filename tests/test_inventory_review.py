import unittest
from inventory_review import review


def record(**changes):
    return {
        "asset_id": "tls", "owner": "Platform owner", "algorithm": "ECDH",
        "purpose": "Key agreement", "dependency": "Synthetic library",
        "confidentiality_years": 7, **changes,
    }


class InventoryReviewTests(unittest.TestCase):
    def test_classical_public_key_needs_migration_review(self):
        self.assertEqual(review([record()])[0]["category"], "classical-public-key-migration-review")

    def test_pqc_label_does_not_attest_readiness(self):
        result = review([record(algorithm="ML-KEM")])[0]
        self.assertFalse(result["readiness_attested"])
        self.assertIn("FIPS 203", result["next_step"])

    def test_missing_owner_and_dependency_are_visible(self):
        result = review([record(owner="", dependency="")])[0]
        self.assertEqual(len(result["gaps"]), 2)

    def test_unknown_algorithm_is_not_treated_as_ready(self):
        result = review([record(algorithm="unknown")])[0]
        self.assertEqual(result["category"], "unclassified-review-required")

    def test_duplicate_assets_are_rejected(self):
        with self.assertRaises(ValueError):
            review([record(), record()])

    def test_negative_or_boolean_lifetime_is_rejected(self):
        for lifetime in (-1, True, float("nan"), float("inf")):
            with self.subTest(lifetime=lifetime), self.assertRaises(ValueError):
                review([record(confidentiality_years=lifetime)])

    def test_unknown_lifetime_stays_missing(self):
        result = review([record(confidentiality_years=None)])[0]
        self.assertIsNone(result["confidentiality_years"])
        self.assertIn("Record the required confidentiality lifetime", result["gaps"])

    def test_symmetric_algorithm_gets_separate_review(self):
        self.assertEqual(review([record(algorithm="AES-256")])[0]["category"], "symmetric-separate-review")

    def test_malformed_inventory_is_rejected(self):
        for value in ({}, [None], [record(asset_id="")], [record(algorithm=None)]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                review(value)


if __name__ == "__main__":
    unittest.main()
