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

driver = None

def login() -> None:
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


def get_to_course_page(course_number:str) -> None:
    driver.get("https://students.technion.ac.il/local/technionsearch/course/" + course_number)


def get_spans_xpath():
    SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[3]/div/div[1]/div/span"
    groups = driver.find_elements(By.XPATH, SPANS_XPATH)
    if len(groups) == 0:
        SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[2]/div/div[1]/div/span"
        groups = driver.find_elements(By.XPATH, SPANS_XPATH)
    return groups, SPANS_XPATH


def is_group_available(course_number:str, group_number:str) -> bool:

    get_to_course_page(course_number)
    groups, SPANS_XPATH = get_spans_xpath()
    result = False
    for index in range(len(groups)):
        if driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div").get_attribute("data-group_id") == group_number and driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/div[2]").get_attribute("class") == IS_AVAILABLE:
            result = True
    return result


def checkout_cart() -> None:
    driver.get("https://students.technion.ac.il/local/tregister/cart")
    WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.ID, "process_cart_item_request"))).click()
    time.sleep(REGISTRATION_TIMEOUT)


def register(course_list:list, single_course_registration:bool) -> None:
    try:
        while True:
            for course in course_list:
                course_elements = course.split("-")
                if is_group_available(course_elements[0], course_elements[1]):
                    checkout_cart()
                    if single_course_registration:
                        raise KeyboardInterrupt
                    else:
                        course_list.remove(course)
                        break
    except KeyboardInterrupt:
        pass
