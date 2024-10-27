PORTS = {
    "STEP_0": 5550,  # Food truck (order processing)
    "STEP_1": 5551,  # Getting ingredients
    "STEP_2": 5552,  # Cooking
    "STEP_3": 5553,  # Packing
    "COMPLETED": 5554,  # Final orders (to notify customers)
}

STEP_NAMES = {0: "food_truck", 1: "ingredient_getter", 2: "cook", 3: "packer"}
