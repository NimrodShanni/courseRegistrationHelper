from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import messagebox

class Gui:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("535x370")
        self.root.title("Registration Helper")

        self.helper = None
        self.driver = None

        self.email_label = tk.Label(self.root, text = "Email:", font = ("Calibri", 14))
        self.email_label.place(x = 10, y = 10)
        self.password_label = tk.Label(self.root, text = "Password:", font = ("Calibri", 14))
        self.password_label.place(x = 10, y = 56)
        self.enter_courses_label = tk.Label(self.root, text = "Enter wanted courses in the following format -", font = ("Calibri", 14))
        self.enter_courses_label.place(x = 10, y = 120)
        self.courses_example_label = tk.Label(self.root, text = '"234124-13, 394804-18, 114804-12, ..."', font = ("Calibri", 12))
        self.courses_example_label.place(x = 10, y = 150)
        self.entered_courses_label = tk.Label(self.root, text = "Selected courses:", font = ("Calibri", 12))
        self.entered_courses_label.place(x = 10, y = 220)
        self.entered_courses_dynamic_label = tk.Label(self.root, text = "None", fg = "red", font = ("Calibri", 12))
        self.entered_courses_dynamic_label.place(x = 135, y = 220)
        self.status_label = tk.Label(self.root, text = "Status:", font = ("Calibri", 12))
        self.status_label.place(x = 10, y = 300)
        self.status_dynamic_label = tk.Label(self.root, text = "Standby", fg = "red", font = ("Calibri", 12))
        self.status_dynamic_label.place(x = 62, y = 300)
        self.form_split1_label = tk.Label(self.root, text = "----------------------------------------------------------------------------------------------------------", font = ("Calibri", 12))
        self.form_split1_label.place(x = -1, y = 97)
        self.form_split2_label = tk.Label(self.root, text = "----------------------------------------------------------------------------------------------------------", font = ("Calibri", 12))
        self.form_split2_label.place(x = -1, y = 240)

        self.user_name_entry = tk.Entry(self.root, width = 40, font = ("Calibri", 14))
        self.user_name_entry.place(x = 105, y = 10)
        self.user_name_entry.focus()
        self.password_entry = tk.Entry(self.root, width = 27, show = "*", font = ("Calibri", 14))
        self.password_entry.place(x = 105, y = 56)
        self.courses_entry = tk.Entry(self.root, width = 45, font = ("Calibri", 12))
        self.courses_entry.place(x = 10, y = 185)

        self.login_button = tk.Button(self.root, text = "Login", bd = 3, font = ("Calibri", 14), command = self.login_click)
        self.login_button.place(x = 455, y = 50)
        self.login_clear_button = tk.Button(self.root, text = "Clear", bd = 3, font = ("Calibri", 14), command = self.login_clear_click)
        self.login_clear_button.place(x = 395, y = 50)
        self.enter_courses_button = tk.Button(self.root, text = "Enter courses", bd = 3, font = ("Calibri", 12), command = self.enter_courses_click)
        self.enter_courses_button.place(x = 429, y = 180)
        self.courses_clear_button = tk.Button(self.root, text = "Clear", bd = 3, font = ("Calibri", 12), command = self.courses_clear_click)
        self.courses_clear_button.place(x = 379, y = 180)
        self.start_button = tk.Button(self.root, text = "Start", fg = "green", width = 8, bd = 5, font = ("Calibri", 16), command = self.start_click)
        self.start_button.place(x = 315, y = 285)
        self.stop_button = tk.Button(self.root, text = "Stop", fg = "red", width = 8, bd = 5, font = ("Calibri", 16), command = self.stop_click)
        self.stop_button.place(x = 420, y = 285)

        self.root.after(200, self.register_handler)
        self.root.mainloop()
        
    def login_click(self):
        email = self.user_name_entry.get()
        password = self.password_entry.get()
        if email != "" and password != "":
            self.helper = Helper(email, password)
            self.driver = self.helper.driver
        else:
            messagebox.showinfo(title = "Error", message = "Invalid login")

    def login_clear_click(self):
        self.user_name_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def enter_courses_click(self):
        if self.helper is not None:
            self.helper.course_list = self.courses_entry.get().split(", ")
            if self.helper.course_list == [""]:
                self.entered_courses_dynamic_label["fg"] = "red"
                self.entered_courses_dynamic_label["text"] = "None"
            else:
                self.entered_courses_dynamic_label["fg"] = "green"
                self.entered_courses_dynamic_label["text"] = ", ".join(self.helper.course_list)
        else:
            messagebox.showinfo(title = "Error", message = "Login first")

    def courses_clear_click(self):
        self.courses_entry.delete(0, tk.END)

    def register_handler(self):
        if self.helper is not None:
            if self.helper.enable:
                self.helper.register()
        self.root.after(10000, self.register_handler)

    def start_click(self):
        if self.helper is not None:
            self.status_dynamic_label["text"] = "Running"
            self.status_dynamic_label["fg"] = "green"
            self.helper.enable = True
        else:
            messagebox.showinfo(title = "Error", message = "driver is not running")

    def stop_click(self):
        if self.helper is not None:
            self.status_dynamic_label["text"] = "Standby"
            self.status_dynamic_label["fg"] = "red"
            self.helper.enable = False
        else:
            messagebox.showinfo(title = "Error", message = "driver is not running")


class Helper:
    def __init__(self, email:str, password:str):
        self.driver = None
        self.enable = False
        self.course_list = [""]
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.TIMEOUT = 10
        self.REGISTRATION_TIMEOUT = 30
        self.IS_AVAILABLE = "text-success"
        self.login(email, password)

    def login(self, email:str, password:str) -> None:
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://students.technion.ac.il/auth/oidc/")
        self.driver.maximize_window()

        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(email)
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(password)
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        except:
            self.driver.quit()


    def get_to_course_page(self, course_number:str) -> None:
        self.driver.get("https://students.technion.ac.il/local/technionsearch/course/" + course_number)


    def get_spans_xpath(self):
        SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[3]/div/div[1]/div/span"
        groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        if len(groups) == 0:
            SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[2]/div/div[1]/div/span"
            groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        return groups, SPANS_XPATH
    

    def is_group_available(self, course_number:str, group_number:str) -> bool:
        Helper.get_to_course_page(self, course_number)
        groups, SPANS_XPATH = Helper.get_spans_xpath(self)
        result = False
        for index in range(len(groups)):
            if self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div").get_attribute("data-group_id") == group_number and self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/div[2]").get_attribute("class") == self.IS_AVAILABLE:
                result = True
        return result


    def checkout_cart(self) -> None:
        self.driver.get("https://students.technion.ac.il/local/tregister/cart")
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "process_cart_item_request"))).click()
        time.sleep(self.REGISTRATION_TIMEOUT)



    # # release version
    # def register(self, single_course_registration:bool) -> None:
    #     for course in self.course_list:
    #         course_elements = course.split("-")
    #         if Helper().is_group_available(self, course_elements[0], course_elements[1]):
    #             Helper().checkout_cart(self)
    #             if single_course_registration:
    #                 self.enable = False
    #             else:
    #                 self.course_list.remove(course)
    #                 break


    # version with printing instead of checking out
    def register(self, single_course_registration:bool = True) -> None:
        for course in self.course_list:
            course_elements = course.split("-")
            if Helper.is_group_available(self, course_elements[0], course_elements[1]):
                print("registered: " + course)
                if single_course_registration:
                    self.enable = False
                else:
                    self.course_list.remove(course)
                    break
            else:
                print("no room at: " + course)



#------------main------------
Gui()