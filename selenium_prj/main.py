from selenium.webdriver import Chrome
import time
# import os

driver = Chrome("./chromedriver")

# open url
driver.get("https://www.youtube.com/view_all_playlists")

# gmail           = ""
# google_password = ""

# bs4.find --> find_element
# bs4.find_all --> find_elements
driver.find_element_by_id("identifierId").send_keys(gmail)
time.sleep(3)  # wait 3 sec
driver.find_element_by_id("identifierNext").click()
time.sleep(1)  # wait 1 sec
driver.find_element_by_class_name("shs0nd").send_keys(google_password)
time.sleep(1)  # wait 1 sec
driver.find_element_by_id("identifierNextsswordNext").click()
time.sleep(5)  # wait 5 sec


print("Done")
