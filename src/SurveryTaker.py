import time
from datetime import datetime
from random import Random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SurveyTaker:

    survey_url = "https://tellthebell.com/Index.aspx?Page=1"
    driver = None

    def __init__(self, code):
        #initialize survey code
        self.survey_code = code

        # create randomizer object and give unique seed
        self.random = Random()
        self.random.seed(datetime.now())

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
                exit(0)
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
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_order_type(self):
        print("Selecting Order Type...")
        # Select carry out option
        try:
            carry_out_element = self.driver.find_element_by_class_name("Opt3").find_element_by_class_name("radioButtonHolder")
            carry_out_element.click()

            # Select Next
            print("Selecting Next...")
            next_button = self.driver.find_element_by_id("NextButton")
            next_button.click()
        except NoSuchElementException:
            print("Order type selection not visible")

    def select_detailed_satisfaction(self):
        print("Selecting Detailed Experience...")
        # Get all elements for all choices
        max_scores = self.driver.find_elements_by_class_name("Opt5")

        for element in max_scores:
            element.click()

        # Select Next
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_experienced_problem(self):
        print("Selecting Experienced Problem Selection....")
        # Select no problems experienced
        no_option = self.driver.find_element_by_class_name("Opt2")
        no_option.click()

        # Select Next Button
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def leave_feedback_description(self):
        print("Leaving Feedback Description...")
        # get the text area element and clear it
        text_area = self.driver.find_element_by_id("S081000")
        text_area.clear()

        with open("C:/Users/Omar/PycharmProjects/YoQuieroSurvey/src/highly_satisfied_responses.txt", 'r',
                  encoding='utf-8') as fp:
            possible_feedback = fp.readlines()
            fp.close()

        # type the random message
        text_area.send_keys(self.random.choice(possible_feedback))

    def enter_highly_satisfied_details(self):
        print("Deciding if feedback description should be left...")

        # generate a random number
        random_number = self.random.randint(0, 100)

        # if random number is higher than 80 leave a feedback message
        if random_number >= 80:
            print("Leaving Feedback...")
            self.leave_feedback_description()
        else:
            print("Not Leaving Feedback...")

        # Select Next
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_recognize_team_member(self, choice, team_member=None):
        print("Selecting Recognize Team Member Choice...")

        # Select whether or not to recognize a team member
        if choice is True:
            print("Selecting YES, recognize team member...")
            if team_member is None:
                self.select_recognize_team_member(False)
            else:
                yes_choice = self.driver.find_element_by_class_name("Opt1")
                yes_choice.click()

                # Select Next
                print("Selecting Next...")
                next_button = self.driver.find_element_by_id("NextButton")
                next_button.click()

                # Enter team member information
                self.recognize_team_member(team_member)

        else:
            print("Selecting NO, don't recognize team member...")
            no_choice = self.driver.find_element_by_class_name("Opt2")
            no_choice.click()

            # Select Next
            print("Selecting Next...")
            next_button = self.driver.find_element_by_id("NextButton")
            next_button.click()

    def recognize_team_member(self, team_member):
        print("Entering Team Member Recognition Information...")
        # get the text line for entering the team member and clear it
        text_line = self.driver.find_element_by_id("S081001")
        text_line.clear()

        # enter the team member name
        text_line.send_keys(team_member)

        # get the text area element and clear it
        text_area = self.driver.find_element_by_id("S081002")
        text_area.clear()

        # get the random feedback for team member
        with open("C:/Users/Omar/PycharmProjects/YoQuieroSurvey/src/team_member_satisfaction_response.txt", 'r',
                  encoding='utf-8') as fp:
            possible_feedback = fp.readlines()
            fp.close()

        # type the random message
        feedback = self.random.choice(possible_feedback)

        # replace filler text with actual name
        if "{member}" in feedback:
            feedback = str(feedback).replace("{member}", team_member)

        # enter the feedback
        text_area.send_keys(feedback)

        # Select Next
        time.sleep(10)
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_taco_visual_options(self):
        print("Selecting Taco Visual Options...")
        # Select Yes
        yes = self.driver.find_element_by_class_name("Opt1").find_element_by_class_name("radioButtonHolder")
        yes.click()

        # Select Next
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def select_hard_shell_purchased(self, was_purchased):
        print("Selecting Hard Shell Purchased Option...")
        yes = self.driver.find_element_by_class_name("Opt1")
        no = self.driver.find_element_by_class_name("Opt2")

        if was_purchased:
            print("Selecting Yes...")
            # Select Yes
            yes.click()

            # Select Next
            print("Selecting Next...")
            next_button = self.driver.find_element_by_id("NextButton")
            next_button.click()
            self.select_taco_visual_options()
        else:
            print("Selecting No...")
            # Select No
            no.click()

            # Select Next
            print("Selecting Next...")
            next_button = self.driver.find_element_by_id("NextButton")
            next_button.click()

    def select_enter_sweepstakes(self):
        print("Declining Sweepstakes Entrance...")

        # Select No
        no = self.driver.find_element_by_class_name("Opt2").find_element_by_class_name("radioSimpleInput")
        no.click()

        # Select Next
        print("Selecting Next...")
        next_button = self.driver.find_element_by_id("NextButton")
        next_button.click()

    def check_success(self):
        try:
            finished = self.driver.find_elements_by_xpath("//*[contains(text(), 'Thank You!')]")
            if finished:
                return "SUCCESSFUL"
        except NoSuchElementException:
            return "UNSUCCESSFUL"


if __name__ == "__main__":
    # survey_code = input("Enter a survey code: ")
    survey_code = "2196503228542109"

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
    survey_taker.select_detailed_satisfaction()

    # Test experienced problem choice
    survey_taker.select_experienced_problem()

    # Test enter feedback description if successful roll
    survey_taker.enter_highly_satisfied_details()

    # Test Recognize Team Member
    survey_taker.select_recognize_team_member(True, "Xavier")

    # Test Hard Shell Purchased
    survey_taker.select_hard_shell_purchased(True)

    # Test Sweepstakes Option
    survey_taker.select_enter_sweepstakes()

    # Test Success
    success = survey_taker.check_success()
    print("Survey Was: " + success)



