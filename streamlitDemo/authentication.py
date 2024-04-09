import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader

# Admin Flag
ADMIN_MODE_KEY = 'ADMIN_MODE'
NOT_ADMIN_MODE_FLAG = '-1'

CURRENT_DIR =  os.getcwd()
if "streamlitDemo" in CURRENT_DIR:
    CONFIG_FILE = os.path.join(CURRENT_DIR, 'config.yaml')
else:
    CONFIG_FILE = os.path.join(CURRENT_DIR, 'streamlitDemo/config.yaml')

def authenticate():
    with open(CONFIG_FILE) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    name, authentication_status, username = authenticator.login('Login')

    if authentication_status == False:
        set_admin_mode(False)
        st.error('Username/password is incorrect')
        return
    
    if authentication_status == None:
        set_admin_mode(False)
        st.warning('Please enter your username and password')
        return

    if authentication_status:
        # reset password if first time logging in
        if not is_password_reset():
            try:
                if authenticator.reset_password(username, 'Reset password'):
                    # update credentials. stauth updates the config object in memory when password reset is performed.
                    # recommendation is to update the config yaml file accordingly.
                    # Reference https://github.com/mkhorasani/Streamlit-Authenticator#4-creating-a-password-reset-widget
                    update_config_file(config)
                    # update password_reset flag in config file. this flag is outside of stauth so have to be handled separately
                    update_config_value('password_reset', False)
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)
        else:
            # display logout
            authenticator.logout('Logout')
            st.write(f'Welcome *{name}*')
            set_admin_mode(True)
        return

def set_admin_mode(isAdminLoggedIn):
    os.environ[ADMIN_MODE_KEY] = "ADMIN_LOGGED" if isAdminLoggedIn else NOT_ADMIN_MODE_FLAG

def is_admin_mode():
    return os.environ.get(ADMIN_MODE_KEY, NOT_ADMIN_MODE_FLAG) == "ADMIN_LOGGED"

def is_user_authorized():    
    # authorized if in admin mode and password has been reset
    if is_admin_mode() and is_password_reset():
        return True
    
    # authorized if in dev mode
    if not is_prod_mode():
        return True
    
    # not authorized in all other scenarios 
    return False

def is_prod_mode():
    with open(CONFIG_FILE) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config['deploy_mode'] == 'prod'

def update_config_file(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file, sort_keys=False)

def update_config_value(key, value):
    with open(CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        # updates top level key
        data[f'{key}'] = value
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(data, file, sort_keys=False)

def is_password_reset():
    with open(CONFIG_FILE) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config['password_reset'] == False
