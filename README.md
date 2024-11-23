# Adventure Game

Welcome to the **Adventure Game**! This is a text-based adventure game where you explore a mysterious castle, interact with characters, solve puzzles, and make choices that affect the outcome of your journey.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [How to Play](#how-to-play)
  - [Commands](#commands)
  - [Gameplay Tips](#gameplay-tips)
- [Winning the Game](#winning-the-game)
  - [Endings](#endings)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In this game, you take on the role of an adventurer exploring a grand castle filled with secrets, treasures, and dangers. Your choices and actions determine the path of your adventure and the ending you experience.

## Features

- **Interactive Gameplay**: Move through different rooms, collect items, and interact with characters.
- **Combat System**: Engage in battles with enemies using weapons and items.
- **Inventory Management**: Keep track of items you're carrying and manage your inventory.
- **Multiple Endings**: Your choices lead to different outcomes, enhancing replayability.
- **Puzzles and Riddles**: Solve challenges to unlock new areas and progress the story.
- **Save and Load**: Save your progress and load previous games.

## Installation

### Prerequisites

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Required Libraries**:
  - `tkinter`: Standard library for GUI applications in Python.
  - `Pillow`: For image handling (optional if you don't use images).

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mohamadaliibrahim/Adventure_Game.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Adventure_Game
   ```

3. **Install Required Libraries**:

   ```bash
   pip install pillow
   ```

   *Note*: If `tkinter` is not installed, you may need to install it separately depending on your operating system.

## Running the Game

To start the game, run the `adventure_game.py` script using Python:

```bash
python adventure_game.py
```

*Note*: If you have multiple versions of Python installed, you may need to specify `python3` instead of `python`.

## How to Play

The game is played through a graphical user interface (GUI) that displays descriptions of your surroundings, messages, and input prompts.

### Commands

You can control your character by typing commands into the input field or by using the action buttons provided. Here are the available commands:

- **Movement**:
  - `north`, `south`, `east`, `west`, `up`, `down`

- **Interaction**:
  - `get [item]`: Pick up an item (e.g., `get sword`).
  - `drop [item]`: Drop an item from your inventory.
  - `use [item]`: Use an item (e.g., `use health potion`).
  - `talk`: Interact with characters in the room.

- **Other Actions**:
  - `search`: Search the area for hidden items or paths.
  - `look`: Redisplay the description of your current location.
  - `inventory`: View items you're carrying and your health status.
  - `save`: Save your current game progress.
  - `load`: Load a previously saved game.
  - `instructions`: Display the list of available commands.
  - `help`: Get guidance on what to do in the game.
  - `accept quest`: Accept an available quest.
  - `complete quest`: Attempt to complete an active quest.

- **Quit the Game**:
  - Type `quit` or press the `Esc` key.

### Gameplay Tips

- **Exploration**: Move through different rooms to discover items and characters.
- **Preparation**: Collect weapons and health potions to prepare for battles.
- **Combat**: When encountering enemies, choose to `attack` or `run`.
- **Inventory Management**: Keep an eye on your carry weight limit and manage your items accordingly.
- **Interacting with Characters**: Use the `talk` command to interact with non-player characters (NPCs).
- **Solving Puzzles**: Pay attention to riddles and challenges that unlock new areas.

## Winning the Game

Your main objective is to explore the castle, make choices, and achieve one of the possible endings based on your actions.

### Endings

#### **1. Secret Ending: Become the Ruler of a Secret Realm**

- **How to Achieve**:
  - Go to the **Garden** by moving `west` from the Entrance Hall.
  - Use `talk` to interact with the **Mysterious Stranger**.
  - Agree to help by typing `yes` when prompted.
  - Retrieve the **cursed amulet** from the **Mystic Chamber**:
    - Go to the **Library** (`east` then `north` from the Entrance Hall).
    - Attempt to go `north` to the Mystic Chamber.
    - Solve the riddle by typing `echo` as the answer.
    - Use `get cursed amulet` to pick up the amulet.
  - Return to the **Mysterious Stranger** in the Garden.
  - Use `talk` to complete the quest.
- **Outcome**: The stranger reveals a hidden path, leading you to become the ruler of a secret realm.

#### **2. Bad Ending: Invoke a Curse by Declining Help**

- **How to Achieve**:
  - Go to the **Garden** and use `talk` to interact with the **Mysterious Stranger**.
  - Decline to help by typing `no` when prompted.
  - Proceed with the main quest:
    - Collect weapons and health potions.
    - Defeat the **Evil Spirit** in the Dungeon and obtain the **ancient sword**.
    - Defeat the **Dragon** in the Crypt and take the **golden apple**.
    - Return to the Entrance Hall and go `up` to the **Tower**.
- **Outcome**: A curse is invoked, leading to a tragic ending.

#### **3. Original Victory**

- **How to Achieve**:
  - Focus on the main quest without fully engaging with the Mysterious Stranger.
  - Collect necessary items and defeat enemies as needed.
  - Defeat the **Dragon** and obtain the **golden apple**.
  - Go to the **Tower** to achieve enlightenment.
- **Outcome**: You complete the game by achieving ultimate knowledge.

## Contributing

Contributions are welcome! If you'd like to improve the game, please follow these steps:

1. **Fork the Repository**: Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your_username/Adventure_Game.git
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your_feature_name
   ```

4. **Make Your Changes**: Implement your improvements or fixes.

5. **Commit Your Changes**:

   ```bash
   git commit -am 'Add new feature or fix'
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/your_feature_name
   ```

7. **Create a Pull Request**: Go to your fork on GitHub and open a pull request to the main repository.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

*Enjoy your adventure, and may your choices lead you to glory!*
