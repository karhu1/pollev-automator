from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

driver = webdriver.Chrome()
driver.get("https://pollev.com/lauramcg")
# assert "Python" in driver.title

print('starting to go through UW login...\n')

time.sleep(1)

register = driver.find_element("css selector", '.mt-8.mdc-button.mdc-button--outlined')
register.click()

time.sleep(0.5)

username = driver.find_element(By.ID, 'username')
username.send_keys('rasmus1@uw.edu')

time.sleep(0.5)

next = driver.find_element(By.CLASS_NAME, 'mdc-button')
next.click()

time.sleep(0.5)

uw_btn = driver.find_element(By.CLASS_NAME, 'mdc-button')
uw_btn.click()

time.sleep(1)

print('inputting username and password...\n')

netid = driver.find_element(By.ID, 'weblogin_netid')
netid.send_keys('rasmus1')

with open('./secret/secret_password.txt', 'r') as file:
  secret_password = file.read()

password = driver.find_element(By.ID, 'weblogin_password')
password.send_keys(secret_password)

submit = driver.find_element(By.ID, 'submit_button')
submit.click()

print('waiting for DUO authentication...\n')
trust = driver.find_elements(By.ID, 'trust-browser-button')

while not trust:
  time.sleep(1)
  trust = driver.find_elements(By.ID, 'trust-browser-button')

print('got DUO authentication!\n')
trust[0].click()

time.sleep(5)

print('going back to right pollEv site...\n')

driver.get("https://pollev.com/lauramcg")

time.sleep(5)

# AT THIS POINT WE HAVE LOGGED IN.

# NOW HOW DO WE LISTEN FOR CHANGES?

print('running scripts...\n')

driver.execute_script("""
  window.changeLog = [];
  const target = document.querySelector('#participate_presenter_lauramcg');

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      window.changeLog.push(mutation.target.textContent);
    });
  });

  observer.observe(target, { childList: true, subtree: true, characterData: true });

""")

def fetch_changes():
  changes = driver.execute_script("""
    const changes = window.changeLog.slice();
    window.changeLog = [];
    return changes;
  """)
  return changes

print('starting to fetch for changes!\n')

# Example loop
while True:
  changes = fetch_changes()
  if changes:
    # print("DOM changed:", change)
    time.sleep(0.5)
    buttons = driver.find_elements(By.CLASS_NAME, 'component-response-multiple-choice__option__vote')
    if buttons:
      buttons[random.randint(0, len(buttons)-1)].click()
  time.sleep(2)

driver.close()