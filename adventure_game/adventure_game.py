# adventure_game.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import random
import pickle
import sys

# Define the Item class
class Item:
    def __init__(self, name, description, weight=0, effect=None):
        self.name = name
        self.description = description
        self.weight = weight
        self.effect = effect  # Function that defines what the item does

    def use(self, player, gui):
        if self.effect:
            self.effect(player, gui)

# Define the Enemy class
class Enemy:
    def __init__(self, name, health, attack, description):
        self.name = name
        self.health = health
        self.attack = attack
        self.description = description

    def is_alive(self):
        return self.health > 0

# Define the Room class
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}        # Dictionary of exits: {'north': Room object}
        self.items = []        # List of Item objects
        self.enemy = None      # Enemy object
        self.locked = False
        self.hidden_exits = {} # For hidden paths

    def add_exit(self, direction, room, locked=False):
        self.exits[direction] = room
        if locked:
            room.locked = True

    def add_hidden_exit(self, direction, room):
        self.hidden_exits[direction] = room

    def search(self):
        self.exits.update(self.hidden_exits)
        self.hidden_exits.clear()

# Define the Player class
class Player:
    def __init__(self):
        self.health = 100
        self.attack = 15
        self.inventory = []
        self.max_weight = 20

    def calculate_carry_weight(self):
        return sum(item.weight for item in self.inventory)

    def add_item(self, item):
        current_weight = self.calculate_carry_weight()
        if current_weight + item.weight <= self.max_weight:
            self.inventory.append(item)
            return True
        else:
            return False

    def remove_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return item
        return None

    def is_alive(self):
        return self.health > 0

# Define the Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.rooms = {}
        self.current_room = None
        self.previous_room = None
        self.running = True
        self.quest = {
            'active': False,
            'completed': False,
            'description': 'Find the lost crown and return it to the King.',
            'reward': None,
        }

    def setup(self):
        # Initialize rooms, items, and enemies
        self.create_world()

    def create_world(self):
        # Create rooms
        entrance_hall = Room('Entrance Hall', 'You are standing in the grand entrance of a mysterious castle.')
        library = Room('Library', 'Rows of ancient books line the walls.')
        armory = Room('Armory', 'Glittering weapons and armor are displayed here.')
        kitchen = Room('Kitchen', 'The smell of old food permeates the air.')
        dungeon = Room('Dungeon', 'A dark, damp dungeon. You hear eerie sounds.')
        mystic_chamber = Room('Mystic Chamber', 'An ancient chamber with walls covered in inscriptions.')
        tower = Room('Tower', 'A tall tower with a breathtaking view.')
        garden = Room('Garden', 'A lush garden with fragrant flowers and hidden paths.')
        secret_cave = Room('Secret Cave', 'A dark cave that holds many secrets.')
        crypt = Room('Crypt', 'An eerie crypt with ancient tombs.')
        observatory = Room('Observatory', 'A room with a large telescope pointing towards the stars.')

        # Set current room
        self.current_room = entrance_hall

        # Define exits
        entrance_hall.add_exit('north', library)
        entrance_hall.add_exit('east', armory)
        entrance_hall.add_exit('west', garden)
        entrance_hall.add_exit('up', tower)

        library.add_exit('south', entrance_hall)
        library.add_exit('east', kitchen)
        library.add_exit('north', mystic_chamber, locked=True)

        armory.add_exit('west', entrance_hall)
        armory.add_exit('down', dungeon)

        kitchen.add_exit('west', library)

        dungeon.add_exit('up', armory)
        dungeon.add_exit('down', crypt)

        mystic_chamber.add_exit('south', library)

        garden.add_exit('east', entrance_hall)
        garden.add_hidden_exit('north', secret_cave)

        secret_cave.add_exit('south', garden)

        tower.add_exit('down', entrance_hall)
        tower.add_exit('up', observatory)

        crypt.add_exit('up', dungeon)

        observatory.add_exit('down', tower)

        # Add rooms to the game
        self.rooms = {
            'Entrance Hall': entrance_hall,
            'Library': library,
            'Armory': armory,
            'Kitchen': kitchen,
            'Dungeon': dungeon,
            'Mystic Chamber': mystic_chamber,
            'Tower': tower,
            'Garden': garden,
            'Secret Cave': secret_cave,
            'Crypt': crypt,
            'Observatory': observatory,
        }

        # Create items
        spellbook = Item('spellbook', 'An ancient spellbook filled with arcane knowledge.', weight=5)
        sword = Item('sword', 'A sharp-looking sword.', weight=10)
        shield = Item('shield', 'A sturdy shield.', weight=8)
        key = Item('key', 'A small rusty key.', weight=1)
        health_potion = Item('health potion', 'A potion that restores health.', weight=2, effect=self.heal_player)
        mysterious_amulet = Item('mysterious amulet', 'An amulet that radiates power.', weight=3, effect=self.increase_attack)
        golden_apple = Item('golden apple', 'A golden apple that shines brightly.', weight=2)
        magic_lamp = Item('magic lamp', 'A lamp that seems to contain something magical.', weight=4)
        ancient_sword = Item('ancient sword', 'A sword with mystical powers.', weight=10, effect=self.increase_attack_power)
        star_map = Item('star map', 'A map of the stars that reveals hidden truths.', weight=1)
        lost_crown = Item('lost crown', 'An ornate crown that seems important.', weight=2)

        # Quest reward
        ring_of_power = Item('ring of power', 'An enchanted ring that increases your attack.', weight=1, effect=self.increase_attack_power_quest)
        self.quest['reward'] = ring_of_power

        # Place items in rooms
        library.items.extend([spellbook, health_potion])
        armory.items.append(sword)
        dungeon.items.append(shield)
        kitchen.items.extend([key, health_potion])
        mystic_chamber.items.append(mysterious_amulet)
        garden.items.append(golden_apple)
        secret_cave.items.append(magic_lamp)
        crypt.items.append(ancient_sword)
        observatory.items.append(star_map)
        crypt.items.append(lost_crown)

        # Create enemies
        goblin = Enemy('Goblin', health=30, attack=10, description='A sneaky goblin.')
        dragon = Enemy('Dragon', health=100, attack=25, description='A massive dragon with fiery breath.')
        crypt.enemy = dragon
        dungeon.enemy = goblin

    def heal_player(self, player, gui):
        player.health += 30
        gui.display_message("You use a health potion and recover 30 health points.")
        gui.display_message(f"Your health is now {player.health}.")

    def increase_attack(self, player, gui):
        player.attack += 10
        gui.display_message("You feel a surge of power. Your attack increases by 10!")

    def increase_attack_power(self, player, gui):
        player.attack += 20
        gui.display_message("You feel immense power coursing through you. Your attack increases by 20!")

    def increase_attack_power_quest(self, player, gui):
        player.attack += 15
        gui.display_message("The ring glows as you wear it. Your attack increases by 15!")

    def play(self, gui):
        self.setup()
        gui.display_location()
        gui.display_instructions()

    def save_game(self):
        with open('savegame.pkl', 'wb') as f:
            # Exclude unpickleable objects
            state = self.__dict__.copy()
            # Remove any references to the GUI
            if 'gui' in state:
                del state['gui']
            pickle.dump(state, f)
        # Inform the user
        print("Game saved successfully.")

    def load_game(self):
        try:
            with open('savegame.pkl', 'rb') as f:
                state = pickle.load(f)
                self.__dict__.update(state)
            print("Game loaded successfully.")
        except FileNotFoundError:
            print("No saved game found.")

    def check_victory_condition(self, gui):
        if any(item.name == 'golden apple' for item in self.player.inventory) and self.current_room.name == 'Tower':
            gui.display_message("\nYou bite into the golden apple atop the tower. Enlightenment floods over you.")
            gui.display_message("Congratulations, you have achieved ultimate knowledge!")
            self.running = False
            gui.game_over()

    def check_quest_completion(self, gui):
        if self.quest['active'] and any(item.name == 'lost crown' for item in self.player.inventory):
            self.quest['active'] = False
            self.quest['completed'] = True
            self.player.add_item(self.quest['reward'])
            gui.display_message("You have completed the quest and received the ring of power!")
            self.player.inventory.remove(next(item for item in self.player.inventory if item.name == 'lost crown'))

    def solve_riddle(self, room, gui):
        gui.display_message("A voice echoes: 'I speak without a mouth and hear without ears. I have nobody, but I come alive with the wind. What am I?'")
        answer = gui.get_player_input("Your answer: ").strip().lower()
        if answer == 'echo':
            gui.display_message("The door creaks open as you answer correctly.")
            room.locked = False
            self.previous_room = self.current_room
            self.current_room = room
            gui.display_location()
        else:
            gui.display_message("The voice says, 'Incorrect. You may not enter.'")

    def create_random_enemy(self):
        enemies = [
            Enemy('Ghost', health=20, attack=5, description='A spooky ghost.'),
            Enemy('Zombie', health=25, attack=7, description='A shambling zombie.'),
            Enemy('Annoyed Squirrel', health=10, attack=3, description='A small but fierce squirrel.'),
            # Add more enemies here
        ]
        return random.choice(enemies)

    def create_random_treasure(self):
        treasures = [
            Item('bag of gold', 'A heavy bag filled with gold coins.', weight=5),
            Item('gemstone', 'A sparkling gemstone.', weight=3),
            Item('ancient artifact', 'An artifact from a bygone era.', weight=7),
            Item('whoopee cushion', 'A classic prank item.', weight=1),
            # Add more treasures here
        ]
        return random.choice(treasures)

# Define the GameGUI class
class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Text Adventure Game")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.bind('<Escape>', self.on_escape)

        # Create widgets
        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=80, height=20, state='disabled')
        self.text_area.pack()

        self.entry = tk.Entry(self.window, width=80)
        self.entry.pack()
        self.entry.bind('<Return>', self.process_input)

        # Initialize input_var
        self.input_var = tk.StringVar()

        # Create Game instance
        self.game = Game()

        # Start the game
        self.game.play(self)

    def display_message(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"{message}\n")
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def display_location(self):
        room = self.game.current_room
        self.display_message('\n------------------------------')
        self.display_message(f"You are in the {room.name}.")
        self.display_message(room.description)

        # Show available items
        if room.items:
            self.display_message("You see the following items:")
            for item in room.items:
                self.display_message(f"- {item.name}: {item.description}")

        # Show available exits
        self.display_message(f"Exits: {', '.join(room.exits.keys())}")

        # Check for enemy in the room
        if room.enemy:
            self.display_message(f"A {room.enemy.name} is here! {room.enemy.description}")

    def display_instructions(self):
        instructions = "\nYou can:\n- Move: 'north', 'south', 'east', 'west', 'up', 'down'\n" \
                       "- Interact: 'get [item]', 'drop [item]', 'use [item]'\n" \
                       "- Other actions: 'search', 'look', 'inventory', 'save', 'load', 'accept quest', 'complete quest'\n" \
                       "- Quit: Press 'Esc' key or type 'quit'\n"
        self.display_message(instructions)

    def get_player_input(self, prompt=""):
        input_value = simpledialog.askstring("Input", prompt, parent=self.window)
        return input_value or ''

    def process_input(self, event=None):
        action = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        self.display_message(f"\n> {action}")

        if not self.game.running or not self.game.player.is_alive():
            return

        if action in ['quit', 'exit']:
            self.game.running = False
            self.game_over()
            return

        elif action in ['north', 'south', 'east', 'west', 'up', 'down']:
            self.move_player(action)

        elif action == 'search':
            self.game.current_room.search()
            self.display_message("You search the area and discover something!")
            self.display_location()

        elif action == 'look':
            self.display_location()

        elif action.startswith('get '):
            item_name = action[4:]
            self.get_item(item_name)

        elif action.startswith('drop '):
            item_name = action[5:]
            self.drop_item(item_name)

        elif action.startswith('use '):
            item_name = action[4:]
            self.use_item(item_name)

        elif action == 'inventory':
            self.show_inventory()

        elif action == 'save':
            self.game.save_game()
            self.display_message("Game saved successfully.")

        elif action == 'load':
            self.game.load_game()
            self.display_location()
            self.display_instructions()

        elif action == 'accept quest':
            self.accept_quest()

        elif action == 'complete quest':
            self.game.check_quest_completion(self)

        else:
            self.display_message("Invalid action.")

        # Handle enemy in the room
        if self.game.current_room.enemy:
            self.combat(self.game.current_room.enemy)
            if not self.game.player.is_alive():
                self.game_over()
                return

        self.game.check_victory_condition(self)
        self.display_instructions()

    def move_player(self, direction):
        room = self.game.current_room
        if direction in room.exits:
            next_room = room.exits[direction]
            if next_room.locked:
                if next_room.name == 'Mystic Chamber':
                    self.game.solve_riddle(next_room, self)
                elif any(item.name == 'key' for item in self.game.player.inventory):
                    self.display_message("You use the key to unlock the door.")
                    next_room.locked = False
                    self.game.previous_room = self.game.current_room
                    self.game.current_room = next_room
                    self.display_location()
                else:
                    self.display_message("The door is locked. You need a key.")
            else:
                self.game.previous_room = self.game.current_room
                self.game.current_room = next_room
                self.display_location()
        else:
            self.display_message("You can't go that way.")

    def get_item(self, item_name):
        room = self.game.current_room
        for item in room.items:
            if item.name == item_name:
                if self.game.player.add_item(item):
                    room.items.remove(item)
                    self.display_message(f"You have picked up the {item.name}.")
                    if item.effect:
                        item.use(self.game.player, self)
                else:
                    self.display_message("You can't carry any more weight. Consider dropping something.")
                return
        self.display_message("That item is not here.")

    def drop_item(self, item_name):
        item = self.game.player.remove_item(item_name)
        if item:
            self.game.current_room.items.append(item)
            self.display_message(f"You have dropped the {item.name}.")
            if item.name == 'mysterious amulet':
                self.game.player.attack -= 10
                self.display_message("You feel your power wane. Your attack decreases by 10.")
        else:
            self.display_message("You don't have that item.")

    def use_item(self, item_name):
        for item in self.game.player.inventory:
            if item.name == item_name:
                item.use(self.game.player, self)
                if item.name == 'health potion':
                    self.game.player.inventory.remove(item)
                return
        self.display_message("You don't have that item.")

    def show_inventory(self):
        self.display_message(f"Your health: {self.game.player.health}")
        if self.game.player.inventory:
            self.display_message("You are carrying:")
            total_weight = self.game.player.calculate_carry_weight()
            for item in self.game.player.inventory:
                self.display_message(f"- {item.name} (Weight: {item.weight})")
            self.display_message(f"Total carry weight: {total_weight}/{self.game.player.max_weight}")
        else:
            self.display_message("Your inventory is empty.")

    def combat(self, enemy):
        self.display_message(f"A wild {enemy.name} appears!")
        while enemy.is_alive() and self.game.player.is_alive():
            action = self.get_player_input("Do you want to 'attack' or 'run'? ").strip().lower()
            if action == 'attack':
                # Player attacks enemy
                enemy.health -= self.game.player.attack
                self.display_message(f"You attack the {enemy.name} for {self.game.player.attack} damage.")
                # Enemy attacks back if still alive
                if enemy.is_alive():
                    self.game.player.health -= enemy.attack
                    self.display_message(f"The {enemy.name} attacks you for {enemy.attack} damage.")
                    self.display_message(f"Your health is now {self.game.player.health}.")
                else:
                    self.display_message(f"You have defeated the {enemy.name}!")
                    self.game.current_room.enemy = None
            elif action == 'run':
                self.display_message("You run back to the previous room.")
                self.game.current_room = self.game.previous_room if self.game.previous_room else self.game.current_room
                self.display_location()
                break
            else:
                self.display_message("Invalid action. Type 'attack' or 'run'.")
        if not self.game.player.is_alive():
            self.game_over()

    def accept_quest(self):
        if not self.game.quest['active'] and not self.game.quest['completed']:
            self.game.quest['active'] = True
            self.display_message(f"You have accepted the quest: {self.game.quest['description']}")
        else:
            self.display_message("You have already accepted or completed the quest.")

    def game_over(self):
        self.display_message("Game Over.")
        self.game.running = False
        self.entry.configure(state='disabled')
        if self.game.player.is_alive():
            messagebox.showinfo("Victory", "Congratulations! You have completed the game.")
        else:
            messagebox.showinfo("Game Over", "You have perished.")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.window.destroy()
            sys.exit()

    def on_escape(self, event):
        self.on_closing()

    def run(self):
        self.window.mainloop()

# Main entry point
if __name__ == "__main__":
    gui = GameGUI()
    gui.run()
