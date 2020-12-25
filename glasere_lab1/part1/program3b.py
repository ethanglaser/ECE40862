import random
rando = random.randint(0,10)
guesses = 0
correct = 0
while guesses < 3 and correct == 0:
    guess = int(input("Enter your guess:"))
    if guess == rando:
        correct = 1
    guesses += 1
if correct:
    print("You win!")
else:
    print("You lose!")