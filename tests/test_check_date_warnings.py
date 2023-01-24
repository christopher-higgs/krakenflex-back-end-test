import unittest
from outages import check_date_warnings
from datetime import datetime, timedelta

class TestCheckDateWarnings(unittest.TestCase):
    """ This class contains tests for the check_date_warnings
        function in outages.py, which generates a list of warnings
        to be displayed in the output table from a given begin and end date.
    """

    def test_no_warnings(self):
        """ Given two valid dates
            Then no warnings are generated
        """
        begin = datetime(2023,1,1) # 01/01/2023
        end = datetime(2023,1,9)   # 09/01/2023
        self.assertEqual(check_date_warnings(begin, end), [])
    
    def test_negative_duration(self):
        """ Given an end date that occurs before the begin date
            Then the warning 'Negative duration detected' is printed
        """
        begin = datetime(2023,1,9) # 09/01/2023
        end = datetime(2023,1,1)   # 01/09/2023
        self.assertEqual(check_date_warnings(begin, end), ['Negative duration detected\n'])
    
    def test_future_begin(self):
        """ Given a begin date that occurs in the future
            Then the warning 'Outage has future begin date' is printed
            And the warning 'Negative duration detected' is printed
        """
        begin = datetime.now() + timedelta(days=7) # 7 days from now
        end = datetime(2022,1,1)    # 01/09/2023
        self.assertTrue('Outage has future begin date\n' in check_date_warnings(begin, end))
        self.assertTrue('Negative duration detected\n' in check_date_warnings(begin, end))
    
    def test_future_end(self):
        """ Given an end date that occurs in the future
            Then the warning 'Outage has future end date' is printed
        """
        begin = datetime(2023,1,9)  # 09/01/2023
        end = datetime.now() + timedelta(days=7)   # 7 days from now
        self.assertTrue('Outage has future end date\n' in check_date_warnings(begin, end))
    
    def test_all_warnings(self):
        """ Given a begin date that occurs in the future
            And an end date that occurs in the future and before the begin date
            Then the warning 'Outage has future end date' is printed
        """
        begin = datetime.now() + timedelta(days=8) # 8 days from now
        end = datetime.now() + timedelta(days=7)   # 7 days from now
        self.assertTrue('Negative duration detected\n' in check_date_warnings(begin, end))
        self.assertTrue('Outage has future begin date\n' in check_date_warnings(begin, end))
        self.assertTrue('Outage has future end date\n' in check_date_warnings(begin, end))
