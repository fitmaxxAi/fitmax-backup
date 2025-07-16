import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Personalized Meal & Workout Planner 💪🍽️")

# Load dataset
meals = pd.read_csv('meals.csv')

# Sidebar for user input
st.sidebar.header('User Preferences')
goal = st.sidebar.selectbox('What is your goal?', ['Gain Muscle', 'Maintain Weight', 'Lose Fat'])
diet_type = st.sidebar.selectbox('Diet Type', ['Veg', 'Non-Veg'])
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

# BMI Line Graph Example (Ideal BMI ranges)
st.subheader("BMI Guidance 📈")
fig_bmi, ax_bmi = plt.subplots(figsize=(6, 3))
x_bmi = ['Underweight', 'Normal', 'Overweight', 'Obese']
y_bmi = [18.5, 24.9, 29.9, 35]
ax_bmi.plot(x_bmi, y_bmi, marker='o', color='orange')
ax_bmi.axhline(y=bmi, color='red', linestyle='--', label=f'Your BMI: {bmi:.2f}')
ax_bmi.legend()
ax_bmi.set_ylabel('BMI Value')
st.pyplot(fig_bmi)


# Filter meals by diet type
filtered_meals = meals[meals['Type'] == diet_type]

# Display meal recommendations
st.header(f"{goal} - {diet_type} Meal Recommendations 🍱")
st.dataframe(filtered_meals)

# Line Graph: Calories per Meal
st.subheader("Calories per Meal 📊")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(filtered_meals['Meal'], filtered_meals['Calories'], marker='o', linestyle='-', color='purple')
plt.xticks(rotation=90)
ax.set_ylabel("Calories")
ax.set_xlabel("Meals")
st.pyplot(fig)

# Pie Chart: Calories vs Protein
st.subheader("Nutrient Breakdown (Calories vs Protein) 🍕")
calories_sum = filtered_meals['Calories'].sum()
protein_sum = filtered_meals['Protein (g)'].sum()

fig_pie, ax_pie = plt.subplots()
ax_pie.pie([calories_sum, protein_sum], labels=['Total Calories', 'Total Protein (g)'],
           autopct='%1.1f%%', startangle=90, colors=['#FF9999','#66B2FF'])
ax_pie.axis('equal')
st.pyplot(fig_pie)

# Workout recommendations
st.header("Workout Routine Recommendations 🏋️‍♂️")

if activity_level == 'Sedentary':
    st.subheader('Sedentary Routine (Beginners, Office Workers)')
    st.write("""
    - 10 min Morning Stretch  
    - 15 min Walking (Slow pace)  
    - 10 min Breathing Exercises / Yoga  
    """)
elif activity_level == 'Light Exercise':
    st.subheader('Light Exercise Routine (Home Workouts, No Equipment)')
    st.write("""
    - 20 Squats  
    - 20 Lunges  
    - 15 Push-ups (Knee supported if needed)  
    - 20-Min Walk or Light Jog  
    - 10-Min Light Yoga or Stretch  
    """)
else:
    st.subheader('Moderate/Heavy Routine (Gym / Active Athletes)')
    st.write("""
    *Upper Body (3x a week)*  
    - Bench Press  
    - Shoulder Press  
    - Pushups  
    - Pullups  
    - Dumbbell Rows  

    *Lower Body (2x a week)*  
    - Squats  
    - Deadlifts  
    - Lunges  
    - Calf Raises  

    *Core (2x a week)*  
    - Planks  
    - Leg Raises  
    - Russian Twists  

    *Cardio (3x a week)*  
    - 20-30 Min Run / Cycle  
    """)

st.success("✅ App Ready for AI Exhibition 🚀")
