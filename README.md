# Chess Tactics Manager

The Chess Tactics Manager is a Python program designed to help Lichess.org players systematically practice and improve their tactical skills. It categorizes tactical themes, tracks progress across different difficulty levels, and prioritizes themes based on recall intervals and mastery.

---

## Features

- **Theme Categorization**: Tactics are grouped into logical categories, such as "Core Tactical Motifs" and "Common Mating Patterns." See: [Lichess Puzzle Themes](https://lichess.org/training/themes)
- **Difficulty Tracking**: Tracks progress for each theme across five difficulty levels (`Easiest`, `Easier`, `Normal`, `Harder`, `Hardest`).
- **Recall Intervals**: Recommends themes based on when they were last practiced and their mastery level.
- **Progress Updates**: Allows users to log success rates and puzzle performance to adjust recall and difficulty progress.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ssmythe/tactics_manager.git
   ```
2. Navigate to the project directory:
   ```bash
   cd tactics_manager
   ```
3. Ensure you have Python 3.7 or later installed.

4. Install necessary dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Program
1. Initialize the program:
   ```bash
   python tactics_manager.py
   ```
   ...or...
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
2. Follow the prompts to:
   - View recommended tactical themes to work on.
   - Track success rates and update progress for completed puzzles.
   - Progress through difficulty levels for each theme.

### Test Execution
1. Run the test suite using `pytest`:
   ```bash
   pytest test_tactics_manager.py
   ```
   ...or...
   ```bash
   chmod +x tests.sh
   ./tests.sh
   ```

---

## File Structure

- **tactics_manager.py**: The main program for managing tactical training.
- **test_tactics_manager.py**: Contains tests for verifying the program's logic.
- **tactics_progress.json**: A dynamically created file that tracks user progress.
- **clean.sh**: A utility script to remove generated files, caches, and temporary data.
- **reset_progress.sh**: A utility script to delete all progress data after user confirmation.
- **run.sh**: A wrapper to run the tactics manager program.
- **tests.sh**: A wrapper to run the pytest tests for the tactics manager program.
- **themes.html**: An HTML document with quick links to all the themes on Lichess.org

---

## Utility Scripts

### clean.sh
The `clean.sh` script removes all temporary and generated files, ensuring a clean project state. This includes:

- Python bytecode files (`*.pyc`, `*.pyo`) and `__pycache__` directories.
- pytest cache files (`.pytest_cache`).

#### Usage
1. Make the script executable (if not already):
   ```bash
   chmod +x clean.sh
   ```
2. Run the script:
   ```bash
   ./clean.sh
   ```

This script ensures that all generated files are removed, leaving only the core project files.

### reset_progress.sh
The `reset_progress.sh` script deletes the `tactics_progress.json` file, resetting all progress data. This action requires user confirmation to prevent accidental data loss.

#### Usage
1. Make the script executable (if not already):
   ```bash
   chmod +x reset_progress.sh
   ```
2. Run the script:
   ```bash
   ./reset_progress.sh
   ```
3. Confirm the reset by entering `y` when prompted, or cancel with `n`.

Use this script when you want to start fresh with no saved progress.

---

## Customization

You can customize the tactical themes and intervals by modifying the `THEMES_BY_CATEGORY` or `INTERVALS` constants in `tactics_manager.py`.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality.

---

## License

This project is not licensed. All rights are reserved. If you wish to use, modify, or distribute this project, please contact the author for permission.

---

## Feedback

If you have any feedback, please reach out via GitHub Issues.
