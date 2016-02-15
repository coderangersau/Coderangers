import csv

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

STEPS = (
        ('username', 'password', 'password-confirm'),
        (('select', 'birthyear'), ('select', 'birthmonth'), ('select', 'country')),
        ('email', 'email-confirm'),
)

driver = webdriver.Firefox()

def create_account(username, password, **fields):
    try:
        fields['username'] = username
        fields['password'] = password
        fields['password-confirm'] = fields['password']
        fields['country'] = 'Australia'
        fields.setdefault('birthmonth', 'January')
        fields.setdefault('birthyear', '2004')
        fields.setdefault('email', 'info@coderangers.com.au')
        fields['email-confirm'] = fields['email']
        while driver.execute_script("return document.readyState") != 'complete':
            pass  # avoid loading the new registration before the old submit is complete
        time.sleep(2)  # MAY NEED TO CHANGE THIS NUMBER IF IT ISN'T GOING THROUGH
        driver.get("https://scratch.mit.edu/accounts/standalone-registration")

        for i, form in enumerate(STEPS):
            if i == 1:
                driver.find_element_by_id('gender_other_radio').click()
                driver.find_element_by_id('gender_other_text').send_keys('Other')
            for field in form:
                css = ('%s[name=%s' if isinstance(field, tuple) else 'input[name=%s]') % field
                if isinstance(field, tuple): field = field[1]
                print("filling", css, "with", fields[field])
                element = WebDriverWait(driver, 5).until(
                    expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css))
                )
                element.send_keys(fields[field])
            driver.find_element_by_id('registration-next').click()
        print('Created username {}, password {} with fields {}'.format(username, password, fields))
        return True
    except Exception:
        print('Scratch account for username {} and password {} with fields {} failed'.format(username, password, fields))
        return False