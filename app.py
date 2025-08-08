import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Personalized Meal & Workout Planner", layout="wide")
st.title("AI Personalized Meal & Workout Planner 💪🍽️")

# Load dataset
meals = pd.read_csv('meals.csv')

# Sidebar for user input
st.sidebar.header('User Preferences')
gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
goal = st.sidebar.selectbox('What is your goal?', ['Gain Muscle', 'Maintain Weight', 'Lose Fat'])
diet_type = st.sidebar.selectbox('Diet Type', ['Both', 'Veg', 'Non-Veg'])
activity_level = st.sidebar.selectbox('Activity Level', ['Sedentary', 'Light Exercise', 'Moderate/Heavy Exercise'])

# BMI Calculator
st.sidebar.header("BMI Calculator (Optional)")
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

bmi = weight / ((height / 100) ** 2)
st.sidebar.markdown(f"*Your BMI:* {bmi:.2f}")

bmi_status = ""
if bmi < 18.5:
    bmi_status = "Underweight"
elif 18.5 <= bmi < 24.9:
    bmi_status = "Normal"
elif 25 <= bmi < 29.9:
    bmi_status = "Overweight"
else:
    bmi_status = "Obese"

st.sidebar.markdown(f"*Status:* {bmi_status}")

# Sleep Tracking
st.header("Daily Sleep Tracker 😴")
sleep_hours = st.slider('How many hours did you sleep last night?', min_value=0, max_value=12, value=7)
if sleep_hours < 6:
    st.warning("You should aim for at least 7-8 hours of sleep for better recovery.")
else:
    st.success("Great! You're getting enough rest.")

# Filter meals by diet type
if diet_type == 'Both':
    filtered_meals = meals
else:
    filtered_meals = meals[meals['Type'] == diet_type]

# Display meal recommendations
st.header(f"{goal} Meal Recommendations 🍱 ({diet_type} Meals)")
st.dataframe(filtered_meals)

# Line Graph: Calories per Meal (Professional Style)
st.subheader("Calories per Meal 📊")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered_meals['Meal'], filtered_meals['Calories'], marker='o', linestyle='-', color='#4CAF50')
plt.xticks(rotation=90, fontsize=8)
ax.set_ylabel("Calories", fontsize=10)
ax.set_xlabel("Meals", fontsize=10)
ax.set_title("Calories in Recommended Meals", fontsize=12)
st.pyplot(fig)

# Pie Chart: Calories vs Protein
st.subheader("Nutrient Breakdown (Calories vs Protein) 🍕")
calories_sum = filtered_meals['Calories'].sum()
protein_sum = filtered_meals['Protein (g)'].sum()

fig_pie, ax_pie = plt.subplots()
ax_pie.pie([calories_sum, protein_sum], labels=['Total Calories', 'Total Protein (g)'],
           autopct='%1.1f%%', startangle=90, colors=['#FF9999', '#66B2FF'])
ax_pie.axis('equal')
st.pyplot(fig_pie)

# Workout Routine Recommendations
st.header("Workout Routine Recommendations 🏋️‍♂️")

if activity_level == 'Sedentary':
    st.subheader('Sedentary Routine (Beginners, Office Workers)')
    sedentary_tasks = ["10 min Morning Stretch", "15 min Walking", "10 min Breathing / Yoga"]
    completed = [st.checkbox(task) for task in sedentary_tasks]
elif activity_level == 'Light Exercise':
    st.subheader('Light Exercise Routine (Home Workouts, No Equipment)')
    light_tasks = ["20 Squats", "20 Lunges", "15 Push-ups (Knee supported)", "20-Min Walk / Jog", "10-Min Light Yoga"]
    completed = [st.checkbox(task) for task in light_tasks]
else:
    st.subheader('Moderate/Heavy Routine (Gym / Active Athletes)')
    heavy_tasks = ["Bench Press", "Shoulder Press", "Pushups", "Pullups", "Dumbbell Rows", 
                   "Squats", "Deadlifts", "Lunges", "Calf Raises", 
                   "Planks", "Leg Raises", "Russian Twists", 
                   "20-30 Min Run / Cycle"]
    completed = [st.checkbox(task) for task in heavy_tasks]

# BMI Line Graph
st.subheader("BMI Guidance 📈")
fig_bmi, ax_bmi = plt.subplots(figsize=(6, 3))
x_bmi = ['Underweight', 'Normal', 'Overweight', 'Obese']
y_bmi = [18.5, 24.9, 29.9, 35]
ax_bmi.plot(x_bmi, y_bmi, marker='o', color='orange', linewidth=2)
ax_bmi.axhline(y=bmi, color='red', linestyle='--', label=f'Your BMI: {bmi:.2f}')
ax_bmi.legend()
ax_bmi.set_ylabel('BMI Value')
st.pyplot(fig_bmi)

# Footer with Names
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: grey;'>Made by <b>Savan,Rehan bomber,Aadil,Akash & Athul</b></h4>", unsafe_allow_html=True)

