from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SurveyTaker:

    survey_url = "https://tellthebell.com/Index.aspx?Page=1"
    driver = None

    def __init__(self, code):
        self.survey_code = code
        self.setup()

    def setup(self):
        # Configure Chrome Options
        chrome_options = webdriver.ChromeOptions()  # initialize Chrome options object
        chrome_options.add_argument("--incognito")  # opens window in incognito
        chrome_options.add_experimental_option("detach", True)  # detaches session to prevent window closure

        # Open the survey website
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def parse_survey_code(self):
        survey_code_array = self.survey_code

        if "-" in self.survey_code:
            survey_code_array = self.survey_code.split("-")

        else:
            survey_code_array = [survey_code_array[i:i + 4] for i in range(0, len(survey_code_array), 4)]

        return survey_code_array

    def open_survey_in_browser(self):
        # open the chrome browser
        self.driver.get(self.survey_url)

        # Check if page reached Successfully
        if "Taco Bell" in self.driver.title:
            print("Taco Bell Survey Paged Loaded!")
            return True
        else:
            print("Taco Bell Survey Page Failed To Load...")
            return False

    def enter_survey_code(self):
        print("Entering Survey Code...")

        # Get the parsed survey code {"1234", "1234", ...}
        survey_code_parsed = self.parse_survey_code()

        # Enter the survey code into each input field
        survey_code_number_1 = self.driver.find_element_by_name("CN1")
        survey_code_number_1.clear()
        survey_code_number_1.send_keys(survey_code_parsed[0])

        survey_code_number_2 = self.driver.find_element_by_name("CN2")
        survey_code_number_2.clear()
        survey_code_number_2.send_keys(survey_code_parsed[1])

        survey_code_number_3 = self.driver.find_element_by_name("CN3")
        survey_code_number_3.clear()
        survey_code_number_3.send_keys(survey_code_parsed[2])

        survey_code_number_4 = self.driver.find_element_by_name("CN4")
        survey_code_number_4.clear()
        survey_code_number_4.send_keys(survey_code_parsed[3])

        # Select The Next Button
        next_button = self.driver.find_element_by_name("NextButton")
        next_button.click()

        # Check if the survey code was accepted
        if self.driver.find_element_by_class_name("Error").is_displayed():
            print("Survey Code Failed...")
            return False
        else:
            print("Survey Code Successful!")
            return True


if __name__ == "__main__":
    survey_code = "1234-1234-1234-1234"

    # Test Opening Survey Page
    survey_taker = SurveyTaker(survey_code)
    survey_taker.open_survey_in_browser()

    # Test Parsing Survey Code
    parsed_code = survey_taker.parse_survey_code()
    print(parsed_code)

    # Test Entering The Survey Code
    survey_taker.enter_survey_code()




