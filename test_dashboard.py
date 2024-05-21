import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import streamlit as st
import geoip2.database
import dashboard  

def get_country(ip_address):
    try:
        with geoip2.database.Reader('GeoLite2-Country.mmdb') as reader:
            response = reader.country(ip_address)
            return response.country.name
    except:
        return "Unknown"

class TestDashboardFunctions(unittest.TestCase):

    @patch('geoip2.database.Reader')
    def test_get_country(self, mock_reader):
        mock_response = MagicMock()
        mock_response.country.name = "United States"
        mock_reader.return_value.__enter__.return_value.country.return_value = mock_response

        ip_address = '8.8.8.8'
        country = get_country(ip_address)
        self.assertEqual(country, "United States")

    # Add more tests here as necessary

if __name__ == '__main__':
    unittest.main()


