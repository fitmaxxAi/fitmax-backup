import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="FitLife AI Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #A23B72;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .meal-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .workout-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid #FF6B6B;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .progress-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4b6cb7 0%, #182848 100%);
        color: white;
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4ECDC4, #556270);
    }
    .user-welcome {
        font-size: 1.5rem;
        color: #2E86AB;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    default_data = {
        'name': 'Fitness Enthusiast',
        'age': 25,
        'gender': 'Male',
        'height': 175,
        'current_weight': 70,
        'goal_weight': 65,
        'activity_level': 'Moderate',
        'goal_type': 'Weight Loss',
        'health_condition': 'Healthy',
        'water_intake': 0,
        'calorie_target': 2000,
        'protein_target': 150,
        'carbs_target': 250,
        'fat_target': 67,
        'daily_calories': 0,
        'food_log': []
    }
    
    for key, value in default_data.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    if 'meals' not in st.session_state:
        st.session_state.meals = []
    if 'workouts' not in st.session_state:
        st.session_state.workouts = []
    if 'exercises' not in st.session_state:
        st.session_state.exercises = []

initialize_session_state()

# Helper functions
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'Sedentary': 1.2, 'Light': 1.375, 'Moderate': 1.55, 'Active': 1.725, 'Very Active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.55)

def calculate_calorie_target(current_weight, goal_weight, tdee, goal_type):
    weight_difference = current_weight - goal_weight
    
    if goal_type == 'Weight Loss':
        deficit = min(1000, max(500, abs(weight_difference) * 100))
        return max(1200, tdee - deficit)
    elif goal_type == 'Weight Gain':
        surplus = min(500, max(250, abs(weight_difference) * 100))
        return tdee + surplus
    else:
        return tdee

def calculate_macro_targets(calorie_target, goal_type):
    if goal_type == 'Weight Loss':
        ratios = {'protein': 0.35, 'carbs': 0.40, 'fat': 0.25}
    elif goal_type == 'Weight Gain':
        ratios = {'protein': 0.30, 'carbs': 0.50, 'fat': 0.20}
    else:
        ratios = {'protein': 0.25, 'carbs': 0.50, 'fat': 0.25}
    
    return {
        'protein_target': round(calorie_target * ratios['protein'] / 4),
        'carbs_target': round(calorie_target * ratios['carbs'] / 4),
        'fat_target': round(calorie_target * ratios['fat'] / 9)
    }

def get_food_recommendations(goal_type, health_condition):
    recommendations = {
        'Weight Loss': [
            'Leafy greens (spinach, kale)',
            'Lean proteins (chicken breast, fish)',
            'Whole grains (quinoa, brown rice)',
            'Berries and low-sugar fruits',
            'Greek yogurt and cottage cheese'
        ],
        'Weight Gain': [
            'Nuts and nut butters',
            'Avocados and healthy oils',
            'Whole milk and full-fat dairy',
            'Complex carbs (sweet potatoes, oats)',
            'Protein shakes with banana'
        ],
        'Weight Maintenance': [
            'Balanced meals with all macros',
            'Colorful vegetables',
            'Lean proteins and healthy fats',
            'Whole fruits in moderation',
            'Hydrating foods like cucumbers'
        ]
    }
    
    health_modifiers = {
        'Diabetes': ['Low glycemic index foods', 'High fiber vegetables', 'Lean proteins'],
        'Hypertension': ['Low sodium foods', 'Potassium-rich foods', 'Whole grains'],
        'Heart Condition': ['Omega-3 rich foods', 'Low saturated fats', 'Fiber-rich foods'],
        'Healthy': ['Varied balanced diet', 'Colorful fruits and vegetables', 'Lean proteins']
    }
    
    base_recommendations = recommendations.get(goal_type, [])
    health_recommendations = health_modifiers.get(health_condition, [])
    
    return base_recommendations + health_recommendations

def generate_meal_plan(calorie_target, macro_targets, goal_type, health_condition):
    meals = []
    meal_templates = {
        'Weight Loss': {
            'Breakfast': 'Greek Yogurt with Berries and Chia Seeds',
            'Lunch': 'Grilled Chicken Salad with Quinoa',
            'Dinner': 'Baked Salmon with Roasted Vegetables',
            'Snack': 'Apple with Almond Butter'
        },
        'Weight Gain': {
            'Breakfast': 'Oatmeal with Banana and Peanut Butter',
            'Lunch': 'Beef and Vegetable Stir-fry with Rice',
            'Dinner': 'Chicken with Sweet Potato and Avocado',
            'Snack': 'Protein Shake with Oats'
        },
        'Weight Maintenance': {
            'Breakfast': 'Whole Grain Toast with Eggs and Avocado',
            'Lunch': 'Turkey and Hummus Wrap with Side Salad',
            'Dinner': 'Fish with Quinoa and Steamed Vegetables',
            'Snack': 'Greek Yogurt with Nuts'
        }
    }
    
    template = meal_templates.get(goal_type, meal_templates['Weight Maintenance'])
    distributions = {'Breakfast': 0.25, 'Lunch': 0.35, 'Dinner': 0.30, 'Snack': 0.10}
    
    for meal_type, distribution in distributions.items():
        meals.append({
            'meal': meal_type,
            'name': template[meal_type],
            'calories': round(calorie_target * distribution),
            'protein': round(macro_targets['protein_target'] * distribution),
            'carbs': round(macro_targets['carbs_target'] * distribution),
            'fat': round(macro_targets['fat_target'] * distribution)
        })
    
    return meals

def generate_workout_plan(goal_type, health_condition, fitness_level):
    workouts = []
    
    workout_templates = {
        'Weight Loss': {
            'Healthy': [
                {'day': 'Monday', 'type': 'Cardio', 'duration': 45, 'description': 'Running or Cycling', 'intensity': 'High'},
                {'day': 'Tuesday', 'type': 'Strength', 'duration': 30, 'description': 'Full Body Circuit', 'intensity': 'Medium'},
                {'day': 'Wednesday', 'type': 'HIIT', 'duration': 30, 'description': 'Interval Training', 'intensity': 'High'},
                {'day': 'Thursday', 'type': 'Active Recovery', 'duration': 30, 'description': 'Yoga or Stretching', 'intensity': 'Low'},
                {'day': 'Friday', 'type': 'Strength', 'duration': 40, 'description': 'Upper Body Focus', 'intensity': 'Medium'},
                {'day': 'Saturday', 'type': 'Cardio', 'duration': 60, 'description': 'Swimming or Hiking', 'intensity': 'Medium'},
                {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
            ],
            'Diabetes': [
                {'day': 'Monday', 'type': 'Walking', 'duration': 30, 'description': 'Brisk Walking', 'intensity': 'Low'},
                {'day': 'Tuesday', 'type': 'Strength', 'duration': 25, 'description': 'Light Weights', 'intensity': 'Low'},
                {'day': 'Wednesday', 'type': 'Yoga', 'duration': 40, 'description': 'Gentle Yoga', 'intensity': 'Low'},
                {'day': 'Thursday', 'type': 'Rest', 'duration': 0, 'description': 'Rest Day', 'intensity': 'None'},
                {'day': 'Friday', 'type': 'Walking', 'duration': 35, 'description': 'Moderate Pace', 'intensity': 'Medium'},
                {'day': 'Saturday', 'type': 'Swimming', 'duration': 30, 'description': 'Light Swimming', 'intensity': 'Low'},
                {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
            ]
        },
        'Weight Gain': {
            'Healthy': [
                {'day': 'Monday', 'type': 'Strength', 'duration': 60, 'description': 'Chest & Triceps', 'intensity': 'High'},
                {'day': 'Tuesday', 'type': 'Strength', 'duration': 60, 'description': 'Back & Biceps', 'intensity': 'High'},
                {'day': 'Wednesday', 'type': 'Cardio', 'duration': 20, 'description': 'Light Cardio', 'intensity': 'Low'},
                {'day': 'Thursday', 'type': 'Strength', 'duration': 60, 'description': 'Legs & Shoulders', 'intensity': 'High'},
                {'day': 'Friday', 'type': 'Strength', 'duration': 45, 'description': 'Full Body', 'intensity': 'Medium'},
                {'day': 'Saturday', 'type': 'Active Recovery', 'duration': 30, 'description': 'Walking or Yoga', 'intensity': 'Low'},
                {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
            ]
        }
    }
    
    # Default template if specific combination not found
    default_template = [
        {'day': 'Monday', 'type': 'Strength', 'duration': 45, 'description': 'Upper Body', 'intensity': 'Medium'},
        {'day': 'Tuesday', 'type': 'Cardio', 'duration': 40, 'description': 'Running', 'intensity': 'Medium'},
        {'day': 'Wednesday', 'type': 'Strength', 'duration': 45, 'description': 'Lower Body', 'intensity': 'Medium'},
        {'day': 'Thursday', 'type': 'Yoga', 'duration': 60, 'description': 'Flexibility', 'intensity': 'Low'},
        {'day': 'Friday', 'type': 'Full Body', 'duration': 50, 'description': 'Circuit Training', 'intensity': 'Medium'},
        {'day': 'Saturday', 'type': 'Outdoor', 'duration': 90, 'description': 'Hiking/Sports', 'intensity': 'High'},
        {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
    ]
    
    template = workout_templates.get(goal_type, {}).get(health_condition, default_template)
    return template

def generate_exercises(workout_type):
    exercises_db = {
        'Strength': ['Bench Press 3x8-12', 'Squats 4x8-10', 'Deadlifts 3x6-8', 'Pull-ups 3xMax'],
        'Cardio': ['Running 30min', 'Cycling 45min', 'Elliptical 30min', 'Rowing 25min'],
        'HIIT': ['Burpees 45s/15s', 'Jump Squats 30s/30s', 'Mountain Climbers 40s/20s'],
        'Yoga': ['Sun Salutations', 'Warrior Series', 'Balance Poses', 'Flexibility Flow'],
        'Walking': ['Brisk Walk 30min', 'Interval Walking', 'Incline Walking'],
        'Swimming': ['Freestyle Laps', 'Breaststroke', 'Water Aerobics']
    }
    return exercises_db.get(workout_type, ['Custom exercises based on your level'])

# Main app layout
st.markdown('<div class="main-header">💪 FitLife AI Planner</div>', unsafe_allow_html=True)
st.markdown(f'<div class="user-welcome">Welcome, {st.session_state.name}!</div>', unsafe_allow_html=True)

# Sidebar - User Profile
with st.sidebar:
    st.markdown("### 👤 User Profile")
    
    with st.form("user_profile"):
        name = st.text_input("Your Name", st.session_state.name)
        age = st.number_input("Age", min_value=18, max_value=100, value=st.session_state.age)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                            index=["Male", "Female", "Other"].index(st.session_state.gender))
        height = st.slider("Height (cm)", 140, 220, st.session_state.height)
        current_weight = st.slider("Current Weight (kg)", 40, 150, st.session_state.current_weight)
        goal_weight = st.slider("Goal Weight (kg)", 40, 150, st.session_state.goal_weight)
        activity_level = st.selectbox("Activity Level", 
                                    ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                    index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(st.session_state.activity_level))
        goal_type = st.selectbox("Goal Type", 
                                ["Weight Loss", "Weight Maintenance", "Weight Gain"],
                                index=["Weight Loss", "Weight Maintenance", "Weight Gain"].index(st.session_state.goal_type))
        health_condition = st.selectbox("Health Condition", 
                                      ["Healthy", "Diabetes", "Hypertension", "Heart Condition"],
                                      index=["Healthy", "Diabetes", "Hypertension", "Heart Condition"].index(st.session_state.health_condition))
        fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"], index=0)
        
        if st.form_submit_button("🚀 Update Profile"):
            st.session_state.update({
                'name': name, 'age': age, 'gender': gender, 'height': height,
                'current_weight': current_weight, 'goal_weight': goal_weight,
                'activity_level': activity_level, 'goal_type': goal_type,
                'health_condition': health_condition
            })
            
            # Recalculate everything
            bmr = calculate_bmr(current_weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level)
            calorie_target = calculate_calorie_target(current_weight, goal_weight, tdee, goal_type)
            macro_targets = calculate_macro_targets(calorie_target, goal_type)
            
            st.session_state.update({
                'calorie_target': calorie_target,
                'protein_target': macro_targets['protein_target'],
                'carbs_target': macro_targets['carbs_target'],
                'fat_target': macro_targets['fat_target']
            })
            
            st.session_state.meals = generate_meal_plan(calorie_target, macro_targets, goal_type, health_condition)
            st.session_state.workouts = generate_workout_plan(goal_type, health_condition, fitness_level)
            
            today_workout = next((w for w in st.session_state.workouts if w['day'] == datetime.now().strftime('%A')), None)
            if today_workout:
                st.session_state.exercises = generate_exercises(today_workout['type'])
            
            st.success("Profile updated successfully!")

    # Calorie Tracker in Sidebar
    st.markdown("### 📊 Calorie Tracker")
    food_name = st.text_input("Food Item")
    food_calories = st.number_input("Calories", min_value=0, max_value=2000, value=0)
    
    if st.button("➕ Add Food"):
        if food_name and food_calories > 0:
            st.session_state.food_log.append({'name': food_name, 'calories': food_calories})
            st.session_state.daily_calories += food_calories
            st.success(f"Added {food_name} ({food_calories} kcal)")
    
    st.metric("Today's Calories", f"{st.session_state.daily_calories} / {st.session_state.calorie_target}")
    progress = min(1.0, st.session_state.daily_calories / st.session_state.calorie_target)
    st.progress(progress)

# Main content - Tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "🍽️ Nutrition", "💪 Workouts", "📊 Progress"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📊 Fitness Overview</div>', unsafe_allow_html=True)
        
        # Metrics in a grid
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            bmr = calculate_bmr(st.session_state.current_weight, st.session_state.height, 
                              st.session_state.age, st.session_state.gender)
            st.markdown(f'<div class="metric-card">BMR<br><h3>{bmr:.0f} kcal</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Current Weight<br><h3>{st.session_state.current_weight} kg</h3></div>', unsafe_allow_html=True)
        
        with metrics_col2:
            tdee = calculate_tdee(bmr, st.session_state.activity_level)
            st.markdown(f'<div class="metric-card">TDEE<br><h3>{tdee:.0f} kcal</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Goal Weight<br><h3>{st.session_state.goal_weight} kg</h3></div>', unsafe_allow_html=True)
        
        with metrics_col3:
            st.markdown(f'<div class="metric-card">Calorie Target<br><h3>{st.session_state.calorie_target} kcal</h3></div>', unsafe_allow_html=True)
            weight_diff = st.session_state.current_weight - st.session_state.goal_weight
            st.markdown(f'<div class="metric-card">Weight to Go<br><h3>{abs(weight_diff):.1f} kg</h3></div>', unsafe_allow_html=True)
        
        # Progress tracking
        st.markdown('<div class="section-header">🎯 Progress Tracking</div>', unsafe_allow_html=True)
        
        progress_col1, progress_col2 = st.columns(2)
        
        with progress_col1:
            max_w = max(st.session_state.current_weight, st.session_state.goal_weight)
            min_w = min(st.session_state.current_weight, st.session_state.goal_weight)
            if max_w > min_w:
                if st.session_state.goal_type == 'Weight Loss':
                    progress = (max_w - st.session_state.current_weight) / (max_w - min_w)
                else:
                    progress = (st.session_state.current_weight - min_w) / (max_w - min_w)
            else:
                progress = 1.0
            st.progress(min(1.0, max(0.0, progress)))
            st.write(f"**Weight Goal:** {min(100, max(0, progress*100)):.1f}% complete")
        
        with progress_col2:
            water_progress = min(1.0, st.session_state.water_intake / 8.0)
            st.progress(water_progress)
            st.write(f"**Water Intake:** {st.session_state.water_intake}/8 cups")
            st.session_state.water_intake = st.slider("Update water intake", 0, 12, st.session_state.water_intake)
    
    with col2:
        st.markdown('<div class="section-header">💡 Today\'s Summary</div>', unsafe_allow_html=True)
        
        # Quick overview cards
        st.markdown(f'<div class="meal-card"><strong>🍽️ Meals Planned:</strong> {len(st.session_state.meals)}</div>', unsafe_allow_html=True)
        
        today_workout = next((w for w in st.session_state.workouts if w['day'] == datetime.now().strftime('%A')), None)
        if today_workout:
            st.markdown(f'<div class="workout-card"><strong>💪 Today\'s Workout:</strong> {today_workout["type"]} ({today_workout["duration"]}min)</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="metric-card">Calories Today<br><h3>{st.session_state.daily_calories}/{st.session_state.calorie_target}</h3></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">🍽️ Nutrition Plan</div>', unsafe_allow_html=True)
    
    if st.session_state.meals:
        meal_col1, meal_col2 = st.columns(2)
        
        for i, meal in enumerate(st.session_state.meals):
            col = meal_col1 if i % 2 == 0 else meal_col2
            with col:
                st.markdown(f'''
                <div class="meal-card">
                    <h4>🍽️ {meal['meal']}: {meal['name']}</h4>
                    <p>Calories: {meal['calories']} kcal</p>
                    <p>Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fat: {meal['fat']}g</p>
                </div>
                ''', unsafe_allow_html=True)
    
    # Food Recommendations
    st.markdown('<div class="section-header">🌟 Recommended Foods</div>', unsafe_allow_html=True)
    recommendations = get_food_recommendations(st.session_state.goal_type, st.session_state.health_condition)
    
    rec_col1, rec_col2 = st.columns(2)
    for i, rec in enumerate(recommendations):
        col = rec_col1 if i % 2 == 0 else rec_col2
        with col:
            st.write(f"✅ {rec}")

with tab3:
    st.markdown('<div class="section-header">💪 Workout Plan</div>', unsafe_allow_html=True)
    
    if st.session_state.workouts:
        # Today's workout highlighted
        today = datetime.now().strftime('%A')
        today_workout = next((w for w in st.session_state.workouts if w['day'] == today), None)
        
        if today_workout:
            st.markdown(f'<div class="workout-card"><h3>🎯 Today ({today}): {today_workout["type"]}</h3>', unsafe_allow_html=True)
            st.write(f"**Duration:** {today_workout['duration']} minutes")
            st.write(f"**Intensity:** {today_workout['intensity']}")
            st.write(f"**Description:** {today_workout['description']}")
            
            if today_workout['type'] != 'Rest' and st.session_state.exercises:
                st.write("**Recommended Exercises:**")
                for exercise in st.session_state.exercises:
                    st.write(f"• {exercise}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekly schedule
        st.markdown('<div class="section-header">📅 Weekly Schedule</div>', unsafe_allow_html=True)
        workout_df = pd.DataFrame(st.session_state.workouts)
        st.dataframe(workout_df, use_container_width=True)

with tab4:
    st.markdown('<div class="section-header">📊 Progress Analytics</div>', unsafe_allow_html=True)
    
    # Nutrition progress
    if st.session_state.meals:
        total_cals = sum(meal['calories'] for meal in st.session_state.meals)
        total_protein = sum(meal['protein'] for meal in st.session_state.meals)
        total_carbs = sum(meal['carbs'] for meal in st.session_state.meals)
        total_fat = sum(meal['fat'] for meal in st.session_state.meals)
        
        progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4)
        
        with progress_col1:
            st.metric("Calories", f"{total_cals}", f"{total_cals - st.session_state.calorie_target}")
            st.progress(min(1.0, total_cals / st.session_state.calorie_target))
        
        with progress_col2:
            st.metric("Protein", f"{total_protein}g", f"{total_protein - st.session_state.protein_target}g")
            st.progress(min(1.0, total_protein / st.session_state.protein_target))
        
        with progress_col3:
            st.metric("Carbs", f"{total_carbs}g", f"{total_carbs - st.session_state.carbs_target}g")
            st.progress(min(1.0, total_carbs / st.session_state.carbs_target))
        
        with progress_col4:
            st.metric("Fat", f"{total_fat}g", f"{total_fat - st.session_state.fat_target}g")
            st.progress(min(1.0, total_fat / st.session_state.fat_target))
    
    # Food log
    if st.session_state.food_log:
        st.markdown('<div class="section-header">📝 Food Log</div>', unsafe_allow_html=True)
        food_df = pd.DataFrame(st.session_state.food_log)
        st.dataframe(food_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### 💡 Tips for Success")
if st.session_state.goal_type == 'Weight Loss':
    st.info("""
    - Stay consistent with your calorie deficit
    - Combine cardio and strength training
    - Get enough protein to preserve muscle mass
    - Drink water before meals to reduce appetite
    - Track your progress weekly, not daily
    """)
elif st.session_state.goal_type == 'Weight Gain':
    st.info("""
    - Eat calorie-dense foods regularly
    - Focus on progressive overload in workouts
    - Consider protein supplements if needed
    - Don't skip meals - eat every 3-4 hours
    - Be patient - healthy weight gain takes time
    """)
else:
    st.info("""
    - Maintain balanced nutrition
    - Stay active with varied exercises
    - Listen to your body's hunger signals
    - Regular health check-ups
    - Enjoy your food and stay hydrated
    """)
    
