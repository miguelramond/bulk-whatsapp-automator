# Program to send bulk customized message through WhatsApp web application

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pandas
import time

# Load the chrome driver
driver = webdriver.Chrome()
count = 0

# Create variable to track amount of contacts actually messaged
validcontactcount = 0

# Open WhatsApp URL in chrome browser
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 120)

# Read data from excel
excel_data = pandas.read_excel('Customer bulk email data.xls', sheet_name='Customers')

# Iterate excel rows till to finish
for column in excel_data['Name'].tolist():
    # Debug print to console
    # print("Starting loop " + (str(count + 1)))

    # Assign customized message
    message = excel_data['Message'][0]

    # Wait for 2 seconds to allow xpath to be found when phone number
    # is not found and must be cleared
    time.sleep(2)

    # OLD XPATH THAT DOESNT WORK ANYMORE THAT WAS IN SEARCH_BOX VARIABLE
    # '//*[@id="side"]/div[1]/div/label/div/div[2]'

    # Locate search box through x_path
    search_box = '/html/body/div[1]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[2]'
    person_title = wait.until(lambda driver: driver.find_element(by=By.XPATH, value=search_box))

    # Clear search box if any contact number is written in it
    person_title.clear()

    # Send contact number in search box
    person_title.send_keys(str(excel_data['Contact'][count]))
    count = count + 1

    # Wait for 3 seconds to search contact number
    time.sleep(3)

    try:
        # Load error message in case unavailability of contact number
        element = driver.find_element(by=By.XPATH, value='//*[@id="pane-side"]/div[1]/div/span')
    except NoSuchElementException:
        # Format the message from excel sheet
        message = message.replace('{customer_name}', column)

        # Add to count in case contact exists and is about to be messaged
        validcontactcount = validcontactcount + 1

        # Press ENTER in search bar in order to enter to found contact chat
        person_title.send_keys(Keys.ENTER)

        # Webdriver wait until whatsapp web exits search results (And enters chat)
        # XPATH here provided is that of the second contact in chat list, which
        # only appears when ENTER is recieved in search bar
        # (thus opening chat and exiting search results)
        searchkeysconfirmation = wait.until(lambda driver: driver.find_element(by=By.XPATH, value='//*[@id="pane-side"]/div[1]/div/div/div[2]'))

        # Additional check only for first contact: Wait until header appears
        # XPATH here is that of the header where contact name, avatar etc appears
        # (Which otherwise is not visible on page load until you enter a chat)
        if validcontactcount == 1:
            firstavatar = wait.until(lambda driver: driver.find_element(by=By.XPATH, value='//*[@id="main"]/header'))

        # Avatar check for further verification of correct chat
        # This IF is entered when contact is an odd number, then stores the avatar URL for checking
        if (validcontactcount % 2) == 1:
            try:
                firstavatar = driver.find_element(by=By.XPATH, value='//*[@id="main"]/header/div[1]/div/img').get_attribute('src')
            except NoSuchElementException:
                # Assign null in case contact has no avatar and just a plan SVG
                firstavatar = 'null'

            # Loop for checking avatar BUT ONLY IF IT'S NOT THE FIRST CONTACT THAT IS BEING MESSAGED
            if validcontactcount != 1:
                # Variable to track 'driver.find_element' tries to break loop in case something breaks
                avatartryticker = 0
                while firstavatar == secondavatar:
                    # Add count to try ticker
                    avatartryticker = avatartryticker + 1

                    # Wait 1 second for buffering just in case
                    time.sleep(1)
                    try:
                        firstavatar = driver.find_element(by=By.XPATH,
                                                           value='//*[@id="main"]/header/div[1]/div/img').get_attribute(
                            'src')
                    except NoSuchElementException:
                        # Assign null in case contact has no avatar and just a plan SVG
                        firstavatar = 'null'
                    if avatartryticker >= 10:
                        break

        # Same above only that this is entered in case counter is on an even number
        # TODO: Make this and above IF into a single function
        if (validcontactcount % 2) == 0:
            try:
                secondavatar = driver.find_element(by=By.XPATH, value='//*[@id="main"]/header/div[1]/div/img').get_attribute('src')
            except NoSuchElementException:
                secondavatar = 'null'

            avatartryticker = 0

            while secondavatar == firstavatar:
                avatartryticker = avatartryticker + 1
                time.sleep(1)
                try:
                    secondavatar = driver.find_element(by=By.XPATH, value='//*[@id="main"]/header/div[1]/div/img').get_attribute('src')
                except NoSuchElementException:
                    secondavatar = 'null'
                if avatartryticker >= 10:
                    break

        # Write and send message
        actions = ActionChains(driver)
        actions.send_keys(message)
        actions.send_keys(Keys.ENTER)
        actions.perform()

# Wait 60 Seconds before shutdown to send final messages
time.sleep(60)

# Close chrome browser
driver.quit()
