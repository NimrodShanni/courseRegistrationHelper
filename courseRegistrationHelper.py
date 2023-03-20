from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import tkinter as tk
import tkinter.font
from tkinter import messagebox

class HelperGui:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("530x550")
        self.root.minsize(530, 550)
        self.root.title("Registration Helper")
        self.small_font = tk.font.Font( family = "Calibri", size = 12)
        self.big_font = tk.font.Font( family = "Calibri", size = 16)
        self.root.option_add( "*font", "Calibri 14" )   #default font
        self.instructions_text = "Each course in new line.\nUse > to indicate replace hierarchy. Example:\n\n114804-12>333123-12\n234124-13\n394804-18>123456-10>123456-20\n...\nIn the above example 333123-12 will be replaced by 114804-12\nAnd 123456-20 will be replaced by 123456-10 and both will be replaced by 394804-18"

        self.helper = None
        self.driver = None
        self.radio_variable = tk.StringVar()
        self.replacement_course = ""
        self.DEFAULT_FREQUENCY = 10
        self.frequency = 1

        self.login_frame = tk.LabelFrame(self.root, padx=5, pady=5)
        self.login_frame.pack(pady=3, padx=10, fill="x")
        self.email_label = tk.Label(self.login_frame, text = "Email:")
        self.email_label.grid(row=0, column=0, sticky="w")
        self.password_label = tk.Label(self.login_frame, text = "Password:")
        self.password_label.grid(row=1, column=0, sticky="w", pady=10)
        self.login_button = tk.Button(self.login_frame, text = "Login", bd = 3, command = self.login_click)
        self.login_button.grid(row=1, column=3, sticky="w")
        self.login_clear_button = tk.Button(self.login_frame, text = "Clear", bd = 3, command = self.login_clear_click)
        self.login_clear_button.grid(row=1, column=2, sticky="w")
        self.user_name_entry = tk.Entry(self.login_frame, width = 40)
        self.user_name_entry.grid(row=0, column=1, sticky="w", columnspan=3)
        self.user_name_entry.focus()
        self.password_entry = tk.Entry(self.login_frame, width = 27, show = "*")
        self.password_entry.grid(row=1, column=1, sticky="w")

        self.wanted_courses_frame = tk.LabelFrame(self.root, padx=5, pady=5)
        self.wanted_courses_frame.pack(pady=3, padx=10, fill= "both", expand="true")
        self.pending_courses_frame = tk.LabelFrame(self.wanted_courses_frame, text = "Pending courses:", font = self.small_font, padx=5, pady=5)
        self.pending_courses_frame.pack(side= "bottom", fill="both", expand= "true")
        self.pending_courses_text = tk.Text(self.pending_courses_frame, height=1, fg = "red", font = self.small_font)
        self.pending_courses_text.pack(fill="both", expand= "true", pady= 5)
        self.pending_courses_text.tag_config("got", foreground="green")
        self.pending_courses_text.tag_config("pending", foreground="red")
        self.pending_courses_text.tag_config("sep1", foreground="blue")
        self.pending_courses_text.tag_config("sep2", foreground="black")
        self.pending_courses_text.insert("0.0", "None")
        self.pending_courses_text.config(state="disabled")
        self.courses_text = tk.Text(self.wanted_courses_frame, height=8, fg = "grey", font = self.small_font)
        self.courses_text.insert(0.0, self.instructions_text)
        self.courses_text.pack(fill="both", expand= "true", pady= 5)
        self.enter_courses_label = tk.Label(self.wanted_courses_frame, text = "Enter wanted courses -", font = self.big_font)
        self.enter_courses_label.pack(side= "left", anchor="n")
        self.enter_courses_button = tk.Button(self.wanted_courses_frame, text = "Enter courses", bd = 3, font = self.small_font, command = self.enter_courses_click)
        self.enter_courses_button.pack(side= "left",anchor="n", padx= 50)

        self.start_frame = tk.LabelFrame(self.root, padx=5, pady=5)
        self.start_frame.pack(pady=3, padx=10, fill="x")
        self.status_label = tk.Label(self.start_frame, text = "Status:")
        self.status_label.grid(row=1, column=0, sticky="w")
        self.status_dynamic_label = tk.Label(self.start_frame, text = "Standby", fg = "red")
        self.status_dynamic_label.grid(row=1, column=1, sticky="w",)
        self.operating_frequency_label = tk.Label(self.start_frame, text = "Operating frequency:")
        self.operating_frequency_label.grid(row=0, column=0, sticky="w", columnspan=2)
        self.frequency_entry = tk.Entry(self.start_frame, width = 3,font = self.small_font)
        self.frequency_entry.grid(row=0, column=2, sticky="w")
        self.frequency_entry.insert(0, self.DEFAULT_FREQUENCY)
        self.operating_frequency_seconds_label = tk.Label(self.start_frame, text = "seconds.")
        self.operating_frequency_seconds_label.grid(row=0, column=3, sticky="w")
        self.start_button = tk.Button(self.start_frame, text = "Start", fg = "green", width = 8, bd = 5, font = self.big_font, command = self.start_click)
        self.start_button.grid(row=0, column=5, sticky="w", rowspan=2, padx=5)
        self.stop_button = tk.Button(self.start_frame, text = "Stop", fg = "red", width = 8, bd = 5, font = self.big_font, command = self.stop_click)
        self.stop_button.grid(row=0, column=4, sticky="w", rowspan=2, padx=5)

        self.replacement_course_dynamic_label = tk.Label(self.root, fg = "green", font = self.small_font)

        self.courses_text.bind("<FocusIn>", self.handle_courses_text_focus_in)
        self.courses_text.bind("<FocusOut>", self.handle_courses_text_focus_out)
        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing) DEBUG
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
            if self.courses_text["fg"] != "grey":
                self.helper.course_list = [course for course in self.courses_text.get(0.0, "end-1c").split("\n") if not course.isspace() and course != ""]
                if self.helper.course_list == []:
                    self.pending_courses_text.config(state="normal")
                    self.pending_courses_text.delete("0.0", "end")
                    self.pending_courses_text.insert("0.0", "None")
                    self.pending_courses_text.config(state="disabled")
                else:
                    self.pending_courses_text.config(state="normal")
                    self.pending_courses_text.delete("0.0", "end")
                    self.pending_courses_text.insert("0.0", " | ".join(self.helper.course_list))
                    self.pending_courses_text.config(state="disabled")
                    self.pending_course_mark_sep(">", "sep2")
                    self.pending_course_mark_sep("|", "sep1")
        else:
            messagebox.showinfo(title = "Error", message = "Login first")

    def pending_course_tag_add(self, text:str, tag:str):
        countVar = tk.StringVar()
        pos = self.pending_courses_text.search(text, "0.0", stopindex="end", count=countVar)
        if pos != "":
            self.pending_courses_text.tag_add(tag, pos, "%s + %sc" % (pos, countVar.get()))

    def pending_course_tag_remove(self, text:str, tag:str):
        countVar = tk.StringVar()
        pos = self.pending_courses_text.search(text, "0.0", stopindex="end", count=countVar)
        if pos != "":
            self.pending_courses_text.tag_remove(tag, pos, "%s + %sc" % (pos, countVar.get()))

    def pending_course_mark_sep(self, text:str, tag:str):
        index = "0.0"
        countVar = tk.StringVar()
        while True:
            index = self.pending_courses_text.search(text, index, stopindex="end", count=countVar)
            if index == "":
                break 
            self.pending_courses_text.tag_add(tag, index, "%s + %sc" % (index, countVar.get()))
            index = "%s + %sc" % (index, countVar.get())


    def register_loop(self):
        if self.helper is not None:
            if self.helper.enable:
                self.helper.register_all(self)
            else:
                self.status_dynamic_label["text"] = "Standby" #
                self.status_dynamic_label["fg"] = "red"       # when all registrations are completed
        self.root.after(int(self.frequency)*1000, self.register_loop)    #loop forever

    def start_click(self):
        if self.helper is not None:
            self.status_dynamic_label["text"] = "Running"
            self.status_dynamic_label["fg"] = "green"
            if self.frequency_entry.get() == "":
                self.frequency_entry.insert(0, self.DEFAULT_FREQUENCY)
            self.frequency = int(self.frequency_entry.get())
            self.helper.enable = True
            self.root.after(100, self.register_loop)
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

    def handle_courses_text_focus_in(self, event = None):
        if self.courses_text["fg"] == "grey":
            self.courses_text.delete(0.0, "end-1c")
            self.courses_text["fg"] = "black"

    def handle_courses_text_focus_out(self, event = None):
        if self.courses_text.get(0.0,"end-1c") == "":
            self.courses_text.delete(0.0, "end-1c")
            self.courses_text["fg"] = "grey"
            self.courses_text.insert(0.0, self.instructions_text)

class Helper:
    def __init__(self, email:str, password:str):
        self.driver = None
        self.enable = False
        self.course_list = []
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.TIMEOUT = 10
        self.REGISTRATION_TIMEOUT = 20
        self.IS_AVAILABLE = "text-success"
        #self.login(email, password)
        #self.action = ActionChains(self.driver)    #DEBUG

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
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div/div/div")))
        SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[3]/div/div[1]/div/span"
        groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        if len(groups) == 0:
            SPANS_XPATH = "/html/body/div[2]/div[3]/div/div/section/div/div/div[2]/div/div[1]/div/span"
            groups = self.driver.find_elements(By.XPATH, SPANS_XPATH)
        return groups, SPANS_XPATH
    
    def is_group_available(self, course_number:str, group_number:str) -> bool:
        self.driver.get("https://students.technion.ac.il/local/technionsearch/course/" + course_number)
        GROUP_NUMBER_XPATH = "/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div"
        AVAILABLE_POSITIONS_XPATH = "/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/div[2]"
        groups, SPANS_XPATH = self.get_spans_xpath()
        result = False
        for index in range(len(groups)):
            if self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]" + GROUP_NUMBER_XPATH).get_attribute("data-group_id") == group_number and self.driver.find_element(By.XPATH, SPANS_XPATH + "[" + str(index+1) + "]" + AVAILABLE_POSITIONS_XPATH).get_attribute("class") == self.IS_AVAILABLE:
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
        existing_courses = WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, COURSES_XPATH_PREFIX)))
        for index in range(len(existing_courses)):
            elem = self.driver.find_element(By.XPATH, COURSES_XPATH_PREFIX + "[" + str(index+1) + "]" + COURSES_XPATH_SUFFIX)
            if elem.get_attribute("data-course_id") == course.split("-")[0] and elem.get_attribute("data-group_id") == course.split("-")[1]:
                self.action.double_click(WebDriverWait(self.driver, self.TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, COURSES_XPATH_PREFIX + "[" + str(index+1) + "]" + COURSES_XPATH_SUFFIX)))).perform()
                time.sleep(5)

    def register_all(self, gui) -> None:
        temp = self.course_list[:]
        for line in temp:
            hierarchy = line.split(">")
            for hier_i, course_and_group in enumerate(hierarchy):
                (course, group) = course_and_group.split("-")
                # check if already registered - if true break - put in remove and register
                #if self.is_group_available(course, group):
                if messagebox.askyesno("available?",course_and_group):  #DEBUG
                    if hier_i == 0:
                        self.course_list.remove(line)
                    else:   #there is higher priority
                        index = self.course_list.index(line)
                        self.course_list[index] = self.course_list[index][:self.course_list[index].find(course_and_group)+len(course_and_group)]    #remove all the lower priority courses

                    if len(hierarchy[hier_i:])>1: #there is more hierarchy after - remove first
                        course_to_remove = hierarchy[-1]
                        #self.remove_course(course_to_remove)
                        gui.pending_course_tag_remove(course_to_remove, "got")
                        gui.pending_course_tag_add(course_to_remove, "pending")

                    #self.register_course(course, group)
                    gui.pending_course_tag_add(course_and_group, "got")
                    break
        if len(self.course_list) == 0:  #all courses done
            self.enable = False
    
    def register_course(self, course:str, group:str) -> None:
        self.add_to_cart(course, group)
        self.checkout_cart()


#------------main------------
HelperGui()