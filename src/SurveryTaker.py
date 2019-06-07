from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
        try:
            if self.driver.find_element_by_class_name("Error").is_displayed():
                print("Survey Code Failed...")
        except NoSuchElementException:
            print("Survey Code Entered Successfully!")

    def select_overall_satisfaction_level(self, satisfaction_level):

        print("Selecting Satisfaction Level: " + str(satisfaction_level))

        # load all the satisfaction choices by class name
        satisfaction = {
            5: self.driver.find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_class_name("Opt1")
        }

        # get the satisfaction choice element
        satisfaction_choice = satisfaction.get(satisfaction_level)

        # click the satisfaction choice element
        satisfaction_choice.click()

        # Select Next
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_order_type(self):
        print("Selecting Order Type...")
        # Select carry out option
        carry_out_element = self.driver.find_element_by_class_name("Opt3").find_element_by_class_name("radioButtonHolder")
        carry_out_element.click()

        # Select Next
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_detailed_satisfaction(self, food_appearance, staff_friendliness, order_accuracy, store_cleanliness, order_speed, order_portion):
        print("Selecting Detailed Experience")
        # Get all elements for all choices
        food_appearance_choices = {
            5: self.driver.find_element_by_id("FNSR011000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR011000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR011000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR011000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR011000").find_element_by_class_name("Opt1")
        }

        friendliness_choices = {
            5: self.driver.find_element_by_id("FNSR010000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR010000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR010000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR010000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR010000").find_element_by_class_name("Opt1")
        }

        accuracy_choices = {
            5: self.driver.find_element_by_id("FNSR008000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR008000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR008000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR008000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR008000").find_element_by_class_name("Opt1")
        }

        cleanliness_choices = {
            5: self.driver.find_element_by_id("FNSR013000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR013000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR013000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR013000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR013000").find_element_by_class_name("Opt1")
        }

        speed_choices = {
            5: self.driver.find_element_by_id("FNSR012000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR012000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR012000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR012000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR012000").find_element_by_class_name("Opt1")
        }

        portion_choices = {
            5: self.driver.find_element_by_id("FNSR007000").find_element_by_class_name("Opt5"),
            4: self.driver.find_element_by_id("FNSR007000").find_element_by_class_name("Opt4"),
            3: self.driver.find_element_by_id("FNSR007000").find_element_by_class_name("Opt3"),
            2: self.driver.find_element_by_id("FNSR007000").find_element_by_class_name("Opt2"),
            1: self.driver.find_element_by_id("FNSR007000").find_element_by_class_name("Opt1")
        }

        # Select all choices
        food_appearance_choice = food_appearance_choices.get(food_appearance)
        food_appearance_choice.click()

        friendliness_choice = friendliness_choices.get(staff_friendliness)
        friendliness_choice.click()

        accuracy_choice = accuracy_choices.get(order_accuracy)
        accuracy_choice.click()

        cleanliness_choice = cleanliness_choices.get(store_cleanliness)
        cleanliness_choice.click()

        speed_choice = speed_choices.get(order_speed)
        speed_choice.click()

        portion_choice = portion_choices.get(order_portion)
        portion_choice.click()

        # Select Next
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()


if __name__ == "__main__":
    survey_code = "2595-5022-2551-2039"

    # Test Opening Survey Page
    survey_taker = SurveyTaker(survey_code)
    survey_taker.open_survey_in_browser()

    # Test Parsing Survey Code
    parsed_code = survey_taker.parse_survey_code()
    print(parsed_code)

    # Test Entering The Survey Code
    survey_taker.enter_survey_code()

    # Test Satisfaction Level Choice
    survey_taker.select_overall_satisfaction_level(5)

    # Test Select Order Type
    survey_taker.select_order_type()

    # Test Detailed Satisfaction level Choices
    survey_taker.select_detailed_satisfaction(5, 3, 5, 5, 4, 5)




