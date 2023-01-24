import unittest
from outages import generate_site_outages

class TestGenerateSiteOutages(unittest.TestCase):
    """ This class contains tests for the generate_site_outages function
        in outages.py.
    """
    def test_site_outages_successful_only(self):
        """ Given a list of valid outages only
            And valid site information

            Then the function 'generate_site_outages' should return 
            the data with 'id', 'name', 'begin' and 'end' values
        """
        mock_outages = [
            {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'}, # OK
            {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}  # OK
        ]
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2"}
            ]
        }
        self.assertEqual(
            generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'),
            [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'},
             {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2', 'begin': '2022-05-09T04:47:25.211Z', 'end': '2022-12-02T18:37:16.039Z'}]
        )

    def test_site_outages_successful_mix(self):
        """ Given:
            At least one valid outage from a list of all outages
            And an outage that began before 2022-01-01
            And an outage that is not associated with this site
            Valid site information

            Then the function 'generate_site_outages' should return 
            the data with 'id', 'name', 'begin' and 'end' values
        """
        mock_outages = [
            {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'}, # OK
            {'id': '09e77920-ca66-4263-8a15-9409210ff858', 'begin': '2021-06-01T18:01:58.920Z', 'end': '2021-09-21T20:02:45.438Z'}, # began too early
            {'id': '0817cd44-b3ed-4790-8ce4-5b477ea86402', 'begin': '2022-12-04T07:25:45.750Z', 'end': '2022-12-25T16:11:32.270Z'}, # not this site
            {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}  # OK
        ]
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2"}
            ]
        }
        self.assertEqual(
            generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'),
            [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'},
             {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2', 'begin': '2022-05-09T04:47:25.211Z', 'end': '2022-12-02T18:37:16.039Z'}]
        )
    
    def test_site_outages_invalid_outage_dates(self):
        """ Given there are only outages with invalid dates present
            And there is valid site info

            Then the function 'generate_site_outages' should return an empty list
        """
        mock_outages = [
            {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'}, # began too early
            {'id': '09e77920-ca66-4263-8a15-9409210ff858', 'begin': '2021-06-01T18:01:58.920Z', 'end': '2021-09-21T20:02:45.438Z'}, # began too early
            {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'begin': '1997-01-09T07:25:45.750Z', 'end': '2022-12-25T16:11:32.270Z'}  # began too early
        ]
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2"}
            ]
        }
        self.assertEqual(generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'), [])
        
    def test_site_outages_no_site_outages(self):
        """ Given there are no outages relating to the given site
            And there is valid site info

            Then the function 'generate_site_outages' should return an empty list
        """
        mock_outages = [
            {'id': '311183e7-fb90-436b-9951-63392b36bdd2', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'}, # not this site
            {'id': '99e77920-ca66-4263-8a15-9409210ff858', 'begin': '2021-06-01T18:01:58.920Z', 'end': '2021-09-21T20:02:45.438Z'}, # not this site
            {'id': '011183e7-fb90-436b-9951-63392b36bdd2', 'begin': '1997-01-09T07:25:45.750Z', 'end': '2022-12-25T16:11:32.270Z'}  # not this site
        ]
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2"}
            ]
        }
        self.assertEqual(generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'), [])

    def test_site_outages_invalid_outages_mix(self):
        """ Given there are a mixture of invalid outages from the list of all outages
            And there is valid site info

            Then the function 'generate_site_outages' should return an empty list
        """
        mock_outages = [
            {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-09-15T19:45:10.341Z'}, # began too early
            {'id': '09e77920-ca66-4263-8a15-9409210ff858', 'begin': '2021-06-01T18:01:58.920Z', 'end': '2021-09-21T20:02:45.438Z'}, # began too early
            {'id': '0817cd44-b3ed-4790-8ce4-5b477ea86402', 'begin': '2022-12-04T07:25:45.750Z', 'end': '2022-12-25T16:11:32.270Z'}  # not this site
        ]
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2"}
            ]
        }
        self.assertEqual(generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'), [])
    
    def test_site_outages_no_outages(self):
        """ Given there are no outages returned from the server
            And there is valid site info

            Then:
            The function 'generate_site_outages' should return an empty list
        """
        mock_outages = []
        mock_site_info = {
            'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree', 'devices': [
                {'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'}
            ]
        }
        self.assertEqual(generate_site_outages(mock_outages, mock_site_info, '2022-01-01T00:00:00.000Z'), [])