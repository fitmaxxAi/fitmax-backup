import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="AI Meal & Workout Planner",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #A23B72;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .meal-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .workout-card {
        background-color: #fff0f5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'age': 30,
        'gender': 'Male',
        'height': 175,
        'current_weight': 70,
        'goal_weight': 65,
        'activity_level': 'Moderate',
        'goal_type': 'Weight Loss',
        'water_intake': 0,
        'calorie_target': 2000,
        'protein_target': 150,
        'carbs_target': 250,
        'fat_target': 67
    }

if 'meals' not in st.session_state:
    st.session_state.meals = []
if 'workouts' not in st.session_state:
    st.session_state.workouts = []
if 'exercises' not in st.session_state:
    st.session_state.exercises = []

# Helper functions
def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate"""
    if gender == 'Male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.55)

def calculate_calorie_target(current_weight, goal_weight, tdee, goal_type):
    """Calculate calorie target based on weight goals"""
    weight_difference = current_weight - goal_weight
    
    if goal_type == 'Weight Loss':
        # Safe weight loss: 0.5-1kg per week (500-1000 calorie deficit)
        deficit = min(1000, max(500, abs(weight_difference) * 100))
        return max(1200, tdee - deficit)
    
    elif goal_type == 'Weight Gain':
        # Safe weight gain: 0.25-0.5kg per week (250-500 calorie surplus)
        surplus = min(500, max(250, abs(weight_difference) * 100))
        return tdee + surplus
    
    else:  # Maintenance
        return tdee

def calculate_macro_targets(calorie_target, goal_type):
    """Calculate macronutrient targets"""
    if goal_type == 'Weight Loss':
        protein_ratio = 0.35
        carbs_ratio = 0.40
        fat_ratio = 0.25
    elif goal_type == 'Weight Gain':
        protein_ratio = 0.30
        carbs_ratio = 0.50
        fat_ratio = 0.20
    else:  # Maintenance
        protein_ratio = 0.25
        carbs_ratio = 0.50
        fat_ratio = 0.25
    
    protein_cals = calorie_target * protein_ratio
    carbs_cals = calorie_target * carbs_ratio
    fat_cals = calorie_target * fat_ratio
    
    return {
        'protein': round(protein_cals / 4),
        'carbs': round(carbs_cals / 4),
        'fat': round(fat_cals / 9)
    }

def generate_meal_plan(calorie_target, macro_targets):
    """Generate sample meal plan based on calorie target"""
    meals = []
    
    # Breakfast (25% of calories)
    breakfast_cals = calorie_target * 0.25
    meals.append({
        'meal': 'Breakfast',
        'name': 'Greek Yogurt with Berries and Oats',
        'calories': round(breakfast_cals),
        'protein': round(macro_targets['protein'] * 0.25),
        'carbs': round(macro_targets['carbs'] * 0.25),
        'fat': round(macro_targets['fat'] * 0.25)
    })
    
    # Lunch (35% of calories)
    lunch_cals = calorie_target * 0.35
    meals.append({
        'meal': 'Lunch',
        'name': 'Grilled Chicken Salad with Quinoa',
        'calories': round(lunch_cals),
        'protein': round(macro_targets['protein'] * 0.35),
        'carbs': round(macro_targets['carbs'] * 0.35),
        'fat': round(macro_targets['fat'] * 0.35)
    })
    
    # Dinner (30% of calories)
    dinner_cals = calorie_target * 0.30
    meals.append({
        'meal': 'Dinner',
        'name': 'Salmon with Sweet Potato and Vegetables',
        'calories': round(dinner_cals),
        'protein': round(macro_targets['protein'] * 0.30),
        'carbs': round(macro_targets['carbs'] * 0.30),
        'fat': round(macro_targets['fat'] * 0.30)
    })
    
    # Snack (10% of calories)
    snack_cals = calorie_target * 0.10
    meals.append({
        'meal': 'Snack',
        'name': 'Protein Shake with Almonds',
        'calories': round(snack_cals),
        'protein': round(macro_targets['protein'] * 0.10),
        'carbs': round(macro_targets['carbs'] * 0.10),
        'fat': round(macro_targets['fat'] * 0.10)
    })
    
    return meals

def generate_workout_plan(goal_type):
    """Generate sample workout plan"""
    workouts = []
    
    if goal_type == 'Weight Loss':
        workouts = [
            {'day': 'Monday', 'type': 'Cardio', 'duration': 45, 'description': 'Running or Cycling', 'intensity': 'High'},
            {'day': 'Tuesday', 'type': 'Strength', 'duration': 30, 'description': 'Full Body Circuit', 'intensity': 'Medium'},
            {'day': 'Wednesday', 'type': 'Cardio', 'duration': 45, 'description': 'HIIT Training', 'intensity': 'High'},
            {'day': 'Thursday', 'type': 'Active Recovery', 'duration': 30, 'description': 'Yoga or Stretching', 'intensity': 'Low'},
            {'day': 'Friday', 'type': 'Strength', 'duration': 40, 'description': 'Upper Body Focus', 'intensity': 'Medium'},
            {'day': 'Saturday', 'type': 'Cardio', 'duration': 60, 'description': 'Swimming or Hiking', 'intensity': 'Medium'},
            {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
        ]
    elif goal_type == 'Weight Gain':
        workouts = [
            {'day': 'Monday', 'type': 'Strength', 'duration': 60, 'description': 'Chest & Triceps', 'intensity': 'High'},
            {'day': 'Tuesday', 'type': 'Strength', 'duration': 60, 'description': 'Back & Biceps', 'intensity': 'High'},
            {'day': 'Wednesday', 'type': 'Cardio', 'duration': 30, 'description': 'Light Cardio', 'intensity': 'Low'},
            {'day': 'Thursday', 'type': 'Strength', 'duration': 60, 'description': 'Legs & Shoulders', 'intensity': 'High'},
            {'day': 'Friday', 'type': 'Strength', 'duration': 45, 'description': 'Full Body', 'intensity': 'Medium'},
            {'day': 'Saturday', 'type': 'Active Recovery', 'duration': 30, 'description': 'Walking or Yoga', 'intensity': 'Low'},
            {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
        ]
    else:  # Maintenance
        workouts = [
            {'day': 'Monday', 'type': 'Strength', 'duration': 45, 'description': 'Upper Body', 'intensity': 'Medium'},
            {'day': 'Tuesday', 'type': 'Cardio', 'duration': 40, 'description': 'Running', 'intensity': 'Medium'},
            {'day': 'Wednesday', 'type': 'Strength', 'duration': 45, 'description': 'Lower Body', 'intensity': 'Medium'},
            {'day': 'Thursday', 'type': 'Yoga', 'duration': 60, 'description': 'Flexibility', 'intensity': 'Low'},
            {'day': 'Friday', 'type': 'Full Body', 'duration': 50, 'description': 'Circuit Training', 'intensity': 'Medium'},
            {'day': 'Saturday', 'type': 'Outdoor', 'duration': 90, 'description': 'Hiking/Sports', 'intensity': 'High'},
            {'day': 'Sunday', 'type': 'Rest', 'duration': 0, 'description': 'Complete Rest', 'intensity': 'None'}
        ]
    
    return workouts

def generate_exercises(workout_type):
    """Generate specific exercises for each workout type"""
    exercises_db = {
        'Strength': [
            'Bench Press: 3 sets x 8-12 reps',
            'Squats: 4 sets x 8-10 reps',
            'Deadlifts: 3 sets x 6-8 reps',
            'Shoulder Press: 3 sets x 10-12 reps',
            'Pull-ups: 3 sets to failure',
            'Dumbbell Rows: 3 sets x 10-12 reps'
        ],
        'Cardio': [
            'Treadmill Running: 20-30 minutes',
            'Stationary Bike: 25-35 minutes',
            'Elliptical Trainer: 30 minutes',
            'Jump Rope: 15-20 minutes',
            'Stair Climber: 20 minutes',
            'Rowing Machine: 25 minutes'
        ],
        'HIIT': [
            'Burpees: 45 seconds on, 15 seconds off x 5 rounds',
            'Mountain Climbers: 40 seconds on, 20 seconds off x 4 rounds',
            'Jump Squats: 30 seconds on, 30 seconds off x 6 rounds',
            'High Knees: 45 seconds on, 15 seconds off x 5 rounds',
            'Box Jumps: 40 seconds on, 20 seconds off x 4 rounds'
        ],
        'Yoga': [
            'Sun Salutations: 5 rounds',
            'Warrior Poses Series',
            'Downward Dog to Plank Flow',
            'Tree Pose and Balancing Series',
            'Childs Pose and Cobra Stretch'
        ]
    }
    
    if workout_type in exercises_db:
        return random.sample(exercises_db[workout_type], 3)
    return ["Custom exercises based on your fitness level"]

# Main app
st.markdown('<h1 class="main-header">🏋️‍♂️ AI Meal & Workout Planner</h1>', unsafe_allow_html=True)

# Sidebar for user input
with st.sidebar:
    st.header("User Profile")
    
    with st.form("user_profile"):
        st.session_state.user_data['age'] = st.slider("Age", 18, 80, st.session_state.user_data['age'])
        st.session_state.user_data['gender'] = st.selectbox("Gender", ["Male", "Female"], 
                                                          index=0 if st.session_state.user_data['gender'] == 'Male' else 1)
        st.session_state.user_data['height'] = st.slider("Height (cm)", 140, 220, st.session_state.user_data['height'])
        st.session_state.user_data['current_weight'] = st.slider("Current Weight (kg)", 40, 150, st.session_state.user_data['current_weight'])
        st.session_state.user_data['goal_weight'] = st.slider("Goal Weight (kg)", 40, 150, st.session_state.user_data['goal_weight'])
        st.session_state.user_data['activity_level'] = st.selectbox(
            "Activity Level",
            ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
            index=["Sedentary", "Light", "Moderate", "Active", "Very Active"].index(st.session_state.user_data['activity_level'])
        )
        st.session_state.user_data['goal_type'] = st.selectbox(
            "Goal Type",
            ["Weight Loss", "Weight Maintenance", "Weight Gain"],
            index=["Weight Loss", "Weight Maintenance", "Weight Gain"].index(st.session_state.user_data['goal_type'])
        )
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            # Recalculate everything
            bmr = calculate_bmr(
                st.session_state.user_data['current_weight'],
                st.session_state.user_data['height'],
                st.session_state.user_data['age'],
                st.session_state.user_data['gender']
            )
            
            tdee = calculate_tdee(bmr, st.session_state.user_data['activity_level'])
            
            st.session_state.user_data['calorie_target'] = calculate_calorie_target(
                st.session_state.user_data['current_weight'],
                st.session_state.user_data['goal_weight'],
                tdee,
                st.session_state.user_data['goal_type']
            )
            
            # Calculate macro targets
            macro_targets = calculate_macro_targets(st.session_state.user_data['calorie_target'], st.session_state.user_data['goal_type'])
            st.session_state.user_data.update(macro_targets)
            
            st.session_state.meals = generate_meal_plan(st.session_state.user_data['calorie_target'], macro_targets)
            st.session_state.workouts = generate_workout_plan(st.session_state.user_data['goal_type'])
            
            # Generate exercises for today's workout
            today_workout = next((w for w in st.session_state.workouts if w['day'] == datetime.now().strftime('%A')), None)
            if today_workout:
                st.session_state.exercises = generate_exercises(today_workout['type'])
            
            st.success("Profile updated successfully!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="section-header">📊 Your Fitness Overview</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    bmr = calculate_bmr(
        st.session_state.user_data['current_weight'],
        st.session_state.user_data['height'],
        st.session_state.user_data['age'],
        st.session_state.user_data['gender']
    )
    
    tdee = calculate_tdee(bmr, st.session_state.user_data['activity_level'])
    
    # Display metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("BMR", f"{bmr:.0f} kcal")
        st.metric("Current Weight", f"{st.session_state.user_data['current_weight']} kg")
    
    with metric_col2:
        st.metric("TDEE", f"{tdee:.0f} kcal")
        st.metric("Goal Weight", f"{st.session_state.user_data['goal_weight']} kg")
    
    with metric_col3:
        st.metric("Calorie Target", f"{st.session_state.user_data['calorie_target']:.0f} kcal")
        weight_to_go = st.session_state.user_data['current_weight'] - st.session_state.user_data['goal_weight']
        st.metric("Weight to Go", f"{abs(weight_to_go):.1f} kg")
    
    # Progress tracking
    st.markdown('<h3 class="section-header">🎯 Progress Tracking</h3>', unsafe_allow_html=True)
    
    # Weight progress (safe calculation)
    max_weight = max(st.session_state.user_data['current_weight'], st.session_state.user_data['goal_weight'])
    min_weight = min(st.session_state.user_data['current_weight'], st.session_state.user_data['goal_weight'])
    
    if max_weight > min_weight:  # Avoid division by zero
        if st.session_state.user_data['goal_type'] == 'Weight Loss':
            weight_progress = (max_weight - st.session_state.user_data['current_weight']) / (max_weight - min_weight)
        elif st.session_state.user_data['goal_type'] == 'Weight Gain':
            weight_progress = (st.session_state.user_data['current_weight'] - min_weight) / (max_weight - min_weight)
        else:
            weight_progress = 0.5
    else:
        weight_progress = 1.0
    
    # Safe progress value (clamped between 0.0 and 1.0)
    safe_weight_progress = max(0.0, min(1.0, weight_progress))
    st.progress(safe_weight_progress)
    st.caption(f"Weight Goal Progress: {safe_weight_progress * 100:.1f}%")
    
    # Water intake tracking
    st.markdown('<h3 class="section-header">💧 Water Intake</h3>', unsafe_allow_html=True)
    
    water_col1, water_col2 = st.columns([2, 1])
    with water_col1:
        water_intake = st.slider("Water intake (cups today)", 0, 12, st.session_state.user_data['water_intake'])
        st.session_state.user_data['water_intake'] = water_intake
    
    with water_col2:
        water_goal = 8  # cups per day
        water_progress = water_intake / water_goal
        safe_water_progress = max(0.0, min(1.0, water_progress))
        st.progress(safe_water_progress)
        st.caption(f"{water_intake}/8 cups ({safe_water_progress * 100:.0f}%)")

with col2:
    st.markdown('<h2 class="section-header">🍽️ Today\'s Meal Plan</h2>', unsafe_allow_html=True)
    
    for meal in st.session_state.meals:
        with st.expander(f"🍽️ {meal['meal']}: {meal['name']}"):
            st.write(f"**Calories:** {meal['calories']} kcal")
            st.write(f"**Protein:** {meal['protein']}g")
            st.write(f"**Carbs:** {meal['carbs']}g")
            st.write(f"**Fat:** {meal['fat']}g")
    
    st.markdown('<h2 class="section-header">💪 Today\'s Workout</h2>', unsafe_allow_html=True)
    
    today_workout = next((w for w in st.session_state.workouts if w['day'] == datetime.now().strftime('%A')), None)
    
    if today_workout:
        emoji = "🔥" if today_workout['type'] != 'Rest' else "😴"
        st.markdown(f'<div class="workout-card">', unsafe_allow_html=True)
        st.write(f"{emoji} **{today_workout['day']}: {today_workout['type']}**")
        st.write(f"⏰ **Duration:** {today_workout['duration']} minutes")
        st.write(f"📝 **Description:** {today_workout['description']}")
        st.write(f"⚡ **Intensity:** {today_workout['intensity']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show exercises
        if today_workout['type'] != 'Rest':
            st.write("**Recommended Exercises:**")
            for exercise in st.session_state.exercises:
                st.write(f"• {exercise}")
    else:
        st.write("No workout scheduled for today.")

# Nutrition summary
st.markdown('<h2 class="section-header">📈 Nutrition Summary</h2>', unsafe_allow_html=True)

if st.session_state.meals:
    total_calories = sum(meal['calories'] for meal in st.session_state.meals)
    total_protein = sum(meal['protein'] for meal in st.session_state.meals)
    total_carbs = sum(meal['carbs'] for meal in st.session_state.meals)
    total_fat = sum(meal['fat'] for meal in st.session_state.meals)
    
    # Macro targets
    protein_target = st.session_state.user_data['protein']
    carbs_target = st.session_state.user_data['carbs']
    fat_target = st.session_state.user_data['fat']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calories", f"{total_calories}", f"{total_calories - st.session_state.user_data['calorie_target']}")
    
    with col2:
        protein_diff = total_protein - protein_target
        st.metric("Protein", f"{total_protein}g / {protein_target}g", f"{protein_diff:+}g")
        st.progress(max(0.0, min(1.0, total_protein / protein_target)))
    
    with col3:
        carbs_diff = total_carbs - carbs_target
        st.metric("Carbs", f"{total_carbs}g / {carbs_target}g", f"{carbs_diff:+}g")
        st.progress(max(0.0, min(1.0, total_carbs / carbs_target)))
    
    with col4:
        fat_diff = total_fat - fat_target
        st.metric("Fat", f"{total_fat}g / {fat_target}g", f"{fat_diff:+}g")
        st.progress(max(0.0, min(1.0, total_fat / fat_target)))

# Weekly workout schedule
st.markdown('<h2 class="section-header">📅 Weekly Workout Schedule</h2>', unsafe_allow_html=True)

workout_df = pd.DataFrame(st.session_state.workouts)
st.dataframe(workout_df, hide_index=True, use_container_width=True)

# Tips based on goals
st.markdown('<h2 class="section-header">💡 Personalized Tips</h2>', unsafe_allow_html=True)

if st.session_state.user_data['goal_type'] == 'Weight Loss':
    st.info("""
    **Weight Loss Tips:**
    - Focus on protein-rich foods to stay full longer
    - Incorporate both cardio and strength training
    - Stay consistent with your calorie deficit
    - Drink plenty of water before meals
    - Get 7-9 hours of sleep nightly
    """)
elif st.session_state.user_data['goal_type'] == 'Weight Gain':
    st.info("""
    **Weight Gain Tips:**
    - Eat calorie-dense foods like nuts and avocados
    - Focus on progressive overload in your workouts
    - Consider protein supplements if needed
    - Eat every 3-4 hours
    - Track your progress weekly
    """)
else:
    st.info("""
    **Maintenance Tips:**
    - Focus on balanced nutrition
    - Maintain consistent exercise routine
    - Listen to your body's hunger cues
    - Regular health check-ups
    - Enjoy variety in your diet
    """)
