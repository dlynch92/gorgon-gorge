import sys
import textwrap
import random
import math
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
        """
        Displays the player's name, hp, attack, defense, gold and equipment whenever the status command is picked.
        """
        print(f"The Adventurer {player.name}:")
        print(f"HP: {player.current_hp}/{player.max_hp} | Attack: {player.attack} | Defense: {player.defense} | Gold: {player.gold}")
        print(f"Sword: {player.sword} | Shield: {player.shield} | Potions: {player.potions}\n")

    def flee(self, monster):
        """
        When flee is picked in battle the player has a 50% chance of escaping back to the field screen. If the player
        fails in fleeing the monster will have a free turn - if they succeed the player is taken back to the field screen
        and flee is set to True so that the narrative text will not display again.
        """
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
        """
        When a player chooses to attack in battle a random number between 1 and 20 is generated - on a 1 the player will miss the 
        attack, and any value higher than the player's critical threshold will cause a strike with extra damage. Anything else the 
        attack will hit normally. Damage is calculated in the calculate_damage_to_monster function.
        """
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

    def potion(self):
        """
        Uses a potion to restore 50% of a players max HP to their current HP, ensure player current HP is no higher than their max hp,
        and reduce the player's potion count by 1
        """
        print("You reach into your bag and pick out a potion.")
        print(f"You drink it - feeling refreshed and restoring {math.ceil(self.max_hp / 2)} HP.")
        self.current_hp = self.current_hp + (math.ceil(self.max_hp / 2))
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        self.potions -= 1
        print(f"Current HP: {self.current_hp}/{self.max_hp}")
        print(f"Potions remaining: {self.potions}")

    def defend(self, monster):
        """
        Increases the player's defense rating for the remainder of the turn. The defense value of the player is multiplied by 1.5 and 
        rounded up but the original value is stored in the original_defense variable within the battle scene, and player defense is set back 
        to that after the monster takes a turn.
        """
        print(f"You raise your shield, prepared for the {monster.name}'s next strike.")
        self.defense = math.ceil(self.defense * 1.5)
        print("Defense increased.")

class Monster:
    def __init__ (self, name, gold, max_hp, current_hp, attack, defense, nature, storing_attack):
        self.name = name
        self.gold = gold
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack = attack
        self.defense = defense
        self.nature = nature
        self.storing_attack = storing_attack

    def death(self, player):
        """
        When monster current_hp is reduced to 0 then the monster dies. Add the monster's gold value to the player's gold
        total and increase players battles won counter by 1.
        """
        player.gold = player.gold + self.gold
        print(f"The {self.name} slumps over - defeated.")
        print("You win!")
        print(f"On the body of the {self.name} you find {self.gold} gold, bringing your total to {player.gold}.\n")
        player.battles_won += 1

    def attack_command(self, player):
        """
        A basic monster attack - has custom description based off type of monster, and then calculates the damage dealt
        to a player. Will display a player's remaining HP (raised to 0 if it is below 0), and if 0 then will call the
        game_over function as the player has lost.
        """
        self.attack_description()
        calculate_damage_to_player()
        if player.current_hp <= 0:
            player.current_hp = 0
        print(f"Current HP: {player.current_hp}/{player.max_hp}\n")
        if player.current_hp == 0:
            game_over()

class Goblin(Monster):
    def __init__(self, turn_count):
        self.turn_count = turn_count
        random_number = random.randrange(1,5)
        match random_number:
            case 1:
                Monster.__init__(self,"Goblin", 5, 9, 10, 4, 3, "malnurished", False)
            case 2:
                Monster.__init__(self,"Goblin", 5, 11, 16, 6, 3, "powerful", False)
            case 3:
                Monster.__init__(self,"Goblin", 5, 11, 13, 7, 3, "ferocious", False)
            case 4:
                Monster.__init__(self,"Goblin", 5, 9, 13, 5, 3, "timid", False)  
    
    def action_determiner(self):
        """
        Determines what the monster's action will be this turn, based off their nature, either attacking, skipping a turn or storing a
        powerful strike.
        """
        match self.turn_count:
            case 1:
                self.attack_command()
            case 2: 
                if self.nature == "malnurished" or self.nature == "timid":
                    print(f"The Goblin looks too {self.nature} to do anything.")
                else: 
                    print(f"The {self.nature} Goblin bangs its mace against its shield and lets out a bloodthirsty bellow.")
                    print("It's readying itself for a powerful blow.")
                    self.storing_attack = True 
            case 3:                
                self.storing_attack = False
                self.attack_command()
                self.turn_count = 1

    def attack_description(self):
        """
        Description when the Goblin uses an attack.
        """
        print("The Goblin raises its mace and swipes at you.")


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
        start_or_quit = input("Commands: \nstart | quit \n\n")

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
            #todo
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
        if monster.current_hp > 0 and player.current_hp > 0:
            battle_input = input("Commands: \nattack | defend | potion | status | flee\n\n")
            if battle_input.lower() == "attack":
                player.attack_command(monster)
                monster.action(player)
            elif battle_input.lower() == "defend":
                original_defense = player.defense
                player.defend(monster)
                monster.action(player)
                player.defense = original_defense
            elif battle_input.lower() == "potion":
                if player.potions > 0:
                    player.potion()
                    monster.action(player)
                else:
                    print("You reach for a potion, but have none.")
                    print(f"The {monster.name} awaits your input.")
                #todo
            elif battle_input.lower() == "status":
                player.status()
                print(f"The {monster.name} awaits your input.")
            elif battle_input.lower() == "flee":
                player.flee(monster)
            else:
                print("Input not recognised.\n")
        elif monster.current_hp <= 0:
            monster.death(player)
            flee = False
            field_screen(flee)
        elif player.current_hp <= 0:
            print("Game over.")
            #todo

def initialise_battle():
    """
    Generates an enemy for the player to fight with difficulty based off the number of previous fights won
    """
    match player.battles_won:
        case 0:
            monster = Goblin(1)
            return monster  

def calculate_damage_to_monster(player, monster, critical):
    """
    Calculates the damage a player deals to a monster when the attack command is taken. Random number is generated to
    determine variance so that they are not always dealing the exact same number. On a critical there is no variance but
    player attack is doubled in the calculation.
    """
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
        damage = (player.attack - monster.defense) + damage_variance
    if damage < 0:
        damage = 0
    monster.current_hp = monster.current_hp - damage
    print(f"You deal {damage} points of damage to the {monster.name}.\n")    

def calculate_damage_to_player(player, monster):
    """
    Calculates the damage a monster deals to the player when the attack command is taken. Random number is generated to
    determine variance so that they are not always dealing the exact same number. If a monster has stored an attack they will
    deal critical damage.
    """
    damage = 0
    if monster.storing_attack == True:
        damage = monster.attack * 2 - player.defense
    else:
        damage_variance_determiner = random.randrange(1,21)
        damage_variance = 0
        if damage_variance_determiner <= 4:
            damage_variance = 2
        elif damage_variance_determiner >= 16:
            damage_variance = 1                
        damage = (monster.attack - player.defense) + damage_variance
    if damage < 0:
        damage = 0
    player.current_hp = player.current_hp - damage
    print(f"The {monster.name} inflicts {damage} points of damage to you.")

def game_over():
    """
    Called when the player's HP reaches 0 - they have lost. Takes yes/no command to see if they want to play again from
    the start. Yes will restart game, no will quit game.
    """
    print("Your journey is over - Gorgon Gorge claims the life of another.")
    print("Perhaps the fates will be kinder to the next one.")
    print("Try again?")
    while True:
        yes_no = input("Commands: \yes | no \n\n")
        if yes_no.lower() == "yes":
            main()
        elif yes_no.lower() == "no":
            print("Quitting...\n")
            sys.exit()
        else:
            print("Input not recognised.\n")

def main():
    """
    Run all program functions   .
    """
    title_screen()
    player_name_input()
    flee = False
    field_screen(flee)

player = Player("", 5, 10, 10, 5, 3, "Short Sword", "Leather Shield", 19, 1, 0)
main()