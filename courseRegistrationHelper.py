from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"
TIMEOUT = 10
REGISTRATION_TIMEOUT = 30
IS_AVAILABLE = "text-success"


def login() -> webdriver:
    driver = webdriver.Chrome(PATH)
    driver.get("https://students.technion.ac.il/auth/oidc/")
    driver.maximize_window()

    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys("nimrodshanni@campus.technion.ac.il")
    WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys("TeChyuevje00!")
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    except:
        driver.quit()
    return driver


def get_to_course_page(driver:webdriver, course_number:str) -> None:
    driver.get("https://students.technion.ac.il/local/technionsearch/course/" + course_number)


def get_spans_xpath(driver:webdriver):
    SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[3]/div/div[1]/div/span"
    groups = driver.find_elements(By.XPATH, SPANS_XPATH)
    if len(groups) == 0:
        SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[2]/div/div[1]/div/span"
        groups = driver.find_elements(By.XPATH, SPANS_XPATH)
    return groups, SPANS_XPATH


def is_group_available(driver:webdriver, course_number:str, group_number:str) -> bool:

    get_to_course_page(driver, course_number)
    groups, SPANS_XPATH = get_spans_xpath(driver)
    result = False
    for index in range(len(groups)):
        if driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div").get_attribute("data-group_id") == group_number and driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/div[2]").get_attribute("class") == IS_AVAILABLE:
            result = True
    return result


def checkout_cart(driver:webdriver) -> None:
    driver.get("https://students.technion.ac.il/local/tregister/cart")
    WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "process_cart_item_request"))).click()
    time.sleep(REGISTRATION_TIMEOUT)


def register(driver:webdriver, course_list:list, single_course_registration:bool) -> None:
    try:
        while True:
            for course in course_list:
                course_elements = course.split("-")
                if is_group_available(driver, course_elements[0], course_elements[1]):
                    checkout_cart(driver)
                    if single_course_registration:
                        raise KeyboardInterrupt
                    else:
                        course_list.remove(course)
                        break
        time.sleep(15)
    except KeyboardInterrupt:
        pass

# # version with printing instead of checking out
# def register(driver:webdriver, course_list:list, single_course_registration:bool) -> None:
#     try:
#         while True:
#             for course in course_list:
#                 course_elements = course.split("-")
#                 if is_group_available(driver, course_elements[0], course_elements[1]):
#                     #checkout_cart(driver)
#                     print("registered: " + course)
#                     if single_course_registration:
#                         raise KeyboardInterrupt
#                     else:
#                         course_list.remove(course)
#                         break
#                 else:
#                     print("no room at: " + course)
#             time.sleep(15)
#     except KeyboardInterrupt:
#         pass


def handler(course_list:list, single_course_registration:bool) -> None:
    driver = login()
    register(driver, course_list, single_course_registration)
    driver.quit()