import random
import os
import time
import sys

# ═══════════════════════════════════════════════════════════════
#                    PROFESSIONAL HANGMAN GAME
# ═══════════════════════════════════════════════════════════════

# ── Hangman ASCII Art Stages ──
HANGMAN_STAGES = [
    """
      ┌──────┐
      │      │
      │      
      │      
      │      
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │      
      │      
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │      │
      │      
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │     /│
      │      
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │     /│\\
      │      
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │     /│\\
      │     / 
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │      O
      │     /│\\
      │     / \\
      │      
    ══╧══════
    """,
    """
      ┌──────┐
      │      │
      │     (O)   💀 DEAD!
      │     /│\\
      │     / \\
      │      
    ══╧══════
    """
]

# ── Word Categories ──
WORD_CATEGORIES = {
    "🐍 Programming": [
        "python", "javascript", "algorithm", "function", "variable",
        "database", "framework", "compiler", "debugging", "recursion",
        "inheritance", "polymorphism", "encapsulation", "abstraction",
        "iteration", "exception", "boolean", "integer", "string",
        "dictionary", "terminal", "repository", "middleware", "backend"
    ],
    "🌍 Countries": [
        "australia", "brazil", "canada", "denmark", "ethiopia",
        "france", "germany", "hungary", "indonesia", "japan",
        "kenya", "lebanon", "mexico", "netherlands", "portugal",
        "singapore", "thailand", "ukraine", "venezuela", "zimbabwe"
    ],
    "🎬 Movies": [
        "inception", "interstellar", "gladiator", "titanic", "avatar",
        "parasite", "joker", "frozen", "gravity", "departed",
        "spotlight", "arrival", "dunkirk", "whiplash", "predator",
        "terminator", "braveheart", "godfather", "scarface", "goodfellas"
    ],
    "🔬 Science": [
        "molecule", "electron", "neutron", "gravity", "velocity",
        "photosynthesis", "mitochondria", "chromosome", "ecosystem",
        "thermodynamics", "catalyst", "hypothesis", "evolution",
        "nucleus", "quantum", "relativity", "asteroid", "telescope",
        "organism", "biosphere"
    ],
    "🍕 Food": [
        "spaghetti", "hamburger", "croissant", "avocado", "chocolate",
        "pancakes", "lasagna", "burrito", "dumpling", "sushi",
        "tiramisu", "bruschetta", "guacamole", "mozzarella", "prosciutto",
        "ravioli", "focaccia", "macaroni", "cheesecake", "cinnamon"
    ],
    "🎲 Random Mix": [
        "adventure", "brilliant", "champion", "discovery", "elephant",
        "frequency", "gorgeous", "hurricane", "illusion", "jubilee",
        "knowledge", "labyrinth", "marathon", "nostalgia", "obsidian",
        "paradise", "quartz", "revolution", "symphony", "treasure"
    ]
}

# ── Difficulty Settings ──
DIFFICULTY_SETTINGS = {
    "1": {"name": "Easy", "emoji": "🟢", "max_tries": 8, "hint_allowed": True, "reveal_count": 2},
    "2": {"name": "Medium", "emoji": "🟡", "max_tries": 6, "hint_allowed": True, "reveal_count": 1},
    "3": {"name": "Hard", "emoji": "🔴", "max_tries": 4, "hint_allowed": False, "reveal_count": 0},
    "4": {"name": "Extreme", "emoji": "💀", "max_tries": 3, "hint_allowed": False, "reveal_count": 0}
}


class HangmanGame:
    """Professional Hangman Game Engine"""

    def __init__(self):
        self.total_wins = 0
        self.total_losses = 0
        self.total_score = 0
        self.games_played = 0
        self.best_score = 0
        self.current_streak = 0
        self.best_streak = 0

    # ── Utility Methods ──
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def slow_print(text, delay=0.03):
        """Print text with a typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def print_separator(char="═", length=60):
        """Print a decorative separator line"""
        print(char * length)

    @staticmethod
    def print_header(title):
        """Print a formatted header"""
        print()
        print("═" * 60)
        centered_title = title.center(60)
        print(centered_title)
        print("═" * 60)

    # ── Display Methods ──
    def display_welcome_screen(self):
        """Display the welcome screen with ASCII art"""
        self.clear_screen()
        print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗              ║
    ║          ██║  ██║██╔══██╗████╗  ██║██╔════╝              ║
    ║          ███████║███████║██╔██╗ ██║██║  ███╗             ║
    ║          ██╔══██║██╔══██║██║╚██╗██║██║   ██║             ║
    ║          ██║  ██║██║  ██║██║ ╚████║╚██████╔╝             ║
    ║          ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝              ║
    ║                                                          ║
    ║          ███╗   ███╗ █████╗ ███╗   ██╗                   ║
    ║          ████╗ ████║██╔══██╗████╗  ██║                   ║
    ║          ██╔████╔██║███████║██╔██╗ ██║                   ║
    ║          ██║╚██╔╝██║██╔══██║██║╚██╗██║                   ║
    ║          ██║ ╚═╝ ██║██║  ██║██║ ╚████║                   ║
    ║          ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝                   ║
    ║                                                          ║
    ║            🎮  THE ULTIMATE WORD GUESSING GAME  🎮       ║
    ║                     Version 2.0                          ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
        """)
        self.slow_print("    Press ENTER to start the game...", 0.02)
        input()

    def display_stats(self):
        """Display the player's statistics"""
        print("\n    ┌─────────── 📊 YOUR STATISTICS ───────────┐")
        print(f"    │  Games Played  : {self.games_played:<25}│")
        print(f"    │  Wins          : {self.total_wins:<25}│")
        print(f"    │  Losses        : {self.total_losses:<25}│")

        win_rate = (self.total_wins / self.games_played * 100) if self.games_played > 0 else 0
        print(f"    │  Win Rate      : {win_rate:.1f}%{' ' * (24 - len(f'{win_rate:.1f}%'))}│")
        print(f"    │  Total Score   : {self.total_score:<25}│")
        print(f"    │  Best Score    : {self.best_score:<25}│")
        print(f"    │  Current Streak: {self.current_streak:<25}│")
        print(f"    │  Best Streak   : {self.best_streak:<25}��")
        print("    └─────────────────────────────────────────┘")

    def display_game_state(self, word, guessed_letters, tries_left, max_tries,
                           difficulty_name, category_name, score, hint_used):
        """Display the current game state"""
        self.clear_screen()

        # Header
        print("═" * 60)
        print(f"  🎮 HANGMAN  │  {difficulty_name}  │  {category_name}")
        print(f"  💰 Score: {score}  │  🔥 Streak: {self.current_streak}")
        print("═" * 60)

        # Hangman figure - map tries_left to stage index
        total_stages = len(HANGMAN_STAGES) - 1  # 7 stages (0-7)
        mistakes = max_tries - tries_left
        stage_index = min(int(mistakes * total_stages / max_tries), total_stages)
        print(HANGMAN_STAGES[stage_index])

        # Word display
        display_word = ""
        for letter in word:
            if letter in guessed_letters:
                display_word += f" {letter.upper()} "
            else:
                display_word += " _ "

        print(f"    Word: {display_word}")
        print(f"    Letters: {len(word)} | Unique: {len(set(word))}")

        # Progress bar
        progress = sum(1 for l in set(word) if l in guessed_letters)
        total_unique = len(set(word))
        bar_length = 30
        filled = int(bar_length * progress / total_unique) if total_unique > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = (progress / total_unique * 100) if total_unique > 0 else 0
        print(f"    Progress: [{bar}] {percentage:.0f}%")

        # Tries remaining
        hearts = "❤️ " * tries_left + "🖤 " * (max_tries - tries_left)
        print(f"\n    Lives: {hearts} ({tries_left}/{max_tries})")

        # Guessed letters
        if guessed_letters:
            correct = [l.upper() for l in guessed_letters if l in word]
            wrong = [l.upper() for l in guessed_letters if l not in word]
            if correct:
                print(f"    ✅ Correct: {', '.join(sorted(correct))}")
            if wrong:
                print(f"    ❌ Wrong  : {', '.join(sorted(wrong))}")

        # Available letters
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        available = [l.upper() for l in alphabet if l not in guessed_letters]
        available_str = " ".join(available)
        print(f"\n    📝 Available: {available_str}")

        # Hint status
        if hint_used:
            print("    💡 Hint: USED")

        self.print_separator("─")

    # ── Menu Methods ──
    def select_category(self):
        """Let the player select a word category"""
        self.clear_screen()
        self.print_header("📚 SELECT A CATEGORY")
        print()

        categories = list(WORD_CATEGORIES.keys())
        for i, category in enumerate(categories, 1):
            word_count = len(WORD_CATEGORIES[category])
            print(f"    [{i}] {category} ({word_count} words)")

        print(f"\n    [0] 🎲 Random Category")
        print()

        while True:
            choice = input("    Enter your choice: ").strip()
            if choice == "0":
                selected = random.choice(categories)
                print(f"\n    🎲 Randomly selected: {selected}")
                time.sleep(1)
                return selected
            elif choice.isdigit() and 1 <= int(choice) <= len(categories):
                return categories[int(choice) - 1]
            else:
                print("    ⚠️  Invalid choice. Try again.")

    def select_difficulty(self):
        """Let the player select a difficulty level"""
        self.clear_screen()
        self.print_header("⚙️  SELECT DIFFICULTY")
        print()

        for key, settings in DIFFICULTY_SETTINGS.items():
            hint_status = "Yes" if settings["hint_allowed"] else "No"
            print(f"    [{key}] {settings['emoji']} {settings['name']:<10} │ "
                  f"Lives: {settings['max_tries']} │ Hints: {hint_status}")

        print()

        while True:
            choice = input("    Enter your choice (1-4): ").strip()
            if choice in DIFFICULTY_SETTINGS:
                selected = DIFFICULTY_SETTINGS[choice]
                print(f"\n    {selected['emoji']} Difficulty set to: {selected['name']}")
                time.sleep(1)
                return selected
            else:
                print("    ⚠️  Invalid choice. Enter 1, 2, 3, or 4.")

    # ── Core Game Logic ──
    def calculate_score(self, word, tries_left, max_tries, hint_used, time_taken):
        """Calculate the score for the current round"""
        base_score = len(word) * 10
        difficulty_bonus = {8: 1.0, 6: 1.5, 4: 2.0, 3: 3.0}.get(max_tries, 1.0)
        remaining_lives_bonus = tries_left * 15
        hint_penalty = 25 if hint_used else 0
        time_bonus = max(0, int(50 - time_taken / 2))  # Faster = more bonus
        streak_bonus = self.current_streak * 10

        total = int((base_score + remaining_lives_bonus + time_bonus + streak_bonus)
                     * difficulty_bonus - hint_penalty)
        return max(total, 10)  # Minimum score of 10

    def give_hint(self, word, guessed_letters):
        """Reveal a random unguessed letter as a hint"""
        unrevealed = [l for l in set(word) if l not in guessed_letters]
        if unrevealed:
            hint_letter = random.choice(unrevealed)
            return hint_letter
        return None

    def play_round(self):
        """Play a single round of Hangman"""
        # Setup
        category = self.select_category()
        difficulty = self.select_difficulty()

        word = random.choice(WORD_CATEGORIES[category])
        max_tries = difficulty["max_tries"]
        tries_left = max_tries
        guessed_letters = []
        hint_used = False
        hint_allowed = difficulty["hint_allowed"]
        score = 0

        # Reveal letters for easier difficulties
        reveal_count = difficulty.get("reveal_count", 0)
        if reveal_count > 0:
            unique_letters = list(set(word))
            reveal = random.sample(unique_letters, min(reveal_count, len(unique_letters)))
            guessed_letters.extend(reveal)

        start_time = time.time()

        # Game Loop
        while tries_left > 0:
            self.display_game_state(
                word, guessed_letters, tries_left, max_tries,
                f"{difficulty['emoji']} {difficulty['name']}", category, score, hint_used
            )

            # Check win condition
            if all(letter in guessed_letters for letter in word):
                time_taken = time.time() - start_time
                score = self.calculate_score(word, tries_left, max_tries, hint_used, time_taken)
                self.total_score += score
                self.total_wins += 1
                self.current_streak += 1

                if score > self.best_score:
                    self.best_score = score
                if self.current_streak > self.best_streak:
                    self.best_streak = self.current_streak

                self.display_game_state(
                    word, guessed_letters, tries_left, max_tries,
                    f"{difficulty['emoji']} {difficulty['name']}", category, score, hint_used
                )

                print("\n    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
                print("    ✅  CONGRATULATIONS! YOU WON!")
                print(f"    📝  The word was: {word.upper()}")
                print(f"    💰  Score earned: +{score} points")
                print(f"    ⏱️   Time taken: {time_taken:.1f} seconds")
                print(f"    🔥  Win Streak: {self.current_streak}")
                print("    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
                return True

            # Get input
            if hint_allowed and not hint_used:
                print("    Type a letter to guess, or 'hint' for a hint")

            guess = input("\n    🔤 Your guess: ").strip().lower()

            # Handle hint request
            if guess == "hint":
                if not hint_allowed:
                    print("\n    🚫 Hints are not available in this difficulty!")
                    time.sleep(1.5)
                    continue
                if hint_used:
                    print("\n    ⚠️  You already used your hint!")
                    time.sleep(1.5)
                    continue

                hint_letter = self.give_hint(word, guessed_letters)
                if hint_letter:
                    guessed_letters.append(hint_letter)
                    hint_used = True
                    print(f"\n    💡 Hint: The letter '{hint_letter.upper()}' is in the word!")
                    time.sleep(2)
                continue

            # Handle quit
            if guess == "quit" or guess == "exit":
                print("\n    👋 Quitting current round...")
                self.total_losses += 1
                self.current_streak = 0
                time.sleep(1.5)
                return False

            # Input validation
            if len(guess) != 1:
                print("\n    ⚠️  Please enter a single letter!")
                time.sleep(1.5)
                continue

            if not guess.isalpha():
                print("\n    ⚠️  Please enter a valid letter (A-Z)!")
                time.sleep(1.5)
                continue

            if guess in guessed_letters:
                print(f"\n    ⚠️  You already guessed '{guess.upper()}'! Try another letter.")
                time.sleep(1.5)
                continue

            # Process guess
            guessed_letters.append(guess)

            if guess in word:
                occurrences = word.count(guess)
                print(f"\n    ✅ Correct! '{guess.upper()}' appears {occurrences} time(s)!")
                time.sleep(1)
            else:
                tries_left -= 1
                print(f"\n    ❌ Wrong! '{guess.upper()}' is not in the word.")
                if tries_left > 0:
                    print(f"    💔 Lives remaining: {tries_left}")
                time.sleep(1.5)

        # Game Over - Lost
        time_taken = time.time() - start_time
        self.total_losses += 1
        self.current_streak = 0

        self.display_game_state(
            word, guessed_letters, tries_left, max_tries,
            f"{difficulty['emoji']} {difficulty['name']}", category, 0, hint_used
        )

        print("\n    ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ")
        print("    💀  GAME OVER! THE HANGMAN GOT YOU!")
        print(f"    📝  The word was: ✨ {word.upper()} ✨")
        print(f"    ⏱️   Time taken: {time_taken:.1f} seconds")
        print(f"    😢  Streak reset to 0")
        print("    ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ☠️ ")
        return False

    # ── Main Game Loop ──
    def main_menu(self):
        """Display the main menu"""
        self.clear_screen()
        self.print_header("🎮 HANGMAN - MAIN MENU")
        print()
        print("    [1] 🎮  New Game")
        print("    [2] 📊  View Statistics")
        print("    [3] 📖  How to Play")
        print("    [4] 🚪  Exit")
        print()

        choice = input("    Enter your choice: ").strip()
        return choice

    def show_how_to_play(self):
        """Display the how-to-play guide"""
        self.clear_screen()
        self.print_header("📖 HOW TO PLAY")
        print("""
    🎯 OBJECTIVE:
       Guess the hidden word one letter at a time before
       the hangman is fully drawn!

    📋 RULES:
       • Each round, a random word is selected from your
         chosen category.
       • Guess one letter at a time.
       • Correct guesses reveal the letter's position(s).
       • Wrong guesses cost you a life and add a body part.
       • You win by guessing all letters before running
         out of lives!

    💡 HINTS:
       • Available in Easy and Medium difficulties.
       • Type 'hint' instead of a letter to reveal one.
       • You get only ONE hint per round.
       • Using a hint reduces your final score.

    💰 SCORING:
       • Base points for word length.
       • Bonus for remaining lives.
       • Bonus for speed.
       • Multiplier based on difficulty.
       • Streak bonuses for consecutive wins!

    ⌨️  SPECIAL COMMANDS:
       • Type 'hint' for a hint (if available).
       • Type 'quit' or 'exit' to leave the round.
        """)
        input("    Press ENTER to return to menu...")

    def run(self):
        """Run the main game"""
        self.display_welcome_screen()

        while True:
            choice = self.main_menu()

            if choice == "1":
                self.games_played += 1
                self.play_round()
                print()
                input("    Press ENTER to continue...")

            elif choice == "2":
                self.clear_screen()
                self.print_header("📊 PLAYER STATISTICS")
                self.display_stats()
                print()
                input("    Press ENTER to return to menu...")

            elif choice == "3":
                self.show_how_to_play()

            elif choice == "4":
                self.clear_screen()
                print()
                self.print_separator("═")
                print()
                if self.games_played > 0:
                    print("    📊 FINAL SESSION STATISTICS:")
                    self.display_stats()
                    print()

                self.slow_print("    👋 Thanks for playing Hangman!", 0.03)
                self.slow_print("    🎮 See you next time!", 0.03)
                print()
                self.print_separator("═")
                print()
                break

            else:
                print("\n    ⚠️  Invalid choice. Please try again.")
                time.sleep(1.5)


# ═══════════════════════════════════════════════════════════════
#                         ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    game = HangmanGame()
    game.run()
