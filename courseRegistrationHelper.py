from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import tkinter as tk
from tkinter import messagebox

class HelperGui:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("535x495")
        self.root.title("Registration Helper")

        self.helper = None
        self.driver = None
        self.radio_variable = tk.StringVar()
        self.replacement_course = ""
        self.DEFAULT_FREQUENCY = 90
        self.frequency = 1

        self.email_label = tk.Label(self.root, text = "Email:", font = ("Calibri", 14))
        self.email_label.place(x = 10, y = 10)
        self.password_label = tk.Label(self.root, text = "Password:", font = ("Calibri", 14))
        self.password_label.place(x = 10, y = 56)
        self.enter_courses_label = tk.Label(self.root, text = "Enter wanted courses -", font = ("Calibri", 16))
        self.enter_courses_label.place(x = 10, y = 280)
        self.entered_courses_label = tk.Label(self.root, text = "Selected courses:", font = ("Calibri", 12))
        self.entered_courses_label.place(x = 10, y = 360)
        self.entered_courses_dynamic_label = tk.Label(self.root, text = "None", fg = "red", font = ("Calibri", 12))
        self.entered_courses_dynamic_label.place(x = 132, y = 360)
        self.replacement_course_dynamic_label = tk.Label(self.root, fg = "green", font = ("Calibri", 12))
        self.status_label = tk.Label(self.root, text = "Status:", font = ("Calibri", 14))
        self.status_label.place(x = 10, y = 454)
        self.status_dynamic_label = tk.Label(self.root, text = "Standby", fg = "red", font = ("Calibri", 14))
        self.status_dynamic_label.place(x = 72, y = 454)
        self.operation_mode_label = tk.Label(self.root, text = "Operation mode:", font = ("Calibri", 16))
        self.operation_mode_label.place(x = 10, y = 120)
        self.operating_frequency_label = tk.Label(self.root, text = "Operating frequency:", font = ("Calibri", 14))
        self.operating_frequency_label.place(x = 10, y = 420)
        self.operating_frequency_seconds_label = tk.Label(self.root, text = "seconds.", font = ("Calibri", 14))
        self.operating_frequency_seconds_label.place(x = 220, y = 420)
        self.form_split1_label = tk.Label(self.root, text = "----------------------------------------------------------------------------------------------------------", font = ("Calibri", 12))
        self.form_split1_label.place(x = -1, y = 97)
        self.form_split2_label = tk.Label(self.root, text = "----------------------------------------------------------------------------------------------------------", font = ("Calibri", 12))
        self.form_split2_label.place(x = -1, y = 250)
        self.form_split3_label = tk.Label(self.root, text = "----------------------------------------------------------------------------------------------------------", font = ("Calibri", 12))
        self.form_split3_label.place(x = -1, y = 390)

        self.user_name_entry = tk.Entry(self.root, width = 40, font = ("Calibri", 14))
        self.user_name_entry.place(x = 105, y = 10)
        self.user_name_entry.focus()
        self.password_entry = tk.Entry(self.root, width = 27, show = "*", font = ("Calibri", 14))
        self.password_entry.place(x = 105, y = 56)
        self.courses_entry = tk.Entry(self.root, width = 45, fg = "grey", font = ("Calibri", 12))
        self.courses_entry.insert(0, '"234124-13, 394804-18, 114804-12, ..."')
        self.courses_entry.place(x = 10, y = 325)
        self.replace_course_entry = tk.Entry(self.root, width = 15, fg = "grey", font = ("Calibri", 12))
        self.replace_course_entry.insert(0, '"234124-19"')
        self.replace_course_entry.place(x = 170, y = 218)
        self.frequency_entry = tk.Entry(self.root, width = 3,font = ("Calibri", 12))
        self.frequency_entry.place(x = 187, y = 423)
        self.frequency_entry.insert(0, self.DEFAULT_FREQUENCY)

        self.login_button = tk.Button(self.root, text = "Login", bd = 3, font = ("Calibri", 14), command = self.login_click)
        self.login_button.place(x = 455, y = 50)
        self.login_clear_button = tk.Button(self.root, text = "Clear", bd = 3, font = ("Calibri", 14), command = self.login_clear_click)
        self.login_clear_button.place(x = 395, y = 50)
        self.enter_courses_button = tk.Button(self.root, text = "Enter courses", bd = 3, font = ("Calibri", 12), command = self.enter_courses_click)
        self.enter_courses_button.place(x = 429, y = 320)
        self.courses_clear_button = tk.Button(self.root, text = "Clear", bd = 3, font = ("Calibri", 12), command = self.courses_clear_click)
        self.courses_clear_button.place(x = 379, y = 320)
        self.replacement_enter_button = tk.Button(self.root, text = "Enter", bd = 3, font = ("Calibri", 12), command = self.replacement_enter_click)
        self.replacement_enter_button.place(x = 352, y = 214)
        self.replacement_clear_button = tk.Button(self.root, text = "Clear", bd = 3, font = ("Calibri", 12), command = self.replacement_clear_click)
        self.replacement_clear_button.place(x = 300, y = 214)
        self.start_button = tk.Button(self.root, text = "Start", fg = "green", width = 8, bd = 5, font = ("Calibri", 16), command = self.start_click)
        self.start_button.place(x = 420, y = 422)
        self.stop_button = tk.Button(self.root, text = "Stop", fg = "red", width = 8, bd = 5, font = ("Calibri", 16), command = self.stop_click)
        self.stop_button.place(x = 315, y = 422)

        self.add_course_radio = tk.Radiobutton(self.root, text = "Add single course", font = ("Calibri", 14), variable = self.radio_variable, value = "add_single_course")
        self.add_course_radio.place(x = 10, y = 150)
        self.add_course_radio.select()
        self.add_courses_radio = tk.Radiobutton(self.root, text = "Add multiple courses", font = ("Calibri", 14), variable = self.radio_variable, value = "add_multiple_courses")
        self.add_courses_radio.place(x = 10, y = 180)
        self.replace_course_radio = tk.Radiobutton(self.root, text = "Replace course:", font = ("Calibri", 14), variable = self.radio_variable, value = "replace_course")
        self.replace_course_radio.place(x = 10, y = 210)

        self.courses_entry.bind("<FocusIn>", self.handle_courses_entry_focus_in)
        self.courses_entry.bind("<FocusOut>", self.handle_courses_entry_focus_out)
        self.replace_course_entry.bind("<FocusIn>", self.handle_replace_course_entry_focus_in)
        self.replace_course_entry.bind("<FocusOut>", self.handle_replace_course_entry_focus_out)
        self.root.after(200, self.register_handler)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        if self.courses_entry["fg"] != "grey":
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
        if self.courses_entry["fg"] != "grey":
            self.courses_entry.delete(0, tk.END)

    def register_handler(self):
        if self.helper is not None:
            if self.helper.enable:
                self.helper.register(self.radio_variable.get(), self.replace_course_entry.get())
            else:
                self.status_dynamic_label["text"] = "Standby" #
                self.status_dynamic_label["fg"] = "red"       # when all registrations are completed
        self.root.after(int(self.frequency)*1000, self.register_handler)

    def start_click(self):
        if self.helper is not None:
            self.status_dynamic_label["text"] = "Running"
            self.status_dynamic_label["fg"] = "green"
            if self.frequency_entry.get() == "":
                self.frequency_entry.insert(0, self.DEFAULT_FREQUENCY)
            self.frequency = int(self.frequency_entry.get())
            self.helper.enable = True
        else:
            messagebox.showinfo(title = "Error", message = "Driver is not running")

    def stop_click(self):
        if self.helper is not None:
            self.status_dynamic_label["text"] = "Standby"
            self.status_dynamic_label["fg"] = "red"
            self.helper.enable = False
        else:
            messagebox.showinfo(title = "Error", message = "Driver is not running")

    def on_closing(self):
        if self.helper is not None:
            self.helper.driver.quit()
        self.root.destroy()

    def replacement_enter_click(self):
        if self.replace_course_entry["fg"] != "grey":
            self.replacement_course = self.replace_course_entry.get()
            if self.replacement_course != "":
                self.replacement_course_dynamic_label["text"] = "Set: " + self.replacement_course
                self.replacement_course_dynamic_label.place(x = 406, y = 217)

    def replacement_clear_click(self):
        self.replace_course_entry.delete(0, tk.END)
        self.replacement_course = ""
        self.replacement_course_dynamic_label.place_forget()

    def handle_courses_entry_focus_in(self, event = None):
        if self.courses_entry.get() == '"234124-13, 394804-18, 114804-12, ..."':
            self.courses_entry.delete(0, tk.END)
            self.courses_entry["fg"] = "black"

    def handle_courses_entry_focus_out(self, event = None):
        if self.courses_entry.get() == "":
            self.courses_entry.delete(0, tk.END)
            self.courses_entry["fg"] = "grey"
            self.courses_entry.insert(0, '"234124-13, 394804-18, 114804-12, ..."')

    def handle_replace_course_entry_focus_in(self, event = None):
        if self.replace_course_entry.get() == '"234124-19"':
            self.replace_course_entry.delete(0, tk.END)
            self.replace_course_entry["fg"] = "black"

    def handle_replace_course_entry_focus_out(self, event = None):
        if self.replace_course_entry.get() == "":
            self.replace_course_entry.delete(0, tk.END)
            self.replace_course_entry["fg"] = "grey"
            self.replace_course_entry.insert(0, '"234124-19"')


class Helper:
    def __init__(self, email:str, password:str):
        self.driver = None
        self.enable = False
        self.course_list = [""]
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.TIMEOUT = 10
        self.REGISTRATION_TIMEOUT = 20
        self.IS_AVAILABLE = "text-success"
        self.login(email, password)
        self.action = ActionChains(self.driver)

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

    def get_spans_xpath(self) -> tuple[list,str]:
        SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[3]/div/div[1]/div/span"
        groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        if len(groups) == 0:
            SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[2]/div/div[1]/div/span"
            groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        return groups, SPANS_XPATH
    
    def is_group_available(self, course_number:str, group_number:str) -> bool:
        self.driver.get("https://students.technion.ac.il/local/technionsearch/course/" + course_number)
        groups, SPANS_XPATH = self.get_spans_xpath()
        result = False
        for index in range(len(groups)):
            if self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div").get_attribute("data-group_id") == group_number and self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/div[2]").get_attribute("class") == self.IS_AVAILABLE:
                result = True
        return result

    def checkout_cart(self) -> None:
        required_url = "https://students.technion.ac.il/local/tregister/cart"
        if self.driver.current_url != required_url:
            self.driver.get(required_url)
        self.action.double_click(WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "process_cart_item_request")))).perform()
        time.sleep(self.REGISTRATION_TIMEOUT)

    def add_to_cart(self, course_number:str, group_number:str) -> None:
        required_url = "https://students.technion.ac.il/local/tregister/cart"
        if self.driver.current_url != required_url:
            self.driver.get(required_url)
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, "id_course_id"))).send_keys(course_number)
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, "id_group_id"))).send_keys(group_number)
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.ID, "id_submitbutton"))).click()

    def remove_course(self, course:str) -> None:
        required_url = "https://students.technion.ac.il/local/tregister/cart"
        if self.driver.current_url != required_url:
            self.driver.get(required_url)
        COURSES_XPATH_PREFIX = "/html/body/div[2]/div[3]/div/div/section/div/ul[2]/li"
        COURSES_XPATH_SUFFIX = "/div/div/div[4]/div/a"
        existing_courses = self.driver.find_elements(By.XPATH, COURSES_XPATH_PREFIX)
        for index in range(len(existing_courses)):
            elem = self.driver.find_element(By.XPATH, COURSES_XPATH_PREFIX + "[" + str(index+1) + "]" + COURSES_XPATH_SUFFIX)
            if elem.get_attribute("data-course_id") == course.split("-")[0] and elem.get_attribute("data-group_id") == course.split("-")[1]:
                self.action.double_click(WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, COURSES_XPATH_PREFIX + "[" + str(index+1) + "]" + COURSES_XPATH_SUFFIX)))).perform()

    def register(self, operation_mode:str, course_for_removal:str) -> None:
        for course in self.course_list:
            if len(self.course_list) > 0:
                course_elements = course.split("-")
                if self.is_group_available(course_elements[0], course_elements[1]):
                    if operation_mode == "replace_course":
                        self.remove_course(course_for_removal)
                    self.add_to_cart(course_elements[0], course_elements[1])
                    self.checkout_cart()
                    if operation_mode == "add_single_course" or operation_mode == "replace_course":
                        self.enable = False
                        break
                    elif operation_mode == "add_multiple_courses":
                        self.course_list.remove(course)
                        break
            else:
                self.enable = False


#------------main------------
HelperGui()