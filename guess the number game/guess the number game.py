import random 


#this imports the random module, which allows us to generate random numbers
def option1():
    print("Welcome to the Guess the Number Game!")
    user_option=int(input("Please select an option: \n1. Start Game\n2. Exit\n"))
    if user_option==1:
        game()
    elif user_option==2:
        print("Thank you for playing! Goodbye!")    

def option2():
    nt=int(input("Do you want to replay the game? (1 for Yes, 2 for No): "))
    if nt==1:
        game()
    elif nt==2:
        print("Thank you for playing! Goodbye!")    

def game():
     secret_number=random.randint(1,20)
#this genarates a random number between 1 and 20 and stores it in the variable secret_number
     attempts=4
     print("I am thinking of a number between 1 and 20.")
     while attempts>0:
            user_guess=int(input("Take a guess: "))
            if user_guess==secret_number:
               print("Congratulations! You guessed the number correctly!") 
               option2()
            elif user_guess<secret_number:
               print("Too low! Try again.")
               attempts-=1
        #this decreases the number of attempts by 1 each time the user guesses incorrectly
            elif user_guess>secret_number:
                print("Too high! Try again.")
                attempts-=1
            
            else:
              print("Invalid input. Please enter a number between 1 and 20.")
        #this handles the case where the user enters an invalid input that is not a number between 1 and 20  
            if attempts==0:
               print("Sorry, you've used all your attempts. The number was", secret_number)
               option2()
         #this handles the case where the user has used all their attempts and reveals the secret number 
             
           
option1()
