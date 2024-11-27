__package__ = "tests"

import unittest
#unitest for industry_process_a_method2
from industry.processA.method2.generated_script import industry_process_a_method2

class TestIndustryProcessAMethod2(unittest.TestCase):
    def test_industry_process_a_method2(self):
        """
        Test the industry_process_a_method2 function.
        """
        # Test inputs
        b0 = 2.0
        a0 = 1.0

        # Expected outputs
        expected_Ao = a0 + 2 * b0  # 1.0 + 2 * 2.0 = 5.0
        expected_Bo = a0 + 2.0 * 0.35 * b0  # 1.0 + 2.0 * 0.35 * 2.0 = 2.4
        expected_Co = expected_Ao - expected_Bo  # 5.0 - 2.4 = 2.6

        # Call the function
        result = industry_process_a_method2(b0, a0)

        # Assert the outputs
        self.assertAlmostEqual(result["Ao"], expected_Ao, places=5, msg="Ao calculation is incorrect.")
        self.assertAlmostEqual(result["Bo"], expected_Bo, places=5, msg="Bo calculation is incorrect.")
        self.assertAlmostEqual(result["Co"], expected_Co, places=5, msg="Co calculation is incorrect.")

if __name__ == "__main__":
    unittest.main()