import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import requests
from io import StringIO

# Page setup
st.set_page_config(
    page_title="AI Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1f77b4; text-align: center;}
    .subheader {font-size: 1.5rem; color: #2ca02c; border-bottom: 2px solid #ff7f0e; padding-bottom: 0.3rem;}
    .metric-label {font-weight: bold; color: #7f7f7f;}
    .metric-value {font-size: 1.2rem; color: #1f77b4;}
    .success-box {background-color: #d4edda; padding: 15px; border-radius: 5px; border-left: 5px solid #28a745;}
    .warning-box {background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107;}
    .info-box {background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 5px solid #17a2b8;}
    .stProgress > div > div > div > div {background-color: #1f77b4;}
    .food-card {border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background: white;}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">💪 AI Personalized Fitness Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Your all-in-one nutrition and workout planning solution")

# Initialize session state for persistence
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'sleep_history': [],
        'water_history': [],
        'workout_history': [],
        'meal_ratings': {},
        'favorite_meals': []
    }

# Load Indian Food Dataset (Sample data - replace with actual Kaggle dataset)
@st.cache_data
def load_indian_food_data():
    # This is sample data - you would replace this with your actual Kaggle dataset
    # For now, I'm creating a comprehensive sample dataset with Indian foods
    indian_foods = {
        'name': [
            'Masala Dosa', 'Idli with Sambar', 'Paneer Butter Masala', 'Chole Bhature',
            'Biryani', 'Palak Paneer', 'Dal Tadka', 'Vegetable Pulao',
            'Upma', 'Pongal', 'Rava Kesari', 'Medu Vada',
            'Butter Chicken', 'Tandoori Roti', 'Aloo Gobi', 'Rajma Chawal',
            'Pav Bhaji', 'Vada Pav', 'Misal Pav', 'Dhokla',
            'Khaman', 'Handvo', 'Thepla', 'Undhiyu'
        ],
        'type': [
            'South Indian', 'South Indian', 'North Indian', 'North Indian',
            'Hyderabadi', 'North Indian', 'North Indian', 'North Indian',
            'South Indian', 'South Indian', 'South Indian', 'South Indian',
            'North Indian', 'North Indian', 'North Indian', 'North Indian',
            'Street Food', 'Street Food', 'Street Food', 'Gujarati',
            'Gujarati', 'Gujarati', 'Gujarati', 'Gujarati'
        ],
        'category': [
            'Breakfast', 'Breakfast', 'Main Course', 'Main Course',
            'Main Course', 'Main Course', 'Main Course', 'Main Course',
            'Breakfast', 'Breakfast', 'Dessert', 'Breakfast',
            'Main Course', 'Bread', 'Main Course', 'Main Course',
            'Snack', 'Snack', 'Snack', 'Snack',
            'Snack', 'Snack', 'Breakfast', 'Main Course'
        ],
        'diet_type': [
            'Veg', 'Veg', 'Veg', 'Veg',
            'Non-Veg', 'Veg', 'Veg', 'Veg',
            'Veg', 'Veg', 'Veg', 'Veg',
            'Non-Veg', 'Veg', 'Veg', 'Veg',
            'Veg', 'Veg', 'Veg', 'Veg',
            'Veg', 'Veg', 'Veg', 'Veg'
        ],
        'calories': [280, 180, 420, 550, 480, 320, 250, 380, 
                    220, 200, 320, 280, 450, 120, 280, 350,
                    400, 300, 350, 180, 160, 220, 280, 320],
        'protein_g': [8, 12, 25, 15, 30, 22, 12, 10, 
                    6, 8, 4, 10, 35, 4, 8, 15,
                    12, 10, 18, 8, 6, 10, 8, 12],
        'carbs_g': [45, 30, 25, 75, 60, 25, 40, 65,
                  35, 35, 65, 40, 20, 20, 45, 60,
                  60, 45, 50, 30, 25, 35, 45, 50],
        'fat_g': [8, 3, 30, 20, 18, 20, 8, 12,
                10, 5, 8, 12, 25, 2, 10, 10,
                15, 12, 12, 5, 4, 8, 10, 12],
        'prep_time_min': [30, 20, 40, 45, 60, 35, 25, 30,
                        15, 25, 20, 30, 50, 10, 30, 40,
                        35, 20, 40, 30, 25, 35, 20, 50],
        'region': [
            'South', 'South', 'North', 'North', 
            'South', 'North', 'North', 'North',
            'South', 'South', 'South', 'South',
            'North', 'North', 'North', 'North',
            'West', 'West', 'West', 'West',
            'West', 'West', 'West', 'West'
        ]
    }
    return pd.DataFrame(indian_foods)

# Load the data
meals_df = load_indian_food_data()

# Sidebar - User Profile
with st.sidebar:
    st.header('👤 User Profile')
    
    # User info with columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", placeholder="Your Name")
    with col2:
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
    
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    goal = st.selectbox('What is your goal?', ['Gain Muscle', 'Maintain Weight', 'Lose Fat'])
    diet_type = st.selectbox('Diet Preference', ['Both', 'Veg', 'Non-Veg'])
    activity_level = st.selectbox('Activity Level', ['Sedentary', 'Light Exercise', 'Moderate', 'Heavy Exercise', 'Athlete'])
    
    # Cuisine Preference
    cuisine_preference = st.multiselect(
        'Preferred Cuisines',
        ['North Indian', 'South Indian', 'Street Food', 'Gujarati', 'Hyderabadi'],
        default=['North Indian', 'South Indian']
    )
    
    # BMI Calculation
    st.header("📏 Body Metrics")
    height = st.slider("Height (cm)", min_value=100, max_value=250, value=175)
    weight = st.slider("Weight (kg)", min_value=30, max_value=200, value=70)
    
    # Calculate BMI
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
    
    # Display BMI with color coding
    bmi_color = "#28a745" if bmi_status == "Normal" else "#ffc107" if bmi_status == "Overweight" else "#dc3545"
    st.markdown(f"<p style='font-size: 1.2rem;'>Your BMI: <span style='color: {bmi_color}; font-weight: bold;'>{bmi:.1f} ({bmi_status})</span></p>", 
                unsafe_allow_html=True)
    
    # Calculate and display recommended daily calories
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light Exercise': 1.375,
        'Moderate': 1.55,
        'Heavy Exercise': 1.725,
        'Athlete': 1.9
    }
    
    tdee = bmr * activity_multipliers[activity_level]
    
    if goal == 'Lose Fat':
        calorie_target = tdee - 500
    elif goal == 'Gain Muscle':
        calorie_target = tdee + 500
    else:
        calorie_target = tdee
        
    st.markdown(f"<div class='info-box'><span class='metric-label'>Daily Calorie Target:</span> <span class='metric-value'>{calorie_target:.0f} kcal</span></div>", 
                unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "🍽️ Nutrition", "💪 Workouts", "📊 Progress"])

# Filter meals by diet type and cuisine preference
if diet_type == 'Both':
    filtered_meals = meals_df[meals_df['type'].isin(cuisine_preference)]
else:
    filtered_meals = meals_df[
        (meals_df['diet_type'].str.lower() == diet_type.lower()) & 
        (meals_df['type'].isin(cuisine_preference))
    ]

with tab1:  # Dashboard tab
    st.markdown('<h2 class="subheader">Daily Overview</h2>', unsafe_allow_html=True)
    
    # Create metrics columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Calorie Target", f"{calorie_target:.0f} kcal")
    with col2:
        st.metric("Protein Target", "120g")  # Simplified for demo
    with col3:
        st.metric("Current BMI", f"{bmi:.1f}")
    with col4:
        st.metric("Goal", goal)
    
    # Quick meal suggestions
    st.markdown("#### 🍽️ Quick Meal Ideas")
    quick_meals = filtered_meals[filtered_meals['prep_time_min'] <= 30].sample(3)
    for _, meal in quick_meals.iterrows():
        st.markdown(f"""
        <div class='food-card'>
            <b>{meal['name']}</b> ({meal['type']})<br>
            ⏱️ {meal['prep_time_min']} min | 🔥 {meal['calories']} kcal | 🥗 {meal['protein_g']}g protein
        </div>
        """, unsafe_allow_html=True)
    
    # Sleep and water tracking in columns
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="subheader">😴 Sleep Tracking</h3>', unsafe_allow_html=True)
        sleep_hours = st.slider('Hours slept last night', 0.0, 12.0, 7.0, 0.5, key="sleep_slider")
        
        # Add to history
        if st.button("Log Sleep", key="log_sleep"):
            st.session_state.user_data['sleep_history'].append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'hours': sleep_hours
            })
            st.success("Sleep logged successfully!")
        
        # Display sleep quality message
        if sleep_hours < 6:
            st.markdown('<div class="warning-box">⚠️ Try to sleep at least 7–8 hours for proper recovery.</div>', unsafe_allow_html=True)
        elif sleep_hours > 9:
            st.markdown('<div class="info-box">ℹ️ You\'re getting plenty of sleep. Make sure it\'s quality rest.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ Great! You\'re getting adequate sleep.</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="subheader">💧 Hydration Tracker</h3>', unsafe_allow_html=True)
        water_glasses = st.slider('Glasses of water today (1 glass = 250ml)', 0, 15, 4, key="water_slider")
        
        # Add to history
        if st.button("Log Water", key="log_water"):
            st.session_state.user_data['water_history'].append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'glasses': water_glasses
            })
            st.success("Water intake logged successfully!")
        
        # Display water intake progress
        water_progress = water_glasses / 8  # Assuming 8 glasses is the goal
        st.progress(water_progress)
        st.caption(f"{water_glasses}/8 glasses ({water_glasses * 250}ml/{2000}ml)")
        
        if water_glasses < 6:
            st.markdown(f'<div class="warning-box">⚠️ Try to drink more water. You\'re {8 - water_glasses} glasses short of the daily recommendation.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ Awesome! You\'re staying well hydrated.</div>', unsafe_allow_html=True)

with tab2:  # Nutrition tab
    st.markdown('<h2 class="subheader">🍽️ Indian Meal Recommendations</h2>', unsafe_allow_html=True)
    
    # Macronutrient distribution
    st.markdown("#### 📊 Recommended Macronutrient Distribution")
    if goal == 'Lose Fat':
        macros = {'Protein': 40, 'Carbs': 30, 'Fat': 30}
    elif goal == 'Gain Muscle':
        macros = {'Protein': 35, 'Carbs': 45, 'Fat': 20}
    else:  # Maintain weight
        macros = {'Protein': 30, 'Carbs': 40, 'Fat': 30}
    
    fig_macros = px.pie(
        values=list(macros.values()), 
        names=list(macros.keys()), 
        title=f"Macronutrient Distribution for {goal}"
    )
    st.plotly_chart(fig_macros, use_container_width=True)
    
    # Meal filtering options
    st.markdown("#### 🔍 Filter Meals")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        meal_category = st.selectbox("Meal Category", ["All", "Breakfast", "Main Course", "Snack", "Dessert"])
    with col2:
        min_cals = st.slider("Min Calories", 0, 1000, 150, key="min_cals")
    with col3:
        max_cals = st.slider("Max Calories", 0, 1000, 600, key="max_cals", value=600)
    
    # Apply filters
    filtered = filtered_meals.copy()
    if meal_category != "All":
        filtered = filtered[filtered['category'] == meal_category]
    filtered = filtered[(filtered['calories'] >= min_cals) & (filtered['calories'] <= max_cals)]
    
    # Display meals
    st.markdown(f"#### 🍱 Recommended {meal_category} Meals ({len(filtered)} found)")
    
    for _, meal in filtered.iterrows():
        with st.expander(f"{meal['name']} ({meal['type']}) - {meal['calories']} kcal"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Nutrition Information:**
                - Calories: {meal['calories']} kcal
                - Protein: {meal['protein_g']}g
                - Carbs: {meal['carbs_g']}g
                - Fat: {meal['fat_g']}g
                - Prep Time: {meal['prep_time_min']} minutes
                """)
            with col2:
                # Rating system
                if meal['name'] not in st.session_state.user_data['meal_ratings']:
                    st.session_state.user_data['meal_ratings'][meal['name']] = 0
                
                rating = st.slider(
                    "How do you like this meal?",
                    0, 5, st.session_state.user_data['meal_ratings'][meal['name']],
                    key=f"rating_{meal['name']}"
                )
                st.session_state.user_data['meal_ratings'][meal['name']] = rating
                
                if st.button(f"Add to Favorites ❤️", key=f"fav_{meal['name']}"):
                    if meal['name'] not in st.session_state.user_data['favorite_meals']:
                        st.session_state.user_data['favorite_meals'].append(meal['name'])
                        st.success("Added to favorites!")
    
    # Favorite meals section
    if st.session_state.user_data['favorite_meals']:
        st.markdown("#### ❤️ Your Favorite Meals")
        favorite_meals = meals_df[meals_df['name'].isin(st.session_state.user_data['favorite_meals'])]
        for _, meal in favorite_meals.iterrows():
            st.markdown(f"- **{meal['name']}** ({meal['calories']} kcal)")

# ... (rest of the code for workouts and progress tabs remains the same)
# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by Savan, Rehan, Aadil, Akash & Athul | AI Fitness Assistant v2.0</p>", unsafe_allow_html=True)
