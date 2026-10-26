# Assignment 2: Adversarial Cybersecurity Game (Minimax & Alpha-Beta Pruning)

## Overview
A Python implementation of the two-player zero-sum cybersecurity board game across a 10-host enterprise network (`H0`–`H9`). The Attacker starts from the Internet (`H0`) and attempts to compromise and exfiltrate data from the crown-jewel database (`H5`), while the Defender allocates a budget of `10` to patch, isolate, or restore machines across a maximum of `10` plies.

## Project Structure
| File | Description |
| :--- | :--- |
| `hosts.py` | Defines the `Host` class representing each machine, its asset value, connections, and status flags (`compromised`, `patched`, `isolated`). |
| `GameState.py` | Implements the game engine: legal action generation (`get_possible_actions`), immutable state transitions (`apply_action`), terminal state detection (`is_done`), and Defender utility calculation (`get_util`). |
| `algos.py` | Implements **Minimax**, **Depth-Limited Minimax**, and **Alpha-Beta Pruning** for adversarial move selection. |
| `tests.py` | Contains the Task 1 verification scenarios (legal moves, patching, and winning/exfiltration) and Task 2 algorithm test runners. |
| `main.py` | Initializes the 10-host network topology and provides an interactive CLI menu to run all tasks and algorithms. |

## Requirements & Installation
* **Python Version:** Python 3.10 or higher (uses `match-case` syntax and type annotations).
* **Dependencies:** None (uses only the Python Standard Library).

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/Abdulrehman-Hatem/Assignment-2.git
cd Assignment-2
```

## How to Run
Run the interactive CLI menu from the terminal:
```bash
python main.py
```

### Menu Options
* **`1` — Demonstrate Legal Moves, Patching, and Winning (Task 1):** Runs the three required test cases demonstrating legal moves for both players, patching `H1` (forcing zero-day usage), and an attacker winning sequence via data exfiltration at `H5`.
* **`2` — Run Minimax Algorithm (Full Depth):** Runs standard unpruned Minimax to full game depth (10 plies). *(Note: Full unpruned Minimax evaluates >10M nodes on the opening plies and takes ~2–3 minutes; use Option 3 or Option 4 for instant execution).*
* **`3` — Run Minimax Algorithm with Depth Limit:** Runs Depth-Limited Minimax (enter `3` for the assignment's required 3-ply depth limit; executes in `< 0.05s`).
* **`4` — Run Alpha-Beta Pruning Algorithm (Full Depth):** Runs full 10-ply Alpha-Beta Pruning to completion in `< 1 second` (`U = -44`).
* **`5` — Run Alpha-Beta Pruning Algorithm with Depth Limit:** Runs Depth-Limited Alpha-Beta Pruning at a custom ply depth (e.g., `3`).
* **`0` — Exit:** Closes the program.

## AI Assistants & External Code Disclosure
* **External Libraries / Outside Code:** None used. All game logic and search algorithms were implemented from scratch using standard Python.
* **AI Assistance:** AI tools gemini was used for debugging, code review, and drafting documentation (this readme and the report).

