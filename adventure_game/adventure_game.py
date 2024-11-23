# adventure_game.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import random
import pickle
import sys
from PIL import Image, ImageTk  # Import for image handling

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
        self.player_choice = None  # Track player's significant choice
        self.quests = {
            'main_quest': {
                'active': False,
                'completed': False,
                'description': 'Defeat the dragon and retrieve the golden apple.',
                'reward': None,
            },
            'stranger_quest': {
                'active': False,
                'completed': False,
                'description': 'Help the Mysterious Stranger by retrieving the cursed amulet.',
                'reward': None,
            },
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
        cursed_amulet = Item('cursed amulet', 'An amulet with dark energy.', weight=2)

        # Quest reward
        ring_of_power = Item('ring of power', 'An enchanted ring that increases your attack.', weight=1, effect=self.increase_attack_power_quest)
        self.quests['main_quest']['reward'] = ring_of_power

        # Place items in rooms

        # Library items
        library.items.extend([spellbook, health_potion])
        # Armory items
        armory.items.append(sword)
        # Dungeon items (powered sword)
        dungeon.items.append(ancient_sword)
        # Kitchen items
        kitchen.items.extend([key, health_potion])
        # Mystic Chamber items
        mystic_chamber.items.extend([mysterious_amulet, cursed_amulet])
        # Secret Cave items
        secret_cave.items.append(magic_lamp)
        # Observatory items
        observatory.items.append(star_map)
        # Crypt items (golden apple)
        crypt.items.append(golden_apple)
        # Crypt items (lost crown)
        crypt.items.append(lost_crown)
        # Add another health potion to Armory for accessibility
        armory.items.append(health_potion)

        # Create enemies
        goblin = Enemy('Goblin', health=30, attack=10, description='A sneaky goblin.')
        dragon = Enemy('Dragon', health=100, attack=25, description='A massive dragon with fiery breath.')
        evil_spirit = Enemy('Evil Spirit', health=50, attack=15, description='A malevolent entity.')

        # Place enemies
        crypt.enemy = dragon
        dungeon.enemy = evil_spirit
        armory.enemy = goblin  # Optionally add a goblin to the armory

        # Create the Mysterious Stranger NPC
        self.mysterious_stranger = {
            'name': 'Mysterious Stranger',
            'description': 'A cloaked figure with an unknown agenda.',
            'location': self.rooms['Garden'],
        }

    def heal_player(self, player, gui):
        player.health += 30
        gui.display_message("You use a health potion and recover 30 health points.", 'system')
        gui.display_message(f"Your health is now {player.health}.", 'system')

    def increase_attack(self, player, gui):
        player.attack += 10
        gui.display_message("You feel a surge of power. Your attack increases by 10!", 'system')

    def increase_attack_power(self, player, gui):
        player.attack += 20
        gui.display_message("You feel immense power coursing through you. Your attack increases by 20!", 'system')

    def increase_attack_power_quest(self, player, gui):
        player.attack += 15
        gui.display_message("The ring glows as you wear it. Your attack increases by 15!", 'system')

    def play(self, gui):
        self.setup()
        gui.display_location()
        # Removed automatic instructions display

    def save_game(self):
        with open('savegame.pkl', 'wb') as f:
            # Exclude unpickleable objects
            state = self.__dict__.copy()
            # Remove any references to the GUI
            if 'gui' in state:
                del state['gui']
            pickle.dump(state, f)
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
        # Original victory condition
        if any(item.name == 'golden apple' for item in self.player.inventory) and self.current_room.name == 'Tower':
            if self.player_choice == 'declined_stranger':
                gui.bad_ending()
            else:
                gui.display_message("\nYou bite into the golden apple atop the tower. Enlightenment floods over you.", 'system')
                gui.display_message("Congratulations, you have achieved ultimate knowledge!", 'system')
                self.running = False
                gui.game_over()
        # Check for the stranger's quest completion
        if self.quests['stranger_quest']['active'] and self.quests['stranger_quest']['completed']:
            gui.display_message("\nYou have completed the Mysterious Stranger's quest.", 'npc')
            gui.display_message("As a reward, the stranger reveals a hidden path leading to a secret ending.", 'npc')
            self.running = False
            gui.secret_ending()

    def check_quest_completion(self, gui):
        if self.quests['main_quest']['active'] and any(item.name == 'lost crown' for item in self.player.inventory):
            self.quests['main_quest']['active'] = False
            self.quests['main_quest']['completed'] = True
            self.player.add_item(self.quests['main_quest']['reward'])
            gui.display_message("You have completed the quest and received the ring of power!", 'system')
            self.player.inventory.remove(next(item for item in self.player.inventory if item.name == 'lost crown'))

    def solve_riddle(self, room, gui):
        gui.display_message("A voice echoes: 'I speak without a mouth and hear without ears. I have nobody, but I come alive with the wind. What am I?'", 'system')
        answer = gui.get_player_input("Your answer: ").strip().lower()
        if answer == 'echo':
            gui.display_message("The door creaks open as you answer correctly.", 'system')
            room.locked = False
            self.previous_room = self.current_room
            self.current_room = room
            gui.display_location()
        else:
            gui.display_message("The voice says, 'Incorrect. You may not enter.'", 'system')

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
        self.window.configure(bg='#A9A9A9')  # Stone grey background

        # Load background image (optional)
        try:
            bg_image = Image.open('castle_background.png')  # Replace with your image file
            bg_photo = ImageTk.PhotoImage(bg_image)
            background_label = tk.Label(self.window, image=bg_photo)
            background_label.place(relwidth=1, relheight=1)
            self.bg_photo = bg_photo
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Create frames
        top_frame = tk.Frame(self.window, bg='#A9A9A9')
        top_frame.pack(fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.window, bg='#A9A9A9')
        bottom_frame.pack(fill=tk.X)

        # Create text area
        self.text_area = scrolledtext.ScrolledText(
            top_frame, wrap=tk.WORD, width=80, height=20, state='disabled',
            bg='#D3D3D3',  # Light grey background
            fg='#2F4F4F',  # Dark slate grey text
            font=('Helvetica', 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Define text tags with updated colors
        self.text_area.tag_config('system', foreground='#2F4F4F', background='#D3D3D3', font=('Helvetica', 12))
        self.text_area.tag_config('player', foreground='#000080', background='#D3D3D3', font=('Helvetica', 12, 'italic'))  # Navy blue
        self.text_area.tag_config('enemy', foreground='#800000', background='#D3D3D3', font=('Helvetica', 12, 'bold'))  # Maroon
        self.text_area.tag_config('input', foreground='#006400', background='#D3D3D3', font=('Helvetica', 12))  # Dark green
        self.text_area.tag_config('npc', foreground='#8B4513', background='#D3D3D3', font=('Helvetica', 12, 'italic'))  # Saddle brown

        # Create action buttons
        button_frame = tk.Frame(bottom_frame, bg='#A9A9A9')
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)

        commands = ['north', 'south', 'east', 'west', 'up', 'down', 'look', 'inventory', 'save', 'load', 'talk']

        for cmd in commands:
            action_button = tk.Button(
                button_frame, text=cmd.capitalize(),
                command=lambda c=cmd: self.execute_command(c),
                bg='#DAA520',  # Goldenrod background
                fg='#000000',  # Black text
                width=8
            )
            action_button.pack(side=tk.LEFT, padx=2)

        # Create entry field
        self.entry = tk.Entry(
            bottom_frame, width=80,
            bg='#F5F5DC',  # Beige background
            fg='#2F4F4F',  # Dark slate grey text
            insertbackground='#2F4F4F'  # Cursor color
        )
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry.bind('<Return>', self.process_input)

        # Initialize input_var
        self.input_var = tk.StringVar()

        # Create Game instance
        self.game = Game()

        # Start the game
        self.game.play(self)

    def display_message(self, message, msg_type='system'):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"{message}\n", msg_type)
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def display_location(self):
        room = self.game.current_room
        self.display_message('\n------------------------------', 'system')
        self.display_message(f"You are in the {room.name}.", 'system')
        self.display_message(room.description, 'system')

        # Show available items
        if room.items:
            self.display_message("You see the following items:", 'system')
            for item in room.items:
                self.display_message(f"- {item.name}: {item.description}", 'system')

        # Show available exits
        self.display_message(f"Exits: {', '.join(room.exits.keys())}", 'system')

        # Check for enemy in the room
        if room.enemy:
            self.display_message(f"A {room.enemy.name} is here! {room.enemy.description}", 'enemy')

        # Check for NPC in the room
        if self.game.mysterious_stranger['location'] == room:
            self.display_message(f"You see {self.game.mysterious_stranger['name']} here.", 'npc')

    def display_instructions(self):
        instructions = "\nYou can:\n- Move: 'north', 'south', 'east', 'west', 'up', 'down'\n" \
                       "- Interact: 'get [item]', 'drop [item]', 'use [item]'\n" \
                       "- Other actions: 'search', 'look', 'inventory', 'save', 'load', 'accept quest', 'complete quest', 'talk'\n" \
                       "- Quit: Press 'Esc' key or type 'quit'\n"
        self.display_message(instructions, 'system')

    def display_help(self):
        help_message = "\nYour goal is to kill the dragon, take the golden apple, and go to the tower to win the game.\n" \
                       "You may encounter characters who offer additional quests that can change the outcome of the game.\n" \
                       "Prepare yourself by finding weapons and health potions.\n" \
                       "Explore rooms, defeat enemies, and make choices wisely."
        self.display_message(help_message, 'system')

    def get_player_input(self, prompt=""):
        input_value = simpledialog.askstring("Input", prompt, parent=self.window)
        return input_value or ''

    def process_input(self, event=None):
        action = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        self.display_message(f"\n> {action}", 'input')
        self.handle_command(action)

    def execute_command(self, command):
        self.display_message(f"\n> {command}", 'input')
        self.handle_command(command)

    def handle_command(self, action):
        if not self.game.running or not self.game.player.is_alive():
            return

        if action in ['quit', 'exit']:
            self.quit_game()
            return

        elif action in ['north', 'south', 'east', 'west', 'up', 'down']:
            self.move_player(action)

        elif action == 'search':
            self.game.current_room.search()
            self.display_message("You search the area and discover something!", 'system')
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
            self.display_message("Game saved successfully.", 'system')

        elif action == 'load':
            self.game.load_game()
            self.display_location()

        elif action == 'accept quest':
            self.accept_quest()

        elif action == 'complete quest':
            self.game.check_quest_completion(self)

        elif action == 'instructions':
            self.display_instructions()

        elif action == 'help':
            self.display_help()

        elif action == 'talk':
            self.interact_with_stranger()

        else:
            self.display_message("Invalid action. Type 'instructions' to see available commands.", 'system')

        # Handle enemy in the room
        if self.game.current_room.enemy:
            self.combat(self.game.current_room.enemy)
            if not self.game.player.is_alive():
                self.game_over()
                return

        # Check for quest completion
        if self.game.quests['stranger_quest']['active']:
            if any(item.name == 'cursed amulet' for item in self.game.player.inventory):
                self.game.quests['stranger_quest']['active'] = False
                self.game.quests['stranger_quest']['completed'] = True
                self.display_message("You have retrieved the cursed amulet for the Mysterious Stranger.", 'npc')
                self.game.player.inventory.remove(next(item for item in self.game.player.inventory if item.name == 'cursed amulet'))
                self.game.check_victory_condition(self)

        self.game.check_victory_condition(self)

    def move_player(self, direction):
        room = self.game.current_room
        if direction in room.exits:
            next_room = room.exits[direction]
            if next_room.locked:
                if next_room.name == 'Mystic Chamber':
                    self.game.solve_riddle(next_room, self)
                elif any(item.name == 'key' for item in self.game.player.inventory):
                    self.display_message("You use the key to unlock the door.", 'system')
                    next_room.locked = False
                    self.game.previous_room = self.game.current_room
                    self.game.current_room = next_room
                    self.display_location()
                else:
                    self.display_message("The door is locked. You need a key.", 'system')
            else:
                self.game.previous_room = self.game.current_room
                self.game.current_room = next_room
                self.display_location()
        else:
            self.display_message("You can't go that way.", 'system')

    def get_item(self, item_name):
        room = self.game.current_room
        for item in room.items:
            if item.name == item_name:
                if self.game.player.add_item(item):
                    room.items.remove(item)
                    self.display_message(f"You have picked up the {item.name}.", 'system')
                    if item.effect:
                        item.use(self.game.player, self)
                else:
                    self.display_message("You can't carry any more weight. Consider dropping something.", 'system')
                return
        self.display_message("That item is not here.", 'system')

    def drop_item(self, item_name):
        item = self.game.player.remove_item(item_name)
        if item:
            self.game.current_room.items.append(item)
            self.display_message(f"You have dropped the {item.name}.", 'system')
            if item.name == 'mysterious amulet':
                self.game.player.attack -= 10
                self.display_message("You feel your power wane. Your attack decreases by 10.", 'system')
        else:
            self.display_message("You don't have that item.", 'system')

    def use_item(self, item_name):
        for item in self.game.player.inventory:
            if item.name == item_name:
                item.use(self.game.player, self)
                if item.name == 'health potion':
                    self.game.player.inventory.remove(item)
                return
        self.display_message("You don't have that item.", 'system')

    def show_inventory(self):
        self.display_message(f"Your health: {self.game.player.health}", 'system')
        if self.game.player.inventory:
            self.display_message("You are carrying:", 'system')
            total_weight = self.game.player.calculate_carry_weight()
            for item in self.game.player.inventory:
                self.display_message(f"- {item.name} (Weight: {item.weight})", 'system')
            self.display_message(f"Total carry weight: {total_weight}/{self.game.player.max_weight}", 'system')
        else:
            self.display_message("Your inventory is empty.", 'system')

    def combat(self, enemy):
        self.display_message(f"A wild {enemy.name} appears!", 'enemy')
        while enemy.is_alive() and self.game.player.is_alive():
            action = self.get_player_input("Do you want to 'attack' or 'run'? ").strip().lower()
            if action == 'attack':
                # Player attacks enemy
                enemy.health -= self.game.player.attack
                self.display_message(f"You attack the {enemy.name} for {self.game.player.attack} damage.", 'player')
                # Enemy attacks back if still alive
                if enemy.is_alive():
                    self.game.player.health -= enemy.attack
                    self.display_message(f"The {enemy.name} attacks you for {enemy.attack} damage.", 'enemy')
                    self.display_message(f"Your health is now {self.game.player.health}.", 'system')
                else:
                    self.display_message(f"You have defeated the {enemy.name}!", 'system')
                    self.game.current_room.enemy = None
            elif action == 'run':
                self.display_message("You run back to the previous room.", 'system')
                self.game.current_room = self.game.previous_room if self.game.previous_room else self.game.current_room
                self.display_location()
                break
            else:
                self.display_message("Invalid action. Type 'attack' or 'run'.", 'system')
        if not self.game.player.is_alive():
            self.game_over()

    def accept_quest(self):
        if not self.game.quests['main_quest']['active'] and not self.game.quests['main_quest']['completed']:
            self.game.quests['main_quest']['active'] = True
            self.display_message(f"You have accepted the quest: {self.game.quests['main_quest']['description']}", 'system')
        else:
            self.display_message("You have already accepted or completed the quest.", 'system')

    def interact_with_stranger(self):
        if self.game.current_room == self.game.mysterious_stranger['location']:
            self.display_message("The Mysterious Stranger approaches you.", 'npc')
            choice = self.get_player_input("Do you want to help the stranger? (yes/no) ").strip().lower()
            if choice == 'yes':
                self.game.quests['stranger_quest']['active'] = True
                self.display_message("You agreed to help the Mysterious Stranger.", 'npc')
            else:
                self.display_message("You declined the stranger's request.", 'npc')
                self.game.player_choice = 'declined_stranger'
        else:
            self.display_message("There's no one here to interact with.", 'system')

    def secret_ending(self):
        self.display_message("You follow the hidden path revealed by the Mysterious Stranger.", 'system')
        self.display_message("You discover a secret realm and become its ruler!", 'system')
        self.game_over()

    def bad_ending(self):
        self.display_message("By declining the Mysterious Stranger, you unknowingly invoked a curse.", 'system')
        self.display_message("Darkness consumes the land, and you fade into obscurity.", 'system')
        self.game_over()

    def game_over(self):
        self.display_message("Game Over.", 'system')
        self.game.running = False
        self.entry.configure(state='disabled')
        if self.game.player.is_alive():
            if self.game.player_choice == 'declined_stranger':
                messagebox.showinfo("Bad Ending", "You have reached a tragic end.")
            else:
                messagebox.showinfo("Victory", "Congratulations! You have completed the game.")
        else:
            messagebox.showinfo("Game Over", "You have perished.")
        # Ask the player if they want to play again
        play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
        if play_again:
            self.restart_game()
        else:
            self.window.destroy()
            sys.exit()

    def restart_game(self):
        # Reset the game
        self.game = Game()
        self.entry.configure(state='normal')
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')
        self.game.play(self)

    def quit_game(self):
        if messagebox.askokcancel("Quit Game", "Are you sure you want to quit the game?"):
            self.window.destroy()
            sys.exit()
        else:
            self.game.running = True
            self.entry.configure(state='normal')

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
