import unittest
from app.services.scorer import Scorer

class TestScorer(unittest.TestCase):
    def test_perfect_score(self):
        """Test perfect match scenario."""
        result = Scorer.calculate_score(1.0, ["python", "react"], ["python", "react"])
        self.assertEqual(result["total_score"], 100.0)

    def test_partial_match(self):
        """Test partial match."""
        # Semantic = 0.8 -> 48pts
        # Skills = 50% -> 20pts
        # Total = 68
        result = Scorer.calculate_score(0.8, ["python"], ["python", "react"])
        self.assertAlmostEqual(result["total_score"], 68.0, delta=0.1)

    def test_zero_match(self):
        """Test no match."""
        result = Scorer.calculate_score(0.0, ["java"], ["python"])
        self.assertEqual(result["total_score"], 0.0)

if __name__ == "__main__":
    unittest.main()
