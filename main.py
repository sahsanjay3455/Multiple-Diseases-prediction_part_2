import mysql.connector
import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu
from PIL import Image

# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="Sanjay#$55", 
    database="crud_new1"
    
    )

mycursor = mydb.cursor()
print("Connection Established")


working_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the model files
diabetes_model_path = (
    r"C:/Users/KIIT01/Desktop/Project_1/disease_prediction/diabetes1.pkl"
)
heart_disease_model_path = (
    r"C:/Users/KIIT01/Desktop/Project_1/disease_prediction/heart1.pkl"
)
kidney_disease_model_path = (
    r"C:/Users/KIIT01/Desktop/Project_1/disease_prediction/kidney.pkl"
)


# Check if the model files exist and load them
if os.path.exists(diabetes_model_path):
    diabetes_model = pickle.load(open(diabetes_model_path, "rb"))
else:
    st.error("Diabetes model file not found!")

if os.path.exists(heart_disease_model_path):
    heart_disease_model = pickle.load(open(heart_disease_model_path, "rb"))
else:
    st.error("Heart disease model file not found!")

if os.path.exists(kidney_disease_model_path):
    kidney_disease_model = pickle.load(open(kidney_disease_model_path, "rb"))
else:
    st.error("Kidney disease model file not found!")

NewBMI_Overweight = 0
NewBMI_Underweight = 0
NewBMI_Obesity_1 = 0
NewBMI_Obesity_2 = 0
NewBMI_Obesity_3 = 0
NewInsulinScore_Normal = 0
NewGlucose_Low = 0
NewGlucose_Normal = 0
NewGlucose_Overweight = 0
NewGlucose_Secret = 0


# Function to check login credentials
def check_login(email, password):
    sql = "SELECT * FROM users WHERE email=%s AND hashed_password=%s"
    val = (email, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    return result


# Create Streamlit App
def main():
    st.set_page_config(
        page_title="Multiple Disease Prediction", layout="wide", page_icon="💕❤️"
    )
    st.title("Multiple Disease Prediction")

    # Check if a user is logged in or not
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # If the user is not logged in, show login interface
    if not st.session_state.logged_in:
        st.subheader("Login")
        email = st.text_input(
            "Enter Email", key="login_email"
        )  # Unique key for login email
        password = st.text_input(
            "Enter Password", type="password", key="login_password"
        )

        if st.button("Login"):
            user = check_login(email, password)
            if user:
                st.success("Login Successful!")
                st.session_state.logged_in = True
                st.session_state.user = user  # Store user info in session
            else:
                st.error("Invalid credentials. Please try again or create an account.")

        # Option to create an account if login fails
        if st.button("Create Account"):
            st.session_state.create_account = True

    # Show the account creation form if "Create Account" is clicked
    if "create_account" in st.session_state and st.session_state.create_account:
        st.subheader("Create a New Account")
        id = st.number_input("Enter the id")
        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")  # Unique key for create account email
        password = st.text_input("Enter Password", type="password")
        if st.button("submit"):
            sql = "INSERT INTO users (id, name, email, hashed_password) VALUES (%s, %s, %s, %s)"
            val = (id, name, email, password)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Account created successfully! Please log in.")
            st.balloons()
            st.session_state.create_account = False  # Reset account creation flow
        else:
            print("enter the valid id number")

    # If logged in, show CRUD operations
    if st.session_state.logged_in:
        st.sidebar.success(
            f"Welcome , {st.session_state.user[1]}"
        )  # Display username in the sidebar

        with st.sidebar:
            selected = option_menu(
                "Menu List",
                [
                    "operation",
                    "Diabetes Disease pred",
                    "Heart Disease prediction",
                    "kidney Disease prediction",
                ],
                menu_icon="hospital-fill",
                icons=["gear", "activity", "heart", "person"],
                default_index=0,
            )

        if selected == "operation":
            option = st.sidebar.selectbox(
                "Select Operation",
                ("Introduction", "Read Records", "Update Record", "Delete Records"),
                index=0,
            )

            if option == "Introduction":
                st.subheader("Welcome to Our Hospital")

                # Add a hospital image
                st.write(
                    """
                **Our hospital is equipped with state-of-the-art technology and provides comprehensive care across various medical disciplines.**
                Our dedicated staff ensures that you receive the best treatment possible. We are committed to enhancing the health and well-being of our community.
                """
                )
                st.video("Major_Project _video.mp4")
                st.image(
                    "hospital_image.jpg",
                    caption="Our Modern Healthcare Facility",
                    channels="RGB",
                    width=800,
                )

                # Add a video with description about the hospital

                # st.audio("hospital_audio.mp3")

            elif option == "Read Records":
                st.subheader("Read the Records")
                mycursor.execute("SELECT id,name,email FROM users")
                result = mycursor.fetchall()

                for row in result:
                    st.write(row)

                st.balloons()

            elif option == "Update Record":
                st.subheader("Update the record")
                id = st.number_input("Enter Id", min_value=1)
                num = st.number_input(
                    "For update press 1 for name, 2 for email, 3 for password"
                )
                if num == 1:
                    name = st.text_input("Enter New Name", key="update_name")
                    if st.button("Update"):
                        sql = "UPDATE users SET name=%s WHERE id=%s"
                        val = (name, id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Record Updated Successfully!!")
                        st.balloons()
                elif num == 2:
                    email = st.text_input("Enter New Email", key="update_email")
                    if st.button("Update"):
                        sql = "UPDATE users SET email=%s WHERE id=%s"
                        val = (email, id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Record Updated Successfully!!")
                        st.balloons()
                elif num == 3:
                    hashed_password = st.text_input(
                        "Enter New Password", key="update_password"
                    )
                    if st.button("Update"):
                        sql = "UPDATE users SET hashed_password=%s WHERE id=%s"
                        val = (hashed_password, id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Record Updated Successfully!!")
                        st.balloons()

            elif option == "Delete Records":
                st.subheader("Delete the Records")
                admin = st.text_input("enter the admin user name")
                pass1 = st.text_input("enter the password:", type="password")
                if admin == "sanjay" and pass1 == "sanjay@123":
                    id = st.number_input("Enter id", min_value=1)
                    if st.button("Delete"):
                        sql = "DELETE FROM users WHERE id=%s"
                        val = (id,)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Record Deleted Successfully!!")
                        st.balloons()
                else:
                    st.error(
                        "Remainder: If You don't know user-name and password then consult with admin"
                    )

        if selected == "Diabetes Disease pred":
            st.title("Diabetes Prediction Using Machine Learning")
            col1, col2, col3 = st.columns(3)

            with col1:
                Pregnancies = st.text_input("Number of Pregnancies")
            with col2:
                Glucose = st.text_input("Glucose Level")
            with col3:
                BloodPressure = st.text_input("Blood Pressure Value")
            with col1:
                SkinThickness = st.text_input("Skin Thickness Value")
            with col2:
                Insulin = st.text_input("Insulin Value")
            with col3:
                BMI = st.text_input("BMI Value")
            with col1:
                DiabetesPedigreeFunction = st.text_input("Diabetes Pedigree Function Value")
            with col2:
                Age = st.text_input("Age")

            diabetes_result = ""

            # Initialize variables with default values (0 or whatever is appropriate)
            NewBMI_Underweight = 0
            NewBMI_Overweight = 0
            NewBMI_Obesity_1 = 0
            NewBMI_Obesity_2 = 0
            NewBMI_Obesity_3 = 0
            NewInsulinScore_Normal = 0
            NewGlucose_Low = 0
            NewGlucose_Normal = 0
            NewGlucose_Overweight = 0
            NewGlucose_Secret = 0

            # Button to trigger prediction
            if st.button("Diabetes Test Result"):
                # Logic to update variables based on input
                if float(BMI) <= 18.5:
                    NewBMI_Underweight = 1
                elif 18.5 < float(BMI) <= 24.9:
                    pass
                elif 24.9 < float(BMI) <= 29.9:
                    NewBMI_Overweight = 1
                elif 29.9 < float(BMI) <= 34.9:
                    NewBMI_Obesity_1 = 1
                elif 34.9 < float(BMI) <= 39.9:
                    NewBMI_Obesity_2 = 1
                elif float(BMI) > 39.9:
                    NewBMI_Obesity_3 = 1

                # More conditions for insulin and glucose
                if 16 <= float(Insulin) <= 166:
                    NewInsulinScore_Normal = 1

                if float(Glucose) <= 70:
                    NewGlucose_Low = 1
                elif 70 < float(Glucose) <= 99:
                    NewGlucose_Normal = 1
                elif 99 < float(Glucose) <= 126:
                    NewGlucose_Overweight = 1
                elif float(Glucose) > 126:
                    NewGlucose_Secret = 1

                # Prepare input for prediction
                user_input = [
                    Pregnancies,
                    Glucose,
                    BloodPressure,
                    SkinThickness,
                    Insulin,
                    BMI,
                    DiabetesPedigreeFunction,
                    Age,
                    NewBMI_Underweight,
                    NewBMI_Overweight,
                    NewBMI_Obesity_1,
                    NewBMI_Obesity_2,
                    NewBMI_Obesity_3,
                    NewInsulinScore_Normal,
                    NewGlucose_Low,
                    NewGlucose_Normal,
                    NewGlucose_Overweight,
                    NewGlucose_Secret,
                ]

                user_input = [float(x) for x in user_input]
                prediction = diabetes_model.predict([user_input])

                if prediction[0] == 1:
                    diabetes_result = "The person is diabetic"
                else:
                    diabetes_result = "The person is not diabetic"

            st.success(diabetes_result)
            
        if selected == "Heart Disease prediction":
            st.title("Heart Disease Prediction Using Machine Learning")
            col1, col2, col3  = st.columns(3)

            with col1:
                age = st.text_input("Age")
            with col2:
                sex = st.text_input("Sex")
            with col3:
                cp = st.text_input("Chest Pain Types")
            with col1:
                trestbps = st.text_input("Resting Blood Pressure")
            with col2:
                chol = st.text_input("Serum Cholestroal in mg/dl")
            with col3:
                fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
            with col1:
                restecg = st.text_input('Resting Electrocardiographic results')

            with col2:
                thalach = st.text_input('Maximum Heart Rate achieved')

            with col3:
                exang = st.text_input('Exercise Induced Angina')

            with col1:
                oldpeak = st.text_input('ST depression induced by exercise')

            with col2:
                slope = st.text_input('Slope of the peak exercise ST segment')

            with col3:
                ca = st.text_input('Major vessels colored by flourosopy')

            with col1:
                thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')
            heart_disease_result = ""
            if st.button("Heart Disease Test Result"):
                user_input = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
                user_input = [float(x) for x in user_input]
                prediction = heart_disease_model.predict([user_input])
                if prediction[0]==1:
                    heart_disease_result = "This person is having heart disease"
                else:
                    heart_disease_result = "This person does not have any heart disease"
            st.success(heart_disease_result)
            
        if selected == "kidney Disease prediction": 
            st.title("Kidney Disease Prediction using ML")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                age = st.text_input('Age')

            with col2:
                blood_pressure = st.text_input('Blood Pressure')

            with col3:
                specific_gravity = st.text_input('Specific Gravity')

            with col4:
                albumin = st.text_input('Albumin')

            with col5:
                sugar = st.text_input('Sugar')

            with col1:
                red_blood_cells = st.text_input('Red Blood Cell')

            with col2:
                pus_cell = st.text_input('Pus Cell')

            with col3:
                pus_cell_clumps = st.text_input('Pus Cell Clumps')

            with col4:
                bacteria = st.text_input('Bacteria')

            with col5:
                blood_glucose_random = st.text_input('Blood Glucose Random')

            with col1:
                blood_urea = st.text_input('Blood Urea')

            with col2:
                serum_creatinine = st.text_input('Serum Creatinine')

            with col3:
                sodium = st.text_input('Sodium')

            with col4:
                potassium = st.text_input('Potassium')

            with col5:
                haemoglobin = st.text_input('Haemoglobin')

            with col1:
                packed_cell_volume = st.text_input('Packet Cell Volume')

            with col2:
                white_blood_cell_count = st.text_input('White Blood Cell Count')

            with col3:
                red_blood_cell_count = st.text_input('Red Blood Cell Count')

            with col4:
                hypertension = st.text_input('Hypertension')

            with col5:
                diabetes_mellitus = st.text_input('Diabetes Mellitus')

            with col1:
                coronary_artery_disease = st.text_input('Coronary Artery Disease')

            with col2:
                appetite = st.text_input('Appetitte')

            with col3:
                peda_edema = st.text_input('Peda Edema')
            with col4:
                aanemia = st.text_input('Aanemia')

            # code for Prediction
            kindey_diagnosis = ''

            # creating a button for Prediction    
            if st.button("Kidney's Test Result"):

                user_input = [age, blood_pressure, specific_gravity, albumin, sugar,
            red_blood_cells, pus_cell, pus_cell_clumps, bacteria,
            blood_glucose_random, blood_urea, serum_creatinine, sodium,
            potassium, haemoglobin, packed_cell_volume,
            white_blood_cell_count, red_blood_cell_count, hypertension,
            diabetes_mellitus, coronary_artery_disease, appetite,
            peda_edema, aanemia]

                user_input = [float(x) for x in user_input]

                prediction = kidney_disease_model.predict([user_input])

                if prediction[0] == 1:
                    kindey_diagnosis = "The person has Kidney's disease"
                else:
                    kindey_diagnosis = "The person does not have Kidney's disease"
                    
            st.success(kindey_diagnosis)  
                
            
            
            


if __name__ == "__main__":
    main()

