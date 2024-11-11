from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
# Create a web driver instance
driver = webdriver.Chrome()

driver.get("https://mot-thyag.github.io/")

time.sleep(2)

# Find the textarea element
textarea = driver.find_element(By.ID, "flows_in")

# Clear existing text (optional)
textarea.clear()

# Send text to the textarea
textarea.send_keys("""
Wages [1500] Budget
Other [250] Budget
Budget [450] Taxes
Budget [420] Housing
Budget [400] Food
Budget [295] Transportation \\n more sample text \\n caption test
Budget [25] Savings \\n Sample Text
Budget [160] Other Necessities #0F0
                   """)

time.sleep(2)


# Find and interact with elements
save_as_svg = driver.find_element(By.ID, "save_as_svg")
save_as_png_2x = driver.find_element(By.ID, "save_as_png_2x")
save_as_svg.click()
save_as_png_2x.click()

time.sleep(2)

# Close the browser
driver.close()