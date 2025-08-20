import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

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
        'meal_ratings': {}
    }

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

# Load meal dataset (sample data - you would replace with your actual data)
@st.cache_data
def load_meals():
    # Sample meal data - replace with your actual CSV loading
    meals_data = {
        'Meal': ['Oatmeal with Berries', 'Grilled Chicken Salad', 'Protein Shake', 'Vegetable Stir Fry', 
                'Greek Yogurt Parfait', 'Salmon with Quinoa', 'Tofu Scramble', 'Turkey Sandwich'],
        'Type': ['Veg', 'Non-Veg', 'Veg', 'Veg', 'Veg', 'Non-Veg', 'Veg', 'Non-Veg'],
        'Calories': [350, 420, 180, 320, 280, 450, 310, 380],
        'Protein (g)': [12, 35, 25, 15, 20, 40, 22, 30],
        'Carbs (g)': [55, 20, 8, 45, 35, 35, 25, 40],
        'Fat (g)': [8, 22, 3, 12, 10, 20, 18, 15]
    }
    return pd.DataFrame(meals_data)

meals_df = load_meals()

# Filter meals by diet type
if diet_type == 'Both':
    filtered_meals = meals_df
else:
    filtered_meals = meals_df[meals_df['Type'].str.lower() == diet_type.lower()]

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
            st.markdown('<div class="info-box">ℹ️ You're getting plenty of sleep. Make sure it's quality rest.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ Great! You're getting adequate sleep.</div>', unsafe_allow_html=True)
    
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
    st.markdown('<h2 class="subheader">🍽️ Meal Recommendations</h2>', unsafe_allow_html=True)
    
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
    
    # Meal recommendations
    st.markdown(f"#### 🍱 Recommended Meals ({diet_type})")
    
    # Add filtering options
    col1, col2 = st.columns(2)
    with col1:
        min_cals = st.slider("Min Calories", 0, 1000, 200, key="min_cals")
    with col2:
        max_cals = st.slider("Max Calories", 0, 1000, 600, key="max_cals", value=600)
    
    # Filter meals based on calories
    cals_filtered_meals = filtered_meals[
        (filtered_meals['Calories'] >= min_cals) & 
        (filtered_meals['Calories'] <= max_cals)
    ]
    
    # Display meals in a nice grid
    cols = st.columns(2)
    for idx, meal in cals_filtered_meals.iterrows():
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"##### {meal['Meal']} ({meal['Type']})")
                st.markdown(f"**{meal['Calories']} kcal** | P: {meal['Protein (g)']}g | C: {meal['Carbs (g)']}g | F: {meal['Fat (g)']}g")
                
                # Rating system
                if meal['Meal'] not in st.session_state.user_data['meal_ratings']:
                    st.session_state.user_data['meal_ratings'][meal['Meal']] = 0
                
                rating = st.slider(
                    f"How do you like {meal['Meal']}?",
                    0, 5, st.session_state.user_data['meal_ratings'][meal['Meal']],
                    key=f"rating_{meal['Meal']}"
                )
                st.session_state.user_data['meal_ratings'][meal['Meal']] = rating
                
                st.markdown("---")

with tab3:  # Workouts tab
    st.markdown('<h2 class="subheader">💪 Workout Plan</h2>', unsafe_allow_html=True)
    
    # Workout recommendations based on activity level and goal
    if activity_level == 'Sedentary':
        workout_plan = {
            "Monday": "10-min Morning Stretch, 15-min Walk",
            "Tuesday": "Rest Day",
            "Wednesday": "15-min Yoga, 10-min Breathing Exercises",
            "Thursday": "Rest Day",
            "Friday": "20-min Light Cardio",
            "Saturday": "15-min Stretching",
            "Sunday": "Rest Day"
        }
    elif activity_level == 'Light Exercise':
        workout_plan = {
            "Monday": "20 Squats, 20 Lunges, 15 Knee Push-ups",
            "Tuesday": "20-min Walk or Jog",
            "Wednesday": "15-min Yoga, 10-min Core Exercises",
            "Thursday": "Rest Day",
            "Friday": "30-min Cardio (choice of activity)",
            "Saturday": "Full Body Stretch (20 min)",
            "Sunday": "Rest Day"
        }
    elif activity_level == 'Moderate':
        workout_plan = {
            "Monday": "Upper Body Strength Training (40 min)",
            "Tuesday": "30-min Cardio",
            "Wednesday": "Lower Body Strength Training (40 min)",
            "Thursday": "Active Recovery (yoga or light swim)",
            "Friday": "Full Body Circuit Training (45 min)",
            "Saturday": "45-min Cardio (choice of activity)",
            "Sunday": "Rest Day"
        }
    else:  # Heavy Exercise or Athlete
        workout_plan = {
            "Monday": "Chest & Triceps (60 min)",
            "Tuesday": "Back & Biceps (60 min)",
            "Wednesday": "Leg Day (60 min)",
            "Thursday": "Shoulders & Core (60 min)",
            "Friday": "HIIT Cardio (45 min)",
            "Saturday": "Active Recovery (yoga or light activity)",
            "Sunday": "Rest Day"
        }
    
    # Display workout plan
    st.markdown("#### 📅 Weekly Workout Schedule")
    
    for day, workout in workout_plan.items():
        with st.expander(f"{day}: {workout.split(',')[0]}..."):
            st.write(workout)
            completed = st.checkbox(f"Completed {day}'s workout", key=f"workout_{day}")
            if completed and day not in st.session_state.user_data['workout_history']:
                if st.button(f"Log {day}'s Workout", key=f"log_{day}"):
                    st.session_state.user_data['workout_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'day': day,
                        'workout': workout
                    })
                    st.success(f"{day}'s workout logged successfully!")

with tab4:  # Progress tab
    st.markdown('<h2 class="subheader">📊 Your Progress</h2>', unsafe_allow_html=True)
    
    # Generate sample progress data (in a real app, this would come from user input)
    dates = pd.date_range(start=(datetime.now() - timedelta(days=30)), end=datetime.now())
    weight_progress = [weight - 0.1*i for i in range(30)] if goal == 'Lose Fat' else [weight + 0.05*i for i in range(30)]
    
    # Weight progress chart
    st.markdown("#### ⚖️ Weight Trend")
    fig_weight = px.line(
        x=dates, y=weight_progress,
        labels={'x': 'Date', 'y': 'Weight (kg)'},
        title="30-Day Weight Progress"
    )
    st.plotly_chart(fig_weight, use_container_width=True)
    
    # BMI chart
    st.markdown("#### 📈 BMI Classification")
    bmi_categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
    bmi_ranges = [18.5, 24.9, 29.9, 40]
    
    fig_bmi = go.Figure()
    fig_bmi.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "BMI"},
        gauge = {
            'axis': {'range': [None, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 18.5], 'color': "lightgray"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "yellow"},
                {'range': [30, 40], 'color': "orange"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': bmi}}))
    
    st.plotly_chart(fig_bmi, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by Savan, Rehan, Aadil, Akash & Athul | AI Fitness Assistant v2.0</p>", unsafe_allow_html=True)
