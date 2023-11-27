import subprocess
import os

headerString = '''
##################################################
#########         Brilla AI Web App        #########
##################################################
'''

print(headerString)
print("### Starting up Brilla AI ###")
print("### Step 1: Installing essential dependencies ###")
run_dep = subprocess.Popen('pip install -q -r requirements.txt', shell= True)
run_dep.wait()

if run_dep.returncode == 0:
    print("### Step 2: Starting Up App ###")
    # clear up log file if it exists
    if os.path.isfile("app_output.log"):
        open("app_output.log", "w").close()

    start_app = subprocess.Popen('streamlit run Brilla_AI.py', shell= True)
    start_app.wait()
else:
    print("Failed to install dependencies. Please resolve and try again.")
