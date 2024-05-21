import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class StreamlitIntegrationTest(unittest.TestCase):

    def setUp(self):
        # Set up the web driver (e.g., Chrome)
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Quit the web driver
        self.driver.quit()

    def test_dashboard_loads(self):
        driver = self.driver
        driver.get('http://localhost:8501')  # URL where your Streamlit app is running

        # Allow some time for the app to load
        time.sleep(5)

        # Check if the title is present
        title = driver.find_element(By.TAG_NAME, 'title')
        self.assertIn('Events Dashboard', title.get_attribute('innerHTML'))

        # Check if the metrics are present
        metrics = driver.find_elements(By.CLASS_NAME, 'metric')
        self.assertEqual(len(metrics), 3)

        # Check if file uploader is present
        file_uploader = driver.find_element(By.CLASS_NAME, 'stFileUploader')
        self.assertIsNotNone(file_uploader)

        # Check if date input fields are present
        date_inputs = driver.find_elements(By.CLASS_NAME, 'stDateInput')
        self.assertEqual(len(date_inputs), 2)

        # Check if sidebar filters are present
        sidebar = driver.find_element(By.CLASS_NAME, 'stSidebar')
        filters = sidebar.find_elements(By.CLASS_NAME, 'stMultiSelect')
        self.assertGreaterEqual(len(filters), 3)

    def test_file_upload(self):
        driver = self.driver
        driver.get('http://localhost:8501')  

        # Allow some time for the app to load
        time.sleep(5)

        # Upload a test file
        file_uploader = driver.find_element(By.CLASS_NAME, 'stFileUploader')
        file_uploader.send_keys(r'C:\Users\Ztash\OneDrive\Desktop\olympics\logs.csv')  

        # Allow some time for the file to be processed
        time.sleep(5)

        # Check if the filename is displayed
        filename_display = driver.find_element(By.TAG_NAME, 'span')
        self.assertIn('logs.csv', filename_display.get_attribute('innerHTML'))  

if __name__ == '__main__':
    unittest.main()
