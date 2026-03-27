print("Simple Calculator")

number1=int(input("Enter first number\n: "))
opparator=input("Enter operator\n:+, -, *, /\n: ")
number2=int(input("Enter second number\n: "))
try:
    
    if opparator=="+":
          print(number1+number2)      
    elif opparator=="-":
           print(number1-number2)
    elif  opparator=="*":
          print(number1*number2)
    elif opparator=="/":
           print(number1/number2)    
except ValueError:
      #check if the user input is not a number
      print("Enter only Numbers") 
except ZeroDivisionError:
      #checks if the user is attempting to divide by zero
      print("Cannot divide by zero")      

                      