# ...existing code...

people = [
    {"name": "Avery Chen", "height": 168, "weight": 62},
    {"name": "Jordan Patel", "height": 175, "weight": 78},
    {"name": "Morgan Reed", "height": 160, "weight": 55},
    {"name": "Riley Brooks", "height": 182, "weight": 84},
    {"name": "Casey Nguyen", "height": 171, "weight": 69},
    {"name": "Taylor Kim", "height": 165, "weight": 58},
    {"name": "Drew Foster", "height": 188, "weight": 91},
    {"name": "Quinn Rivera", "height": 177, "weight": 73},
]

for person in people:
    weight =person["weight"]
    height =person['height']
    bmi_value =bmi.compute_bmi(weight,height)
    category =bmi.classify_bmi(bmi_value)
    print(f"{person['name']},")