# --- REPLACE the load_meals_from_github function with this ---

def load_meals_from_github():
    """Returns prebuilt meal templates instead of loading from CSV."""
    try:
        # Prebuilt meal templates (no CSV loading needed)
        meal_templates = {
            'Weight Loss': {
                'Breakfast': 'Greek Yogurt with Berries and Chia Seeds (300 cal, 25g protein)',
                'Lunch': 'Grilled Chicken Salad with Quinoa (400 cal, 35g protein)',
                'Dinner': 'Baked Salmon with Roasted Vegetables (450 cal, 40g protein)',
                'Snack': 'Apple with Almond Butter (200 cal, 8g protein)'
            },
            'Weight Gain': {
                'Breakfast': 'Oatmeal with Banana and Peanut Butter (550 cal, 20g protein)',
                'Lunch': 'Beef and Vegetable Stir-fry with Rice (600 cal, 35g protein)',
                'Dinner': 'Chicken with Sweet Potato and Avocado (650 cal, 45g protein)',
                'Snack': 'Protein Shake with Oats (350 cal, 30g protein)'
            },
            'Weight Maintenance': {
                'Breakfast': 'Whole Grain Toast with Eggs and Avocado (450 cal, 25g protein)',
                'Lunch': 'Turkey and Hummus Wrap with Side Salad (500 cal, 30g protein)',
                'Dinner': 'Fish with Quinoa and Steamed Vegetables (550 cal, 35g protein)',
                'Snack': 'Greek Yogurt with Nuts (300 cal, 20g protein)'
            },
            'Muscle Building': {
                'Breakfast': 'Protein Pancakes with Berries (500 cal, 35g protein)',
                'Lunch': 'Lean Beef with Brown Rice and Broccoli (650 cal, 45g protein)',
                'Dinner': 'Salmon with Sweet Potato and Asparagus (600 cal, 40g protein)',
                'Snack': 'Cottage Cheese with Almonds (350 cal, 30g protein)'
            }
        }
        
        return meal_templates
    except Exception as e:
        st.error(f"Error creating meal templates: {e}")
        # Fallback to default templates
        return {
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
