import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="AI Personalized Meal & Workout Planner", layout="wide")
st.title("💪 AI Personalized Meal & Workout Planner 🍽️")

# Load meal dataset
meals = pd.read_csv('meals.csv')

# Sidebar - User Info
st.sidebar.header('👤 User Preferences')
gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
goal = st.sidebar.selectbox('What is your goal?', ['Gain Muscle', 'Maintain Weight', 'Lose Fat'])
diet_type = st.sidebar.selectbox('Diet Preference', ['Both', 'Veg', 'Non-Veg'])
activity_level = st.sidebar.selectbox('Activity Level', ['Sedentary', 'Light Exercise', 'Moderate/Heavy Exercise'])

# BMI Calculation
st.sidebar.header("📏 BMI Calculator (Optional)")
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

bmi = weight / ((height / 100) ** 2)
bmi_status = ""
if bmi < 18.5:
    bmi_status = "Underweight"
elif 18.5 <= bmi < 24.9:
    bmi_status = "Normal"
elif 25 <= bmi < 29.9:
    bmi_status = "Overweight"
else:
    bmi_status = "Obese"

st.sidebar.markdown(f"**Your BMI:** {bmi:.2f} ({bmi_status})")

# 🌙 Sleep Tracking
st.header("😴 Sleep Tracker")
sleep_hours = st.slider('How many hours did you sleep last night?', 0, 12, 7)
if sleep_hours < 6:
    st.warning("⚠️ Try to sleep at least 7–8 hours for proper recovery.")
else:
    st.success("✅ Great! You're getting good sleep.")

# 💧 Water Intake Tracker
st.header("💧 Water Intake Reminder")
water_intake = st.number_input("How many glasses of water did you drink today? (1 glass = ~250ml)", min_value=0, max_value=30, value=8)
if water_intake < 8:
    st.warning(f"⚠️ Try to drink more water. You're {8 - water_intake} glasses short of the daily recommendation.")
else:
    st.success("✅ Awesome! You're staying well hydrated.")

# Filter meals by diet type
if diet_type == 'Both':
    filtered_meals = meals
else:
    filtered_meals = meals[meals['Type'].str.lower() == diet_type.lower()]

# Display Recommended Meals
st.header(f"🍱 Recommended Meals ({diet_type})")
st.dataframe(filtered_meals)

# 📊 Protein per Meal Chart (Cleaner Graph)
if 'Protein (g)' in filtered_meals.columns:
    st.subheader("📊 Protein Content per Meal")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(filtered_meals['Meal'], filtered_meals['Protein (g)'], color='#66B2FF')
    plt.xticks(rotation=90, fontsize=8)
    ax.set_ylabel("Protein (g)")
    ax.set_title("Protein in Recommended Meals")
    st.pyplot(fig)

# 🏋️ Workout Routine
st.header("🏋️ Workout Routine Recommendations")
if activity_level == 'Sedentary':
    st.subheader("Sedentary Routine (Great for Beginners)")
    tasks = ["10-min Morning Stretch", "15-min Walk", "10-min Breathing or Yoga"]
elif activity_level == 'Light Exercise':
    st.subheader("Light Home Workout (No Equipment Needed)")
    tasks = ["20 Squats", "20 Lunges", "15 Knee Push-ups", "20-min Walk or Jog", "10-min Yoga"]
else:
    st.subheader("Gym/Heavy Workout (For Athletes)")
    tasks = [
        "Bench Press", "Shoulder Press", "Push-ups", "Pull-ups", "Dumbbell Rows",
        "Squats", "Deadlifts", "Lunges", "Calf Raises",
        "Planks", "Leg Raises", "Russian Twists",
        "20–30 Min Run or Cycling"
    ]

completed_tasks = [st.checkbox(task) for task in tasks]

# 📈 BMI Chart
st.subheader("📈 BMI Guidance")
fig_bmi, ax_bmi = plt.subplots(figsize=(6, 3))
x_bmi = ['Underweight', 'Normal', 'Overweight', 'Obese']
y_bmi = [18.5, 24.9, 29.9, 35]
ax_bmi.plot(x_bmi, y_bmi, marker='o', color='orange', linewidth=2)
ax_bmi.axhline(y=bmi, color='red', linestyle='--', label=f'Your BMI: {bmi:.2f}')
ax_bmi.legend()
ax_bmi.set_ylabel('BMI Value')
st.pyplot(fig_bmi)

# Footer
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: grey;'>Made with ❤️ by <b>Savan, Rehan, Aadil, Akash & Athul</b></h4>", unsafe_allow_html=True)
