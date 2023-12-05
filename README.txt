This program’s purpose is to register a Technion student to desired courses when there’s an opening. This is achieved in two steps:
First of all, the program samples the Technion’s courses website at user set intervals in order to scan for an opening.
When an opening is detected, the desired course is added to the user’s cart and the cart gets checked out.
One of the program’s most significant features is defining hierarchy between courses.
This means that if course A is set to be more valuable than course B, then the program will sample continuously until the user is registered in course A, even if successful registration to course B has been made.
In that case, the registration to course B will be removed and replaced by A’s.


---- main code file is courseRegistrationHelper.py ----

Before first use:

Before using download the chromedriver version that corresponds to your chrome browser version, and put the exe file in "C:\Program Files (x86)\chromedriver.exe"
chromedriver download link: https://chromedriver.chromium.org/downloads

command for making exe out ot .py file in cmd:
pyinstaller --onefile courseRegistrationHelper.py
