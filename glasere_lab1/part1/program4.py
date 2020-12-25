print("Welcome to the birthday dictionary. We know the birthdays of:")
birthdays = {"Ethan Glaser": "11/13/1998", "Anirudh Panuganty": "06/04/1999", "Noah Rodriguez": "02/12/1999", "Justin MacNeill": "01/02/1999", "Charlie Kerby": "05/04/1999", "Benjamin Franklin": "01/17/1706"}
for key in birthdays.keys():
    print(key)
print("Who's birthday do you want to look up?")
name = input()
print(name + "'s birthday is " + birthdays[name])
