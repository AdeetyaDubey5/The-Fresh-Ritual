import streamlit as st
import mysql.connector

# Function to connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@8476",
        database="db"
    )

# Function to insert feedback into the database
def insert_feedback(username, feedback):
    try:
        conn = connect_to_database()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (username, feedback) VALUES (%s, %s)", (username, feedback))
            conn.commit()
            st.success("Feedback submitted successfully!")
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to store user data in the database
# Function to store user data in the database
def store_user_data(username, age, gender, daily_water_intake, skin_type, skin_tone, skin_concerns, sensitivity_level, allergies, daily_sleep):
    try:
        conn = connect_to_database()
        if conn.is_connected():
            cursor = conn.cursor()

            # Get user ID based on the username
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]

            # Convert skin_concerns to a single string with proper formatting
            formatted_skin_concerns = ', '.join([concern.strip().capitalize() for concern in skin_concerns.split(',')])
            
            # Insert user data into the database
            cursor.execute("""
                INSERT INTO user_data 
                (user_id, age, gender, daily_water_intake, skin_type, skin_tone, skin_concerns, sensitivity_level, allergies, daily_sleep)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, age, gender, daily_water_intake, skin_type, skin_tone, formatted_skin_concerns, sensitivity_level, allergies, daily_sleep))
            conn.commit()
            st.success("User data stored successfully!")
    except mysql.connector.Error as e:
        st.error(f"Error storing user data: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def recommend_skincare_routine(primary_skin_concerns):
    routine = ""
    for concern in primary_skin_concerns:
        if concern == "Acne":
            routine += "### Acne:\n" \
                       "##### Day Routine:\n" \
                       "Cleanser: Salicylic Acid Cleanser \n\n" \
                       "Treatment: Benzoyl Peroxide Spot Treatment\n\n" \
                       "Moisturizer: Oil-Free Moisturizer\n\n" \
                       "Sunscreen: Non-comedogenic SPF\n\n" \
                       "##### Night Routine:\n" \
                       "Cleanser: Salicylic Acid Cleanser\n\n" \
                       "Treatment: Retinol Serum (to prevent acne and improve skin texture)\n\n" \
                       "Moisturizer: Lightweight, Non-comedogenic Moisturizer\n\n\n"
        elif concern == "Dryness":
            routine += "### Dry Skin:\n" \
                       "##### Day Routine:\n" \
                       "Cleanser: Gentle Hydrating Cleanser\n\n" \
                       "Serum: Hyaluronic Acid Serum\n\n" \
                       "Moisturizer: Rich Moisturizing Cream\n\n" \
                       "Sunscreen: Hydrating SPF\n\n" \
                       "##### Night Routine:\n" \
                       "Cleanser: Hydrating Cleanser\n\n" \
                       "Serum: Hyaluronic Acid Serum\n\n" \
                       "Moisturizer: Nourishing Night Cream\n\n"
        # Add more routines for other concerns if needed

    return routine

# Update the home function to call the modified recommend_skincare_routine function
# Modify the home function to properly format the skin concerns
def home(username):
    st.markdown("# <div style='text-align: center;'>The Fresh Ritual</div>", unsafe_allow_html=True)
    st.write("## Home")

    # Retrieve user profile data from the database based on the username
    user_profile = fetch_user_profile(username)

    # Display user profile data
    if user_profile:
        st.write("##### Your Responses:")
        st.write(f"Age:  {user_profile[6]} years")  # Age at index 4
        st.write(f"Gender:  {user_profile[5]}")  # Gender at index 3
        st.write(f"Daily Water Intake:  {user_profile[4]} liters")  # Daily Water Intake at index 2
        st.write(f"Skin Type:  {user_profile[2]}")  # Skin Type at index 1
        st.write(f"Skin Tone:  {user_profile[3]}")  # Skin Tone at index 5
        st.write("Primary Skin Concerns:")
        if user_profile[7]:
            primary_concerns = [concern.strip().lower() for concern in user_profile[7].split(',')]
            formatted_concerns = ''.join(primary_concerns)
            st.write(formatted_concerns)
        else:
            st.write("No skin concerns selected.")    
    
        st.write(f"Skin Sensitivity Level:  {user_profile[8]}")  # Skin Sensitivity Level at index 7
        st.write(f"Allergies:  {user_profile[9]}")  # Allergies at index 8
        st.write(f"Daily Sleep: {user_profile[10]} hours")  # Daily Sleep at index 9

        # Recommend skincare routine based on user's skin concerns
        recommended_routine = ""
        if user_profile[7]:
            recommended_routine = recommend_skincare_routine(user_profile[7].split(', '))
        else:
            recommended_routine = "Since you haven't selected any primary skin concerns, here's a basic routine:\n" \
                                  "Day Routine:\n" \
                                  "1. Cleanser: Gentle Hydrating Cleanser\n" \
                                  "2. Moisturizer: Rich Moisturizing Cream\n" \
                                  "3. Sunscreen: Hydrating SPF\n\n" \
                                  "Night Routine:\n" \
                                  "1. Cleanser: Hydrating Cleanser\n" \
                                  "2. Moisturizer: Nourishing Night Cream\n"

        # Print the recommended routine directly
        st.write("### Recommended Skincare Routine:")
        st.write(recommended_routine)


    else:
        st.subheader("Let's begin with some basic questionnaires:")

        # Question 1: Age
        age = st.slider("What's your age?", min_value=0, max_value=120, step=1)

        # Question 2: Gender
        gender = st.radio("Choose your gender", ("Male", "Female", "Other"))

        # Question 3: Daily Water Intake
        daily_water_intake = st.slider("What's your water intake (in liters)?", min_value=0, max_value=10, step=1)

        # Question 4: Skin Type
        skin_type = st.radio("What's your skin type?", ("Dry", "Normal", "Oily", "Combination"))

        # Question 5: Skin Tone
        skin_tone = st.radio("What's your skin tone?", ("Medium", "Fair", "Dark", "Olive", "Tan"))

        # Question 6: Skin Concerns
        st.write("Select the skin concerns you face:")
        acne = st.checkbox("Acne")
        dryness = st.checkbox("Dryness")
        oiliness = st.checkbox("Excess Oiliness")
        aging = st.checkbox("Aging")
        redness_irritation = st.checkbox("Redness and Irritation")
        fine_lines_wrinkles = st.checkbox("Fine Lines and Wrinkles")
        pigmentation = st.checkbox("Dark Spots and Hyperpigmentation")
        under_eye_circles_puffiness = st.checkbox("Under-eye Circles and Puffiness")
        uneven_texture = st.checkbox("Uneven Skin Texture")
        enlarged_pores = st.checkbox("Enlarged Pores")
        dull_skin = st.checkbox("Dull Skin")

        # Store selected skin concerns in a list
        skin_concerns = []
        if acne:
            skin_concerns.append("Acne")
        if dryness:
            skin_concerns.append("Dryness")
        if oiliness:
            skin_concerns.append("Excess Oiliness")
        if aging:
            skin_concerns.append("Aging")
        if redness_irritation:
            skin_concerns.append("Redness and Irritation")
        if fine_lines_wrinkles:
            skin_concerns.append("Fine Lines and Wrinkles")
        if pigmentation:
            skin_concerns.append("Dark Spots and Hyperpigmentation")
        if under_eye_circles_puffiness:
            skin_concerns.append("Under-eye Circles and Puffiness")
        if uneven_texture:
            skin_concerns.append("Uneven Skin Texture")
        if enlarged_pores:
            skin_concerns.append("Enlarged Pores")
        if dull_skin:
            skin_concerns.append("Dull Skin")

        # Question 7: Sensitivity Level
        sensitivity_level = st.radio("To what extent is your skin sensitive?", ("Low", "Moderate", "High", "Not sensitive"))

        # Question 8: Any allergies
        allergies = st.selectbox("Do you have any facial allergies?", ("No allergy", "Hives (raised red bumps or splotches on the skin)", "Contact dermatitis (an itchy rash caused by direct contact with a substance or an allergic reaction to it.)", "Eczema ( a condition that causes your skin to become dry, itchy and bumpy)"))

        # Question 9: Daily Sleep
        daily_sleep = st.slider("How much do you sleep in a day?", min_value=0, max_value=24, step=1)

        # Submit Button
        if st.button("Submit"):
            if not username or not skin_type or not daily_water_intake or not gender or not age:
                st.warning("Please fill out all required fields marked with an asterisk (*)")
            else:
                # Store user data in the database
                store_user_data(username, age, gender, daily_water_intake, skin_type, skin_tone, ",".join(skin_concerns), sensitivity_level, allergies, daily_sleep)
                st.session_state["proceed_clicked"] = True
                st.success("Thank you for completing the questionnaire!")
                st.write("Redirecting to login page...")
                st.rerun()


# Function to fetch user profile data from the database
# Function to fetch user profile data from the database
def fetch_user_profile(username):
    try:
        conn = connect_to_database()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.username, ud.skin_type, ud.skin_tone, ud.daily_water_intake, ud.gender, ud.age, 
                ud.skin_concerns, ud.sensitivity_level, ud.allergies, ud.daily_sleep
                FROM users u
                JOIN user_data ud ON u.id = ud.user_id
                WHERE u.username = %s
                """, (username,))

            user_profile = cursor.fetchone()
            if user_profile:
                # Check if skin concerns are None or a list
                skin_concerns = user_profile[7]
                if skin_concerns is not None and isinstance(skin_concerns, list):
                    user_profile[7] = ", ".join(skin_concerns)
                #print("User Profile:", user_profile)  # Print user profile for debugging
            return user_profile
    except mysql.connector.Error as e:
        st.error(f"Error fetching user profile data: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# Profile page
def profile(username):
    st.title("Your Profile")
    
    # Retrieve user profile data from the database based on the username
    user_profile = fetch_user_profile(username)

    # Display user profile data
    if user_profile:
        st.write(f"User ID: {user_profile[0]}")
        st.write(f"Username: {user_profile[1]}")
        st.write(f"Gender: {user_profile[5]}")
        st.write(f"Age: {user_profile[6]} years")
    else:
        st.warning("User profile data not found.")


# About us page
def about_us():
    st.header("About Us")
    st.write("Welcome to The Fresh Ritual! We are a team of passionate programmers dedicated to bringing you the best in skincare routines and wellness practices. Our team comprises three talented individuals:")

    st.write("**Adeetya Dubey**")
    st.write("Adeetya is the backbone of our technical infrastructure. With his expertise in backend development and database management, he ensures that our platform runs smoothly and securely. Vedansh's dedication to reliability ensures that you can always depend on The Fresh Ritual.")

    st.write("Together, we strive to create a holistic experience that empowers you to take charge of your skincare journey. Whether you're a skincare enthusiast or a wellness seeker, we're here to support you every step of the way.")

    st.write("**Akanksha Yadav**")
    st.write("Akanksha is our resident data wizard. She dives deep into the world of user insights and preferences, using her analytical skills to optimize the user experience. With Akanksha on board, we ensure that every interaction with our platform is tailored to your needs.")

    st.write("**Vedansh Gure**")
    st.write("Vedansh is a visionary coder with a keen eye for design. With a knack for turning complex ideas into elegant solutions, Adeetya ensures that our platform not only functions flawlessly but also looks stunning.")

    st.write("Join us on The Fresh Ritual and embark on a journey to radiant skin and vibrant well-being!")


# Streamlit app
def main():
    st.sidebar.title("Navigation")
    navigation = st.sidebar.radio("Go to", ("Home", "Profile", "Feedback", "About Us"))

    username = st.session_state.get("username")

    if navigation == "Home":
        home(username)
    elif navigation == "Profile":
        if username:
            profile(username)
        else:
            st.error("User not logged in.")
    elif navigation == "Feedback":
        st.title("Feedback")
        st.write("We value your feedback! Please share your thoughts below.")

        feedback = st.text_area("Write your feedback here:")

        if st.button("Submit Feedback"):
            if feedback:
                if username:
                    insert_feedback(username, feedback)
                else:
                    st.error("User not logged in.")
            else:
                st.warning("Please enter your feedback before submitting.")

        st.write("😊 Thank you for your feedback! We appreciate it.")
    elif navigation == "About Us":
        about_us()

# Run the Streamlit app
if __name__ == "__main__":
    main()
