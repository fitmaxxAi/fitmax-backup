import streamlit as st
import pandas as pd
from random import sample
import matplotlib.pyplot as plt

# ---------- Load Meals ----------
meals_df = pd.read_csv("meals.csv")

# ---------- Calorie Calculator ----------
def calculate_calories(gender, weight, height, age, activity_level):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Very Active": 1.55,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    return round(tdee)

# ---------- Streamlit Page Setup ----------
st.set_page_config(page_title="AI Fitness Coach", page_icon="🏋️", layout="centered")
st.title("🏋️ AI Personalized Meal & Workout Recommendation")
st.markdown("*Smart AI-generated guidance for your muscle-gain journey.*")

# ---------- Inputs ----------
st.sidebar.header("🔧 Your Information")
age = st.sidebar.slider("Age", 15, 80, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.slider("Height (cm)", 140, 200, 170)
weight = st.sidebar.slider("Weight (kg)", 40, 120, 70)
activity_level = st.sidebar.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Very Active"])
diet = st.sidebar.selectbox("Diet Preference", ["Veg", "Non-Veg"])

if st.sidebar.button("Generate Plan"):
    # ---------- Calorie Estimate ----------
    calories = calculate_calories(gender, weight, height, age, activity_level)
    st.header(f"🔥 Estimated Daily Calorie Need: *{calories} kcal*")

    # ---------- Meal Plan ----------
    st.subheader("🍽 Recommended Meal Plan (Sample)")
    filtered_meals = meals_df[meals_df["Type"] == diet]
    suggested_meals = filtered_meals.sample(3)
    st.dataframe(suggested_meals[["Meal", "Calories", "Protein (g)"]])

    # ---------- Visual: Macros Pie Chart ----------
    total_calories = suggested_meals["Calories"].sum()
    total_protein = suggested_meals["Protein (g)"].sum()
    carb_ratio = 0.5 * total_calories
    fat_ratio = 0.2 * total_calories
    protein_ratio = total_protein * 4  # 1g protein = 4 kcal
    
    labels = ['Carbs (approx.)', 'Fats (approx.)', 'Protein (actual)']
    sizes = [carb_ratio, fat_ratio, protein_ratio]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

    # ---------- Universal Workout Plan (Muscle Gain) ----------
    st.subheader("🏋️ Muscle-Gain Workout Plan (3 Days a Week)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### *Day 1: Push*")
        st.write("""
        - Bench Press / Dumbbell Press: 4x6-10  
        - Overhead Shoulder Press: 3x8-12  
        - Incline Press: 3x8-12  
        - Lateral Raises: 3x12-15  
        - Triceps Pushdown / Dips: 3x10-15
        """)

    with col2:
        st.markdown("### *Day 2: Pull*")
        st.write("""
        - Pull-ups / Lat Pulldown: 4x6-10  
        - Barbell / Dumbbell Row: 4x8-12  
        - Face Pulls: 3x12-15  
        - Curls: 3x10-15  
        - Hammer Curls: 3x10-12
        """)

    with col3:
        st.markdown("### *Day 3: Legs*")
        st.write("""
        - Squats: 4x6-10  
        - Romanian Deadlifts: 4x8-12  
        - Lunges: 3x10-12  
        - Leg Press: 3x10-15  
        - Calf Raises: 3x12-20
        """)

    # ---------- Notes Section ----------
    st.subheader("📌 Key Health Notes:")
    st.markdown("""
    - *Underweight:* Focus on progressive overload, eat in a calorie surplus.  
    - *Average:* Combine strength & hypertrophy, track protein intake.  
    - *Overweight:* Prioritize clean form, manage calories responsibly.
    """)

    st.subheader("💧 Nutrition & Recovery Tips:")
    st.markdown("""
    - *Protein:* 1.6-2.2g per kg of body weight daily  
    - *Calories:* Eat slightly above maintenance (250-500 surplus)  
    - *Sleep:* 7-9 hours/night  
    - *Hydrate:* Proper hydration improves recovery
    """)

    # ---------- Styling Footer ----------
    st.markdown("---")
    st.markdown("<center>Created for AI Exhibition | Simple, Practical, Professional</center>", unsafe_allow_html=True)