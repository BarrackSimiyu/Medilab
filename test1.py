# function with parameters
# def sum(num1,num2):
   

#    sum=num1+num2
#    print("The sum is:",sum)

# sum(5,2)

# calculate BMI
def bmi(weight,height):
   
   bmi=weight/(height*height)
   print("The BMI is :",bmi)

bmi(100,2.0)

# area of a circle

def area(pie,r):
   area=pie*r*r
   print("The area of the circle is:",area)

# area(3.142,14)

# to check greater or lesss than
def check(a,b,c):
  
   if a>b and a>c:
      print("a is the largest ")
   elif b>a and b>c:
      print("b is the largest")
   
   else:
      print("c is the greatest")
      

# check(500,200,100)
      
    #   write a function to check odd numbers
def is_odd(number):

    
    if number % 2 != 0:
        print(number," is an odd number")
    else:
        print(number,"is an even number")

is_odd(10)


         
         
