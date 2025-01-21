#!/usr/bin/env python


import json
import datetime
import os

# Constants
DATA_FILE = "tactics_progress.json"
THEMES_BY_CATEGORY = {
    "Core Tactical Motifs": [
        "Fork",
        "Discovered attack",
        "Pin",
        "Skewer",
        "Hanging piece",
        "Capture the defender",
        "Advanced pawn",
        "Exposed king"
    ],
    "Common Mating Patterns": [
        "Back rank mate",
        "Smothered mate",
        "Arabian mate",
        "Anastasia's mate",
        "Dovetail mate",
        "Double bishop mate",
        "Hook mate",
        "Kill box mate",
        "Boden's mate"
    ],
    "Intermediate Tactical Themes": [
        "Sacrifice",
        "Deflection",
        "Attraction",
        "Quiet move",
        "Intermezzo (Zwischenzug)",
        "X-Ray attack",
        "Interference",
        "Trapped piece"
    ],
    "Special Endgame Tactics": [
        "Rook endgame",
        "Pawn endgame",
        "Queen endgame",
        "Knight endgame",
        "Bishop endgame",
        "Queen and rook"
    ],
    "Advanced Concepts": [
        "Zugzwang",
        "Clearance",
        "Promotion",
        "Underpromotion",
        "En passant",
        "Defensive move"
    ],
    "Study by Phases of the Game": [
        "Opening tactics",
        "Middlegame tactics",
        "Endgame tactics"
    ],
    "Mates in Moves": [
        "Mate in 1",
        "Mate in 2",
        "Mate in 3",
        "Mate in 4 or more"
    ],
    "Special Themes and Challenges": [
        "Equality puzzles",
        "Advantage puzzles",
        "Crushing puzzles",
        "Castling"
    ]
}
INTERVALS = {
    "short": 7,  # 1 week
    "medium": 30,  # 1 month
    "long": 90  # 3 months
}
DIFFICULTY_LEVELS = ["Easiest", "Easier", "Normal", "Harder", "Hardest"]
PUZZLES_PER_LEVEL = 50
ACCURACY_THRESHOLD = 80  # Percentage for moving to the next level

# Initialize the data file

def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        data = {
            "themes": {}
        }
        for category, themes in THEMES_BY_CATEGORY.items():
            for theme in themes:
                data["themes"][theme] = {
                    "last_attempted": None,
                    "success_rate": None,
                    "difficulty_progress": {level: {"puzzles_solved": 0, "correct": 0} for level in DIFFICULTY_LEVELS}
                }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Initialized data file with {sum(len(themes) for themes in THEMES_BY_CATEGORY.values())} themes and difficulty levels.")

# Load data from the file

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data back to the file

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Calculate days since last attempt

def days_since(date_str):
    if not date_str:
        return float('inf')  # Treat as never attempted
    last_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return (datetime.datetime.now() - last_date).days

# Determine the next theme to work on

def determine_next_theme(data):
    # Helper function to sort themes by days since last attempt (descending)
    def sort_by_days(theme_list):
        return sorted(theme_list, key=lambda x: x[1], reverse=True)

    unmastered_themes = []
    medium_recall_themes = []
    long_recall_themes = []
    short_recall_themes = []

    for theme, stats in data["themes"].items():
        days = days_since(stats["last_attempted"])

        # Unmastered themes
        if stats["success_rate"] is None or stats["success_rate"] < 8:
            unmastered_themes.append((theme, days))

        # Mastered themes with medium or long recall
        elif days >= INTERVALS["long"]:  # Strictly long interval
            long_recall_themes.append((theme, days))
        elif INTERVALS["medium"] <= days < INTERVALS["long"]:
            medium_recall_themes.append((theme, days))

        # Mastered themes with short recall
        elif days >= INTERVALS["short"]:
            short_recall_themes.append((theme, days))

    # Prioritize unmastered themes (sorted by longest time since last attempt)
    if unmastered_themes:
        return sort_by_days(unmastered_themes)[0][0]

    # Prioritize long recall themes
    if long_recall_themes:
        return sort_by_days(long_recall_themes)[0][0]

    # Prioritize medium recall themes
    if medium_recall_themes:
        return sort_by_days(medium_recall_themes)[0][0]

    # Prioritize short recall themes
    if short_recall_themes:
        return sort_by_days(short_recall_themes)[0][0]

    return None  # All themes are up-to-date

# Determine current difficulty level for a theme

def get_theme_difficulty(data, theme):
    for level in DIFFICULTY_LEVELS:
        progress = data["themes"][theme]["difficulty_progress"][level]
        accuracy = (progress["correct"] / progress["puzzles_solved"] * 100) if progress["puzzles_solved"] > 0 else 0
        if progress["puzzles_solved"] < PUZZLES_PER_LEVEL or accuracy < ACCURACY_THRESHOLD:
            return level
    return None  # All levels completed for this theme

# Update difficulty progress for a theme

def update_theme_difficulty_progress(data, theme, correct):
    current_difficulty = get_theme_difficulty(data, theme)
    if not current_difficulty:
        print(f"All difficulty levels completed for theme: {theme}.")
        return
    progress = data["themes"][theme]["difficulty_progress"].get(current_difficulty)
    if not progress:
        print("Invalid difficulty level.")
        return
    progress["puzzles_solved"] += 1
    if correct:
        progress["correct"] += 1

# Display themes with numbers

def display_themes_with_numbers(data):
    print("Select a theme:")
    index = 1
    for category, themes in THEMES_BY_CATEGORY.items():
        print(f"\n{category}:")
        for theme in themes:
            last_attempted = data["themes"][theme]["last_attempted"]
            success_rate = data["themes"][theme]["success_rate"]
            current_difficulty = get_theme_difficulty(data, theme)
            print(f"{str(index).ljust(3)} {theme.ljust(25)} [{current_difficulty} {last_attempted} {success_rate}/10]")
            index += 1

# Main logic
if __name__ == "__main__":
    initialize_data_file()
    data = load_data()

    # Determine the next theme
    next_theme = determine_next_theme(data)
    if next_theme:
        print(f"Next theme to work on: {next_theme}")
    else:
        print("All themes are up-to-date. Great job!")

    # Determine current difficulty level for the theme
    current_difficulty = get_theme_difficulty(data, next_theme)
    if current_difficulty:
        print(f"Current difficulty level for {next_theme}: {current_difficulty}")
    else:
        print(f"All difficulty levels completed for theme: {next_theme}.")

    # Update progress after a session
    update = input("Did you complete a theme or puzzle session? (y/n): ").strip().lower()[0]
    if update == "y":
        display_themes_with_numbers(data)
        try:
            theme_index = int(input("Enter the number of the theme you practiced: ").strip())
            theme_list = [theme for themes in THEMES_BY_CATEGORY.values() for theme in themes]
            if 1 <= theme_index <= len(theme_list):
                theme = theme_list[theme_index - 1]
                success_rate = int(input("Enter your success rate out of 10: ").strip())
                data["themes"][theme]["last_attempted"] = datetime.datetime.now().strftime("%Y-%m-%d")
                data["themes"][theme]["success_rate"] = success_rate

                # Update difficulty progress for the theme
                for _ in range(10):  # Assuming session is always out of 10 puzzles
                    update_theme_difficulty_progress(data, theme, success_rate > 0)
                    success_rate -= 1

                save_data(data)
                print(f"Updated theme: {theme} and its difficulty progress.")
            else:
                print("Invalid theme number.")
        except ValueError:
            print("Please enter a valid number.")
