
import random as r

to_guess = r.randint(1, 100)
guesses = []
i = 1

while True:
    user = int(input(f"Enter your {i} guess:"))
    guesses.append(user)  # store all the guesses

    if user > to_guess:
        print(f"{user} is bigger than the number")

    elif user < to_guess:
        print(f"{user} is smaller than the number")

    else:
        print("CORRECT !!!")
        break  # stop the game

    i += 1  # count the number of complete guesses

print(f"It took you {i} guesses and they were {guesses}")
