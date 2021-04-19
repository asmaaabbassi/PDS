#!/usr/bin/env python
# coding: utf-8

# In[44]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.investing.com/indices/usdollar")

element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
python_button = driver.find_elements_by_xpath('//*[@id="onetrust-accept-btn-handler"]')[0]
python_button.click()

driver.execute_script("window.scrollTo(0, 200)")
driver.find_element_by_link_text("Historical Data").click()

driver.find_element_by_link_text("Sign In").click()

mail = driver.find_elements_by_xpath('//*[@id="loginFormUser_email"]')[0]
mail.click()
mail.clear()
mail.send_keys('thomas.monnier@mines-paristech.fr')

password = driver.find_elements_by_xpath('//*[@id="loginForm_password"]')[0]
password.click()
password.clear()
password.send_keys('Project2021!')

password.send_keys(Keys.ENTER)


driver.execute_script("window.scrollTo(0, 500)")

python_span = driver.find_elements_by_xpath('//*[@id="datePickerIconWrap"]/span')[1]
python_span.click()

begin_date = driver.find_elements_by_xpath('//*[@id="startDate"]')[0]
begin_date.click()
begin_date.clear()
begin_date.send_keys('01/01/2020')

end_date = driver.find_elements_by_xpath('//*[@id="endDate"]')[0]
end_date.click()
end_date.clear()
end_date.send_keys('12/31/2020')

driver.find_element_by_link_text("Apply").click()

driver.find_element_by_link_text("Download Data").click()


#driver.close()


# In[ ]:




