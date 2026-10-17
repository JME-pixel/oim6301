def compute_bmi(weight,height):
    bmi = weight/(height**2)
    return bmi

def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    #print(category)
    return category


def main():
    weight = float(input("enter your weight in kilogram:"))
    height = float(input("enter your height in meters:"))
    bmi_value= compute_bmi(weight,height)   
    result =classify_bmi(bmi_value)
    print(f"Your category is {result}")

main()