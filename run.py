import sys
import textwrap
import random
import math
from time import sleep
import wordtodigits


class Player:
    def __init__(self, name, gold, max_hp, current_hp, attack, defense, critical_threshold, potions, battles_won):
        self.name = name
        self.gold = gold
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack = attack
        self.defense = defense
        self.critical_threshold = critical_threshold
        self.potions = potions
        self.battles_won = battles_won
        self.defending = False
    
    def status(self):
        """
        Displays the player's name, hp, attack, defense, gold and equipment whenever the status command is picked.
        """
        print(f"The Adventurer {player.name}:")
        print(f"HP: {player.current_hp}/{player.max_hp} | Attack: {player.attack} | Defense: {player.defense}")
        print(f"Gold: {player.gold} | Potions: {player.potions}\n")

    def flee(self, monster):
        """
        When flee is picked in battle the player has a 50% chance of escaping back to the field screen. If the player
        fails in fleeing the monster will have a free turn - if they succeed the player is taken back to the field screen
        and flee is set to True so that the narrative text will not display again.
        """
        self.defending = False
        print(f"You turn and attempt to flee from the {monster.nature} {monster.name}.")
        sleep(1)
        random_number = random.randrange(1,5)
        if random_number <= 3:
            print("And succeed!\n")
            sleep(0.5)
            flee = True
            print("You retreat to safety.\n")
            field_screen(flee, leave_shop)
        else:
            print("And fail!\n")
            sleep(0.5)
            monster.action_determiner()

    def attack_command(self, monster):
        """
        When a player chooses to attack in battle a random number between 1 and 20 is generated - on a 1 the player will miss the 
        attack, and any value higher than the player's critical threshold will cause a strike with extra damage. Anything else the 
        attack will hit normally. Damage is calculated in the calculate_damage_to_monster function.
        """
        self.defending = False
        print(f"You swing your sword at the {monster.name}.")
        random_number = random.randrange(1,21)
        sleep(1)
        if monster.evasive == True and random_number <= 13:
            print(f"And miss. The {monster.name} is moving too quickly to comprehend.\n")
        elif monster.evasive == True and random_number > 13 and random_number < player.critical_threshold:
            print(f"Despite the {monster.name}'s speed, your attack hits.")
            critical = False
            calculate_damage_to_monster(player, monster, critical)
        elif monster.evasive == True and random_number >= player.critical_threshold:
            print(textwrap.fill(f"Despite the {monster.name}'s speed, your attack hits and rends through the {monster.name}'s flesh, dealing critical damage.", 80))
            critical = True
            calculate_damage_to_monster(player, monster, critical)
        elif random_number == 1:
            print(f"The {monster.name} dodges the attack.\n")
        elif random_number >= player.critical_threshold:
            print(f"You rend your sword through the {monster.name}'s flesh, dealing critical damage.")
            critical = True
            calculate_damage_to_monster(player, monster, critical)
        else:
            print(f"Your attack hits!")
            critical = False
            calculate_damage_to_monster(player, monster, critical)
        #check if monster dies and win battle if so
        if monster.current_hp <= 0:
            monster.death(player)
            flee = False
            leave_shop = False
            if monster.name == Gorgon:
                game_win()
            else:
                field_screen(flee, leave_shop)

    def potion(self):
        """
        Uses a potion to restore 50% of a players max HP to their current HP, ensure player current HP is no higher than their max hp,
        and reduce the player's potion count by 1
        """
        self.defending = False
        if player.potions > 0:
            print("You reach into your bag and pick out a potion.")
            print(f"You drink it - feeling refreshed and restoring {math.ceil(self.max_hp / 2)} HP.")
            self.current_hp = self.current_hp + (math.ceil(self.max_hp / 2))
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.potions -= 1
            print(f"Potions remaining: {self.potions}\n")
        else: 
            print("You reach for a potion, but have none.")

    def defend(self, monster):
        """
        Increases the player's defense rating for the remainder of the turn. The defense value of the player is multiplied by 1.5 and 
        rounded up but the original value is stored in the original_defense variable within the battle scene, and player defense is set back 
        to that after the monster takes a turn.
        """
        self.defending = True
        if monster.name == Gorgon:
            print(f"You raise your shield and hide behind it, blocking the Gorgon from view.\n")
        else:
            print(f"You raise your shield, prepared for the {monster.name}'s next strike.\n")
        self.defense = math.ceil(self.defense * 2.5)

class Monster:
    def __init__ (self, name, gold, max_hp, current_hp, attack, defense, nature, storing_attack, recharging, turn_count, evasive):
        self.name = name
        self.gold = gold
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.attack = attack
        self.defense = defense
        self.nature = nature
        self.storing_attack = storing_attack
        self.recharging = recharging
        self.turn_count = turn_count
        self.evasive = evasive

    def death(self, player):
        """
        When monster current_hp is reduced to 0 then the monster dies. Ask if the player wants to loot the monster,
        Add the monster's gold value to the player's gold total if so and increase players battles won counter by 1.
        """
        player.gold = player.gold + self.gold
        player.battles_won += 1
        print(f"The {self.name} slumps over - defeated.\n")
        while True:
            loot_input = input("Commands: loot | leave\n\n")
            if loot_input.lower() == "loot":
                print(f"On the body of the {self.name} you find {self.gold} gold, bringing your total to {player.gold}.\n")
                sleep(3)
                break
            elif loot_input.lower() == "leave":
                print("You move on, swiftly.")
                sleep(3)
                break
            else: 
                print("Invalid input.")

    def attack_command(self, player):
        """
        A basic monster attack - has custom description based off type of monster, and then calculates the damage dealt
        to a player. Will display a player's remaining HP (raised to 0 if it is below 0), and if 0 then will call the
        game_over function as the player has lost.
        """
        self.attack_description()
        calculate_damage_to_player(player, self)
        if player.current_hp <= 0:
            player.current_hp = 0
            game_over()

class Goblin(Monster):
    def __init__(self):
        random_number = random.randrange(1,5)
        match random_number:
            case 1:
                Monster.__init__(self,"Goblin", 5, 10, 10, 4, 2, "malnurished", False, False, 1, False)
            case 2:
                Monster.__init__(self,"Goblin", 8, 15, 15, 5, 3, "large", False, False, 1, False)
            case 3:
                Monster.__init__(self,"Goblin", 8, 10, 10, 7, 2, "ferocious", False, False, 1, False)
            case 4:
                Monster.__init__(self,"Goblin", 5, 13, 13, 5, 3, "timid", False, False, 1, False)  
    
    def introduction(self, flee):
        """
        Description of the monster when it appears.
        """
        if not flee:
            print(textwrap.fill("You turn the corner - a wall of foul stench permeates the air. Standing there, poised for battle, is a raggedy humanoid creature. Its sharp teeth are bared and it carries a blunt mace in one hand and a small shield in the other. You know what this is, every adventurer in the world knows what this is - A goblin. A persistant blight in the world outside of the safety of the city walls.", 80))
            print("")
        else:
            print("You take a different route - Eventually, however, you encounter another Goblin.\n")
        print(f"It looks {self.nature}.\n")

    def action_determiner(self):
        """
        Determines what the monster's action will be this turn, based off their nature, either attacking, skipping a turn or storing a
        powerful strike.
        """
        match self.turn_count:
            case 1:
                if self.recharging == True:
                    print("The Goblin shuffles around trying to regain its footing after the last attack.\n")
                else:
                    self.attack_command(player)
                self.turn_count += 1    
            case 2: 
                if self.nature == "malnurished" or self.nature == "timid":
                    print(f"The Goblin looks too {self.nature} to do anything.\n")
                else: 
                    print(textwrap.fill(f"The {self.nature} Goblin bangs its mace against its shield and lets out a bloodthirsty bellow.", 80))
                    print("It's readying itself for a powerful blow.\n")
                    self.storing_attack = True 
                self.turn_count += 1
            case 3:                
                self.attack_command(player)
                if self.storing_attack == True:
                    self.recharging = True
                self.storing_attack = False
                self.turn_count = 1

    def attack_description(self):
        """
        Description when the Goblin uses an attack.
        """
        if self.storing_attack == True:
            print("The Goblin dashes forward and jumps, putting its entire weight behind a huge overhead swing.")
        else:
            print("The Goblin raises its mace and swipes at you.")

class Siren(Monster):
    def __init__(self):
        random_number = random.randrange(1,3)
        match random_number:
            case 1:
                Monster.__init__(self,"Siren", 14, 20, 20, 4, 4, "wistful", False, False, 1, False)
            case 2:
                Monster.__init__(self,"Siren", 14, 20, 20, 5, 3, "aloof", False, False, 1, False)

    def introduction(self, flee):
        """
        Description of the monster when it appears.
        """
        if not flee:
            print(textwrap.fill("Quiet at first, but getting louder by the second, you hear the humming of a melanchonic song. It comes into focus, quickly drowning out the ambience of the grove. It's beautiful and sad - and hideous. Evil, even.", 80))
            print("")
            print(textwrap.fill("You descend a steep rock and find the source of the noise hiding in a large alcove. A feminine humanoid form stands there humming her song, barely bothered by your presence. She would be beautiful, lest for the layer of corpses that adorn the floor of her abode.", 80))
            print("")
            print(textwrap.fill("These poor souls were adventurers too, you imagine. But they were not as prepared as you - you know what this monster is. A siren.", 80))
            print("")
            
        else: 
            print(textwrap.fill("You take a different route - eventually however, a Siren's song begins anew. You feel compelled to follow it to the source. Another alcove, another pile of corpses. Another Siren.", 80))
            print("")
        print(f"It looks {self.nature}.\n")

    def action_determiner(self):
        match self.turn_count:
            case 1:
                print("The siren does not react to your presence - she continues to hum.\n")
                self.turn_count += 1    
            case 2: 
                print("The siren does not react to your presence - her humming becomes more intense.\n")
                self.turn_count += 1
            case 3:                
                print("The siren does not react to your presence - her humming builds to a crescendo.\n")
                self.turn_count += 1
            case 4: 
                print("The siren's song takes over your body and drains your life. You feel weak.")
                print("Your HP is reduced to 1.")
                print("The siren reacts to your presence - the humming stops. She is poised to attack.\n")
                player.current_hp = 1
                self.turn_count += 1
            case 5:
                self.attack_command(player)

    def attack_description(self):
        """
        Description when the Siren uses an attack.
        """
        print("The Siren erratically flails at you with her claws.")

class Sprite(Monster):
    def __init__(self):
        random_number = random.randrange(1,3)
        match random_number:
            case 1:
                Monster.__init__(self,"Sprite", 19, 24, 24, 6, 4, "clumsy", False, False, 1, False)
            case 2:
                Monster.__init__(self,"Sprite", 19, 24, 24, 6, 4, "hyperactive", False, False, 1, False)

    def introduction(self, flee):
        """
        Description of the monster when it appears.
        """
        if not flee:
            print(textwrap.fill("A shimmer catches your eye - something flutters gracefully through the air. A tiny creature with translucent wings. Its eyes are large and sparkling initially with curiosity, then quickly with mischief.", 80))
            print("")
            print(textwrap.fill("This is a Sprite. It begins to encircle you and lets out a soft, menacing giggle that resonates through the glade. Then you spot it - a bow. Tiny, but for the size of the sprite, quite large. It is poised at you.", 80))
            print("")
        else:
            print(textwrap.fill("You take a different route - soon enough, though, the familiar hum of wings fill the air. Then the laughter. Another Sprite is here.", 80))
            print("")
        print(f"It looks {self.nature}.\n")

    def action_determiner(self):
        match self.turn_count:
            case 1:
                self.attack_command(player)
                self.turn_count += 1    
            case 2:
                if self.nature == "clumsy":
                    print("The Sprite draws some dust from its pocket and sprinkles it on an arrow.")
                    print("An intense magical aura emanates from the arrow tip.\n")
                    self.storing_attack = True
                elif self.nature == "hyperactive":
                    print("The Sprite begins to zip around the air at supersonic speeds.")
                    print("You can't tell where it is.\n")
                    self.evasive = True
                self.turn_count += 1
            case 3:
                self.attack_command(player)
                if self.storing_attack == True:
                    self.recharging = True
                self.storing_attack = False
                self.turn_count += 1
            case 4:
                if self.recharging == True:
                    print("The Sprite fumbles around with its quill, hastily reaching for more arrows.\n")
                    self.recharging = False
                else:
                    self.attack_command(player)
                self.turn_count += 1
            case 5:
                if self.evasive == True:
                    print("The Sprite's intense movements grind to a halt. It looks exhausted.\n")   
                    self.recharging = True
                    self.evasive = False
                else:
                    self.attack_command(player)
                self.turn_count += 1
            case 6:
                if self.recharging == True:
                    print("The Sprite still looks tired. It levitates in place.\n")
                    self.recharging = False
                else:
                    print("The Sprite fumbles around with it's quill, reaching for more arrows.\n")
                self.turn_count = 1


    def attack_description(self):
        """
        Description when the Sprite uses an attack.
        """
        if self.storing_attack == True:
            print(textwrap.fill("In the blink of an eye the Sprite's longbow is drawn and fired - the arrow rips through the air faster than you can comprehend.", 80))
        elif self.evasive == True:
            print(textwrap.fill("Out of nowhere an arrow pierces your flesh.", 80))
        else:
            print("The Sprite draws its longbow and fires.")

class Troll(Monster):
    def __init__(self):
        random_number = random.randrange(1,3)
        match random_number:
            case 1:
                Monster.__init__(self,"Troll", 25, 55, 55, 7, 3, "gangly", False, False, 1, False)
            case 2:
                Monster.__init__(self,"Troll", 25, 55, 55, 5, 5, "angry", False, False, 1, False)

    def introduction(self, flee):
        """
        Description of the monster when it appears.
        """
        if not flee:
            print(textwrap.fill("The silence is pierced by the sound of a lumbering creature standing up. You can't see it through the thick foliage, but it is nearby.", 80))
            print("")
            print(textwrap.fill("But then you do - it's hard not to. A towering mass of muscle and flesh holding a club larger in size than you. It turns and meets your eye. Its a Troll, and its coming for you.", 80))
            print("")
        else:
            print(textwrap.fill("You take a different route - but there is no route here that will lead you safely through. This is the Troll's home, and they smell you. Fresh meat. Another Troll stands before you.", 80))
            print("")
        print(f"It looks {self.nature}.\n")

    def action_determiner(self):
        match self.turn_count:
            case 1:
                self.attack_command(player)
                self.turn_count += 1    
            case 2:
                if self.nature == "angry":
                    print("The Troll beats its chest wildly with its club, enraging it further.")
                    print("The Troll's attack increases at the expense of its health.\n")
                    self.attack += 1
                    self.current_hp -= 3
                    if self.current_hp < 1:
                        self.current_hp = 1
                    self.turn_count = 1
                    
                elif self.nature == "gangly":
                    if self.storing_attack == False and self.recharging == False:
                        random_number = random.randrange(1,5)
                        if random_number == 1:
                            self.storing_attack = True
                            print("The Troll winds up for a huge swing.\n")
                        else:
                            self.attack_command(player)
                    elif self.storing_attack == True:
                         self.attack_command(player)
                         self.storing_attack = False
                         self.recharging = True
                    else:
                        print("The Troll takes a moment to regain his footing after the swing.\n")
                        self.recharging = False

    def attack_description(self):
        """
        Description when the Troll uses an attack.
        """
        if self.storing_attack == True:
            print("The Troll lets out a blood-curdling roar and swipes fiercly with its club.")
        else:
            print("The Troll swings its club.")

class Gorgon(Monster):
    def __init__(self):
        Monster.__init__(self,"Gorgon", 100000, 70, 70, 9, 6, "legendary", False, False, 1, False)
        self.gaze_countdown = 6

    def introduction(self, flee):
        """
        Description of the monster when it appears.
        """
        if not flee:
            print(textwrap.fill("You approach the altar in the middle of the room - the light that envelops it is warm, comforting, moreso than anything else you have encountered in this place.", 80))
            print("")
            print(textwrap.fill("The ritual to summon the Gorgon is etched in your brain - this is what its all been for. The blood, sweat and tears that have lead you to this place are all for this. You take a deep breath and begin the incantation.", 80))
            print("")
            print(textwrap.fill("The single column of light expands outwards, illuminating the entire room. The scope of it is terrifying - before you could see a handful of frozen adventurers, but now you can see hundreds. Thousands maybe. Scores upon scores of them in every direction as far as the eye can see.", 80))
            print("")
            print(textwrap.fill("And then a roar from behind you.", 80))
            print("")
            print(textwrap.fill("The Gorgon. Huge. Her lower body is serpentine and coils gracefully on the cold, stone floor. Her upper body, though bearing the semblence of a woman, is clearly not human. Her skin is a sickly green. Crowning her head is a writhing mass of green venomous snakes, each one hissing and flicking its forked tongue as they weave through the air. Five snakes, more grey than green, sit motionless covering her eyes. The serpents' scales catch the light and create an eerie, shimmering halo that encompasses the Gorgon.", 80))
            print("")
            print("This is it. \n")
        else:
            print(textwrap.fill("The Gorgon remains where you left her - any signs of damage have vanished from her complexion. She stands tall, waiting for your approach.", 80))
        print(f"It looks {self.nature}.\n")

    def action_determiner(self):
        if self.gaze_countdown == 0:
            self.stone_gaze()
        else:    
            match self.turn_count:
                case 1:
                    print("Six grey snakes of hair sit motionless covering the Gorgon's eyes.")
                    self.attack_command(player)
                    self.turn_count += 1
                case 2:
                    self.attack_command(player)
                    self.turn_count += 1
                case 3:
                    print(textwrap.fill("Globs of green, viscous liquid spit forth from a green snake's mouth onto the Gorgon's scimitar.", 80))
                    print("")
                    self.storing_attack = True
                    self.turn_count += 1
                case 4:
                    self.attack_command(player)
                    self.storing_attack = False
                    self.turn_count += 1
                case 5:
                    random_number = random.randrange(1,11)
                    if self.storing_attack == False and self.gaze_countdown >= 2 and random_number >= 7:
                        print(textwrap.fill("Globs of green, viscous liquid spit forth from a green snake's mouth onto the Gorgon's scimitar.", 80))
                        print("")
                        self.storing_attack = True
                    elif self.storing_attack == True:
                        self.attack_command(player)
                        self.storing_attack = False
                    else:
                        self.attack_command(player)

    def attack_description(self):
        """
        Description when the Gorgon uses an attack.
        """
        if self.storing_attack == True:
            print("Two grey snakes covering the Gorgon's eyes rise and dance with the rest.")
            print(textwrap.fill("The Gorgon's scimitar carves through your flesh, the poison stings fiercely.", 80))
            print("")

            self.gaze_countdown -= 2
        else:
            print("One grey snake covering the Gorgon's eyes rises and dances with the rest.")
            print("The Gorgon's scimitar carves through your flesh.\n")
            self.gaze_countdown -= 1
            
    
    def stone_gaze(self):
        """
        When Gorgon's gaze_countdown reaches 0 this will be the next action.
        """
        print("No grey snakes remain covering the Gorgon's eyes.\n")
        sleep(3)
        if player.defending == True:
            print("You remain behind your shield - the air around you grows heavy like stone.\n")
            sleep(3)
            print("The sensation passes.")
            print("You peer over your shield - Six grey snakes sit motionless covering her eyes.\n")
            self.gaze_countdown = 6
        if player.defending == False:
            print("The Gorgon's gaze entraps you.\n")
            sleep(3)
            print(textwrap.fill("Her eyes are large and beautiful and you can't look away. You don't want to look away. Her gaze is magnetic and piercing. You feel it from your head first but it spreads quickly to the rest of your body: a stiffness. And then...", 80))
            sleep(3)
            print("")
            print("Nothing.\n")
            sleep(3)
            print("For eternity.\n")
            sleep(3)
            print(textwrap.fill("You have fallen prey to the Gorgon's gaze. Perhaps your petrified body will serve as ample warning to the next.",80))
            player.current_hp = 0
            print("")
            game_over()
shop = {
    "Potion": 3,
    "HP": 2,
    "Attack": 5,
    "Defense": 5,
}

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
        start_or_quit = input("Commands: start | quit \n\n")

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
                yes_no = input("Commands: yes | no \n\n")
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

def field_screen(flee, leave_shop):
    """
    The field screen where players can advance to the next battle, go to the shop or check their status. Only calls narrative field
    description at start of game or after winning a battle - skips if they flee.   
    """
    if not flee and not leave_shop:
       field_description()

    while True:
        field_input = input("Commands: battle | shop | status | potion \n\n")
        if field_input.lower() == "battle":
            print("You raise your sword.\n")
            battle_screen(flee)
        elif field_input.lower() == "shop":
            shop_screen(flee)
        elif field_input.lower() == "status":
            player.status()
        elif field_input.lower() == "potion":
            player.potion()
        elif field_input.lower() == "dev":
            player.max_hp = 999
            player.current_hp = 999
            player.potions = 999
            player.attack = 10
            player.defense = 100
            print("Dev mode activated\n")
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
            print(textwrap.fill("The tension in the air is lifted now that the threat of the goblin has passed - but you've heard the stories. Stories of adventurers greater than you that have never made it back from this twisted place. Adventurers that would not fall victim to a measly goblin, or even ten.", 80))
            print("")
            print("There will be worse to come.\n")
            print(textwrap.fill("Deeper you venture - the path becoming less and less distinct and travelled as the minutes go by. The stench of goblin has long since passed, the air now thick with the scent of moss. A trail of bioluminescent fungi leads the way forward - down, and down, and down.",80))
            print("")
            print("Until it hits you again. That forboding. Worse than the last.\n")
        case 2: 
            print(textwrap.fill("You continue your descent and are lead to the edge of a vast, serene lake. The water is a mirror, reflecting the towering cliffs and twisted trees that encircle it - their images rippling with every gentle breeze.", 80))
            print("")
            print(textwrap.fill("Moored on the shore is a small wooden rowboat, it groans and creaks under your weight as you step onto it and begin to row.", 80))
            print("")
            print(textwrap.fill("You cross the lake with no resistance and dismount your boat. Standing on the shore it hits you - the silence. With the sounds of your oar hitting the water gone there is naught to distract from the ominous silence of this impossibly large cavern. Nothing is alive here. There is no wind. Everything is still.", 80))
            print("")
            print("You venture further.\n")
        case 3:
            print(textwrap.fill("Further in you reach a forest nestled deep in within the Gorge. A dense canopy of twisted trees rise from the ground and envelop the space above you, they are impossibly large for how far down you must be now. Your steps are muffled by a carpet of fallen leaves and the snapping of twigs.", 80))
            print("")
            print(textwrap.fill("Yet these sounds are the only ones you hear. Again it hits you - the unnatural silence. It is oppressive.", 80))
            print("")
            print(textwrap.fill("The deeper in you go, however, the more signs of life you see. Old rusted weapons. Bones. Blood.", 80))
            print("")
            print("Something lurks nearby.\n")
        case 4:
            print(textwrap.fill("You escape the forest and navigate a series of labyrinthian passages for what feels like an eternity. The walls here are covered in intricate carvings depicting The Gorgon, a gigantic figure with long flowing braids of hair that are sentient in and of themselves. They look snake-like in form.", 80))
            print("")
            print(textwrap.fill("The Gorgon's victims are depicted here too. So many of them - all turned to stone as a result of the Gorgon's fearsome, legendary gaze. While the hair looks to drape over the monster's eyes it seems they will dance and move of their own accord.", 80))
            print("")
            print(textwrap.fill("It would be wise to raise your shield and hide, you think, if the hair showed signs of moving, lest you end up nothing more than another cautionary tale carved into these ancient walls.", 80))
            print("")
            print(textwrap.fill("You turn a corner. The cavern widens into a vast chamber littered with the crumbling bodies of those who came before you, their panicked and pained expressions of terror frozen in stone. At the center of the room lays a stone altar drapes in an eerie ethereal glow.", 80))
            print("")
            print("You stand on the precipice of the Gorgon's lair.\n")

def shop_screen(flee):
    """
    Displays items and stats the player can buy in between battles. Displays an array of items and upradable stats and takes user
    input, if it matches then moves onto shop_quantity_input to take the quantity required to finalise the purchase. 
    """
    print("A voice rings out from the aether.")
    print('"Looking for potions? Or do you want to increase your stats?"')
    while True:
        print(shop)
        print(f"Current Gold: {player.gold}\n")
        shop_input = input("Commands: Type name of item/stat above | status | exit \n\n")
        shop_lower = shop
        shop_lower = {letters.lower(): l for letters, l in shop_lower.items()}
        if shop_input.lower() in shop_lower and shop_input.lower() != "potion":
            print(f'"Ahh, you want to upgrade your {shop_input}?"')
            shop_quantity_input(shop_input, shop_lower)
        elif shop_input.lower() == "potion":
            print('"Aah a potion? 3 gold each."')
            shop_quantity_input(shop_input, shop_lower)
        elif shop_input.lower() == "status":
            player.status()
            print('"You still want to buy something?"')
        elif shop_input.lower() == "exit":
            print('"See you around."')
            leave_shop = True
            print("The voice dissipates - You return your attention to your surroundings. \n")
            field_screen(flee, leave_shop)
        else:
            print('"We do not stock that item, ask again."')

def shop_quantity_input(shop_input, shop_lower):
        """
        Takes quantity of items player wants to buy, validates if a number is entered and if they can afford it,
        then adds purchase to the player object and returns them to the shop screen.
        """
        while True:
            buying = shop_lower.get(shop_input.lower())
            quantity = wordtodigits.convert(input('"How many do you want?"\n\n'))
            if shop_quantity_input_validation(quantity):
                quantity = int(quantity)
                gold_needed = buying * quantity
                if quantity == 0:
                    print('"Want something else, then?"')
                    break
                print(f'"You want {quantity}? That will be {gold_needed} gold in total."')
                print('"Are you sure?"')
                print(f"Current Gold: {player.gold}\n")
                while True:
                    yes_no = input("Commands: yes | no\n\n")
                    if yes_no.lower() == "yes" and player.gold >= gold_needed:
                        match shop_input.lower():
                            case "potion":
                                player.potions += quantity
                                print('"They leave a bad taste in your mouth, but it beats being dead."')
                            case "hp":
                                player.max_hp += quantity
                                player.current_hp += quantity
                                print('"Feeling healthier already, I bet."')
                            case "defense":
                                player.defense += quantity
                                print('"If nothing can hurt you then nothing can kill you. Good choice."')
                            case "attack":
                                player.attack += quantity
                                print('"The best offense is a good offense, I always say."')
                        player.gold -= gold_needed
                        print('"Pleasure doing business."')
                        break
                    if yes_no.lower() == "yes" and player.gold < gold_needed:
                        print('"No credit, cash only. Come back when you have enough."')
                        break
                    if yes_no.lower() == "no":
                        print('"Want something else?"')
                        break
                    else: print("Invalid input")
                break

def shop_quantity_input_validation(quantity):
    """
    Ensures the quantity input in the shop is a valid integer between 0 and 99 and returns an error if not.
    """
    try: 
        quantity = int(quantity)
        if quantity < 0 or quantity >=100:
            raise ValueError()
    except ValueError:
        print(f"Input invalid: Please enter a number between 0 and 99.\n")
        return False
    else:
        return True

def battle_screen(flee):
    """
    Takes players commands during a battle and executes the relevant player object function
    """
    monster = initialise_battle()
    monster.introduction(flee)
       
    while True:
        print(f"Current HP: {player.current_hp}/{player.max_hp}")
        battle_input = input("Commands: attack | defend | potion | status | flee\n\n")
        if battle_input.lower() == "attack":
            player.attack_command(monster)
            monster.action_determiner()
        elif battle_input.lower() == "defend":
            original_defense = player.defense
            player.defend(monster)
            monster.action_determiner()
            player.defense = original_defense
        elif battle_input.lower() == "potion":
            if player.potions > 0:
                player.potion()
                monster.action_determiner()
            else:
                print("You reach for a potion, but have none.")
                print(f"The {monster.name} awaits your input.\n")
        elif battle_input.lower() == "status":
            player.status()
            print(f"The {monster.name} awaits your input.\n")
        elif battle_input.lower() == "flee":
            player.flee(monster)
        else:
            print("Input not recognised.\n")

def initialise_battle():
    """
    Generates an enemy for the player to fight with difficulty based off the number of previous fights won.
    """
    match player.battles_won:
        case 0:
            monster = Gorgon()
            return monster  
        case 1:
            monster = Siren()
            return monster
        case 2: 
            monster = Sprite()
            return monster  
        case 3: 
            monster = Troll()
            return monster       
        case 4:
            monster = Gorgon()
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
    print(f"The {monster.name} inflicts {damage} points of damage to you.\n")

def game_over():
    """
    Called when the player's HP reaches 0 - they have lost. Runs play again function to see if the player wants to restar and play again.
    """
    print(f"Current HP: {player.current_hp}/{player.max_hp}")
    print("Your journey is over - Gorgon Gorge claims the life of another.")
    print("Surely the fates will be kinder to the next.\n")
    play_again()

def game_win():
    """
    When the player beats the Gorgon - displays the final character statistics and a congratulatory message before asking if they want to play again.
    """
    print("The body of the Gorgon lies motionless on the floor.")
    print(textwrap.fill("Centuries of myth and legend, struck down single-handedly by you. Her riches are all yours.", 80))
    print(f"The tale of {player.name} will be passed down in legend.")
    print(f"The tale of {player.name}, The Gorgon Slayer.\n")
    player.status()
    play_again()

def play_again():
    """
    Takes yes/no command to see if they want to play again from the start. Yes will restart game, no will quit game.
    """
    print("Play again?")
    while True:
        yes_no = input("Commands: yes | no \n\n")
        if yes_no.lower() == "yes":
            main()
        elif yes_no.lower() == "no":
            print("Quitting...\n")
            sys.exit()
        else:
            print("Input not recognised.\n")
    
def main():
    """
    Run all program functions.
    """
    global player
    global flee
    global leave_shop
    player = Player("", 5, 10, 10, 5, 3, 19, 1, 0)
    title_screen()
    player_name_input()
    flee = False
    leave_shop = False
    field_screen(flee, leave_shop)

main()