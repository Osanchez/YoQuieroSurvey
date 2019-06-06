from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SurveyTaker:

    survey_url = "https://tellthebell.com/Index.aspx?Page=1"

    def __init__(self, code):
        self.survey_code = code

    def parse_survey_code(self):
        parsed_code = self.survey_code.split("-")
        return parsed_code

    def open_survey_in_browser(self):
        # Configure Chrome Options
        chrome_options = webdriver.ChromeOptions()  # initialize Chrome options object
        chrome_options.add_argument("--incognito")  # opens window in incognito
        chrome_options.add_experimental_option("detach", True)  # detaches session to prevent window closure

        # Open the survey website
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        driver.get(self.survey_url)  # open the chrome browser


if __name__ == "__main__":
    survey_code = "1234-1234-1234-1234"
    survey_taker = SurveyTaker(survey_code)
    survey_taker.open_survey_in_browser()




