import unittest
from main import greeting, calculate_pi_fifth_digit


class TestMain(unittest.TestCase):
    
    def test_greeting(self):
        """Test that greeting function works without errors."""
        try:
            greeting()
        except Exception as e:
            self.fail(f"greeting() raised {type(e).__name__} unexpectedly!")
    
    def test_calculate_pi_fifth_digit(self):
        """Test that pi is calculated correctly to the 5th digit."""
        result = calculate_pi_fifth_digit()
        
        # Pi to 5 decimal places is 3.14159
        expected_pi = 3.14159
        
        # Check if result is within acceptable range
        self.assertEqual(result, expected_pi, 
                        f"Expected {expected_pi}, but got {result}")
    
    def test_calculate_pi_return_type(self):
        """Test that calculate_pi_fifth_digit returns a float."""
        result = calculate_pi_fifth_digit()
        self.assertIsInstance(result, float, 
                            "calculate_pi_fifth_digit should return a float")
    
    def test_calculate_pi_accuracy(self):
        """Test that pi calculation is accurate to at least 5 decimal places."""
        result = calculate_pi_fifth_digit()
        
        # Pi to high precision
        actual_pi = 3.14159265358979323846
        
        # Check that the difference is within acceptable tolerance
        tolerance = 0.000001  # Tolerance for 5 decimal places
        self.assertAlmostEqual(result, actual_pi, places=5,
                              msg=f"Pi calculated as {result}, expected approximately {actual_pi}")


if __name__ == '__main__':
    unittest.main()
