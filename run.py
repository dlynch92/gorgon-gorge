import sys
import textwrap
import random
from time import sleep

class Player:
    def __init__(self, name, gold, max_hp, current_hp, attack, defense, sword, shield, critical_threshold, potions, battles_won):
        self.name = name
        self.gold = gold
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack = attack
        self.defense = defense
        self.sword = sword
        self.shield = shield
        self.critical_threshold = critical_threshold
        self.potions = potions
        self.battles_won = battles_won
    
    def status(self):
        print(f"The Adventurer {player.name}:")
        print(f"HP: {player.current_hp}/{player.max_hp} | Attack: {player.attack} | Defense: {player.defense} | Gold: {player.gold}")
        print(f"Sword: {player.sword} | Shield: {player.shield} | Potions: {player.potions}\n")

    def flee(self, monster):
        print(f"You turn and attempt to flee from the {monster.nature} {monster.name}.")
        sleep(1)
        random_number = random.randrange(1,3)
        if random_number == 1:
            print("And succeed!\n")
            sleep(0.5)
            flee = True
            field_screen(flee)
        else:
            print("And fail!")
            sleep(0.5)
            #monster attacks

    def attack_command(self, monster):
        print(f"You swing your sword at the {monster.name}.")
        random_number = random.randrange(1,21)
        sleep(1)
        if random_number == 1:
            print(f"The {monster.name} dodges the attack.")
        elif random_number >= player.critical_threshold:
            print(f"You rend your sword through the {monster.name}'s flesh, dealing critical damage.")
            critical = True
            calculate_damage_to_monster(player, monster, critical)
        else:
            print(f"Your attack hits!")
            critical = False
            calculate_damage_to_monster(player, monster, critical)


class Monster:
    def __init__ (self, name, gold, max_hp, current_hp, attack, defense, nature):
        self.name = name
        self.gold = gold
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack = attack
        self.defense = defense
        self.nature = nature
    
    def attack_command(self, player):
        print(f"monster chomp {player.name}")
    
    def death(self, player):
        player.gold = player.gold + self.gold
        print(f"The {self.name} slumps over - defeated.")
        print("You win!")
        print(f"On the body of the {self.name} you find {self.gold} gold, bringing your total to {player.gold}.\n")
        player.battles_won += 1

player = Player("", 5, 10, 10, 5, 3, "Short Sword", "Leather Shield", 19, 1, 0)

def title_screen():
    """
    Displays title and basic instructions, enables the user to start the game
    or quit
    """
    print("GORGON GORGE\n")
    print(textwrap.fill("Welcome to Gorgon Gorge, a turn-based RPG where you step into the shoes of a daring adventurer on a quest to find and confront a mythical gorgon. Your journey begins at the mouth of an ancient gorge, shrouded in dark legends and whispered tales of a creature so terrifying that its very gaze can turn flesh to stone.", 80))
    print("")
    print(textwrap.fill("Driven by a desire for glory, treasure, or perhaps a deeply personal mission, you venture into the depths of Gorgon Gorge, fully aware of the dangers that lie ahead. The gorge is a place of untamed beauty and lurking peril, where every shadow hides a potential threat and every path could lead to your doom. Twisted rock formations and ancient ruins tell the story of a land steeped in magic and mystery.", 80))
    print("")

    while True:
        start_or_quit = input("Commands: \nstart - Start the game \nquit - Exit the game \n\n")

        if start_or_quit.lower() == "start":
            break
        elif start_or_quit.lower() == "quit":
            print("Quitting...\n")
            sys.exit()
        else:
            print("Input not recognised.\n")

def player_name_input():
    """
    Takes the player's name and runs validation function to ensure it can be accepted, then moves player on to game screen.
    """

    while True:
        print("What is your name, adventurer?")
        player_name = input("Please enter a name between 3 and 15 characters below: \n\n")
        if player_name_validation(player_name):
            print(f"Your name is {player_name}?\n")
            while True:
                yes_no = input("Commands: \nyes - Confirm name \nno - Choose another name \n\n")
                if yes_no.lower() == "yes":
                    player.name = player_name
                    print(f"The adventurer {player.name} steps forth...\n")
                    break
                elif yes_no.lower() == "no":
                    player_name_input()
                else:
                    print("Input not recognised.\n")
            break 

        
def player_name_validation(player_name):
    """
    Validates player name by ensuring it is between 3 and 15 characters long, contains no special characters,
    and does not consist entirely of spaces.
    """
    try: 
        if len(player_name) > 15 or len(player_name) < 3:
            raise ValueError(
                f"The name entered was {len(player_name)} characters long."
            )
        if not player_name.replace(" ", "").isalpha():
            raise ValueError(
                "Please use alphabetical characters only."
        )
        if player_name.isspace():
            raise ValueError(
                "Name cannot be blank."
            )
    except ValueError as e:
        print(f"Name invalid: {e}\n")
        return False
    else:
        return True

def field_screen(flee):
    """
    The field screen where players can advance to the next battle, go to the shop or check their status. Only calls narrative field
    description at start of game or after winning a battle - skips if they flee.   
    """
    if not flee:
       field_description()

    while True:
        field_input = input("Commands: \nbattle - Advance to next battle \nshop - Buy items and equipment \nstatus - Display player status\n\n")
        if field_input.lower() == "battle":
            print("You raise your sword.\n")
            battle_screen()
        elif field_input.lower() == "shop":
            print("Shop starts\n")
        elif field_input.lower() == "status":
            player.status()
        else:
            print("Input not recognised.\n")

def field_description():
    """
    Description of the field that changes depending on how many battles the user has won
    """
    match player.battles_won:
        case 0: 
            print(textwrap.fill("The air is thick with enchantment, carrying the scent of blooming nightshade and the distant hum of mystical energies. Towering walls of ancient stone, etched with glowing runes, rise on either side - their surfaces shimmering with hues that shift like the colors of an opal.", 80))
            print("")
            print(textwrap.fill("As you advance deeper into the gorge the peaceful ambience gives way to something more sinister. Growling. The gnashing of teeth. A sense of forboding. Around the next bend, you know, something waits — something unknown and undoubtedly dangerous.", 80))
            print("")
        case 1:
            print("You won a fight! Back to the field screen")

def battle_screen():
    """
    Takes players commands during a battle and executes the relevant player object function
    """

    monster = initialise_battle()
    print(f"A {monster.name} appears. It looks {monster.nature}.\n")
       
    while True:
        if monster.current_hp > 0:
            battle_input = input("Commands: \nattack | defend | potion | status | flee\n\n")
            if battle_input.lower() == "attack":
                player.attack_command(monster)
                monster.attack_command(player)
            elif battle_input.lower() == "defend":
                print("Shield")
            elif battle_input.lower() == "potion":
                print("Potion")
            elif battle_input.lower() == "status":
                player.status()
                print(f"The {monster.name} awaits your input.")
            elif battle_input.lower() == "flee":
                player.flee(monster)
            else:
                print("Input not recognised.\n")
        else:
            monster.death(player)
            flee = False
            field_screen(flee)

def initialise_battle():
    """
    Generates an enemy for the player to fight with difficulty based off the number of previous fights won
    """
    random_number = random.randrange(1,5)
    match player.battles_won:
        case 0:
            match random_number:
                case 1:
                    monster = Monster("Goblin", 5, 9, 10, 4, 3, "malnurished")
                    return monster  
                case 2:
                    monster = Monster("Goblin", 5, 11, 16, 6, 3, "powerful")
                    return monster  
                case 3:
                    monster = Monster("Goblin", 5, 11, 13, 7, 3, "ferocious")
                    return monster  
                case 4:
                    monster = Monster("Goblin", 5, 9, 13, 5, 3, "timid")
                    return monster   

def calculate_damage_to_monster(player, monster, critical):
    damage = 0
    if critical == True:
        damage = player.attack * 2 - monster.defense
    else:
        damage_variance_determiner = random.randrange(1,11)
        damage_variance = 0
        if damage_variance_determiner <= 3:
            damage_variance = 2
        elif damage_variance_determiner >= 7:
            damage_variance = 1                
        damage = player.attack - monster.defense + damage_variance
    monster.current_hp = monster.current_hp - damage
    print(f"You deal {damage} points of damage.")    

def main():
    """
    Run all program functions   
    """
    title_screen()
    player_name_input()
    flee = False
    field_screen(flee)

main()