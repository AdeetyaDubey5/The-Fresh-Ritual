import streamlit as st
import base64
from Home import main as second_module_main
import mysql.connector
from mysql.connector import Error
import hashlib
backgroundColor = "#F0F0F0"
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('//Users/adeetyadubey/Desktop/TFR/tfr_zz/foto.png')


def create_user_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@8476",
        database="db"
    )
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL)')
    conn.close()

def add_userdata(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@8476",
        database="db"
    )
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql@8476",
            database="db"
        )
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))
        result = c.fetchone()
        user_id = result[0] if result is not None else None
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        user_id = None
    finally:
        if conn.is_connected():
            conn.close()
    return user_id


def signup_user(username, password):
    add_userdata(username, password)
    st.success("You have successfully created an account!")


import mysql.connector
from mysql.connector import IntegrityError

def signup():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    con_password = st.text_input("Confirm Password", type="password")
    signed_up = st.session_state.get("signed_up", False)

    if st.button("Signup"):
        if not username or not password or not con_password:
            st.warning("Invalid credentials! Please enter all fields.")
        elif password != con_password:
            st.warning("Password does not match! Enter again")
        else:
            try:
                # Attempt to sign up the user
                signup_user(username, password)
                st.session_state["username"] = username
                st.session_state["signed_up"] = True
                st.success("Signup successful!")
                # Trigger a rerun to go to the next page
                st.rerun()
            except IntegrityError:
                st.error("Username already exists. Please choose a different username.")
    return username

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    logged_in = st.session_state.get("logged_in", False)

    if st.button("Login"):
        if not username or not password:
            st.warning("Please enter both Username and Password.")
        else:
            # Check if the username and password are valid
            user_id = login_user(username, password)
            if user_id is not None:
                st.session_state["username"] = username
                st.session_state["logged_in"] = True
                # Trigger a rerun to go to the next page
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again!")
    return username


def main():
    st.markdown("# <div style='text-align: center;'>The Fresh Ritual</div>", unsafe_allow_html=True)
    st.write("")
    st.subheader("Signup")
    
    

    #username = signup()  # Get the username after signup
    
    login_signup = st.radio("Select Option", ("Signup", "Login"))
    
    if (login_signup == 'Signup'):
        username = signup()
    elif (login_signup == 'Login'):
        username = login()
    


if __name__ == "__main__":
    # Check if the session state variables exist, if not initialize them
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "signed_up" not in st.session_state:
        st.session_state["signed_up"] = False

    # If the user is not logged in or has not signed up, call the main function
    if not st.session_state["logged_in"] and not st.session_state["signed_up"]:
        main()
    else:
        # If the user is logged in, call the third_module_main function
        if st.session_state["logged_in"]:
            second_module_main()
        # If the user has signed up, call the second_module_main function
        elif st.session_state["signed_up"]:
            second_module_main()
