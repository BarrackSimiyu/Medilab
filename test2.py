# Function to find the greatest of three numbers
def find_greatest(num1, num2, num3):
    if num1 >= num2 and num1 >= num3:
        greatest = num1
    elif num2 >= num1 and num2 >= num3:
        greatest = num2
    else:
        greatest = num3
    return greatest

# Input three numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
num3 = float(input("Enter the third number: "))

# Find and print the greatest number
greatest_number = find_greatest(num1, num2, num3)
print(f"The greatest number is: {greatest_number}")
