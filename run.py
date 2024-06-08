import sys
import os

player_name = ""

def title_screen():
    """
    Displays title and basic instructions, enables the user to start the game
    or quit
    """

    print("GORGON GORGE\n")
    print("Welcome to Gorgon Gorge, a turn-based RPG where you step into the shoes of a daring adventurer on a quest to find and confront a mythical gorgon. Your journey begins at the mouth of an ancient gorge, shrouded in dark legends and whispered tales of a creature so terrifying that its very gaze can turn flesh to stone.\n")
    print("Driven by a desire for glory, treasure, or perhaps a deeply personal mission, you venture into the depths of Gorgon Gorge, fully aware of the dangers that lie ahead. The gorge is a place of untamed beauty and lurking peril, where every shadow hides a potential threat and every path could lead to your doom. Twisted rock formations and ancient ruins tell the story of a land steeped in magic and mystery.\n")

    while True:
        start_or_quit = input("Commands: \nstart - Start the game \nquit - Exit the game \n\n")

        if start_or_quit.lower() == "start":
            print("Starting game\n")
            break
        elif start_or_quit.lower() == "quit":
            print("Quitting game\n")
            sys.exit()
        else:
            print("Invalid input\n")

def player_name_input():
    """
    Takes the player's name and validates it ensuring it is between 3 and 15 characters long, contains no special characters,
    and does not consist entirely of spaces.
    """


def main():
    """
    Run all program functions   
    """
    title_screen()

main()