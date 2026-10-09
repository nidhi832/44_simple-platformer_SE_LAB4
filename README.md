# Lab 4: VibeCoding — Real-Time Simple Platformer Game

**Course:** Software Engineering Laboratory  
**Student Name:** Srinidhi P  
**SRN:** PES1UG24AM407  
**Pair-Programming Partner:** Google Antigravity (Gemini 3.7 Flash)  
**Main Submission Repo:** [nidhi832/PES1UG24AM407_SELAB](https://github.com/nidhi832/PES1UG24AM407_SELAB)  
**Dedicated Game Repo:** [nidhi832/44_simple-platformer_SE_LAB4](https://github.com/nidhi832/44_simple-platformer_SE_LAB4)

---

## Overview

This project is an enhanced real-time 2D platformer developed in Python with **Pygame**. The lab assignment focused on **VibeCoding** — collaborative, iterative pair programming with an advanced AI coding assistant to diagnose, debug, refactor, and expand a game codebase.

Through prompt engineering and iterative testing, critical game-feel bugs (such as collision tunneling) were eliminated, and key gameplay features (dynamic difficulty selection, sound synthesis, game-over state handling, and hazard balancing) were implemented.

---

## Tasks & Implementations

### Task 1: Refined Platform Collision Detection
* **Issue:** At high falling speeds or after falling from high platforms, the player character suffered from "tunneling" (phasing straight through solid platform floors).
* **Fix:** 
  - Implemented **continuous swept collision detection** along the vertical axis (`prev_bottom <= platform.y + 4 and new_bottom >= platform.y`), checking if the player's downward trajectory intersected the platform's top boundary during the frame step.
  - Added a **terminal velocity cap** (`16.0`) to avoid oversized displacement steps per frame.
  - Properly snaps the player to the platform surface (`y = platform.y - height`) and resets vertical velocity (`vy = 0`).

### Task 2: Game Over Screen & State Machine
* **Issue:** Dying (falling into gaps or colliding with hazards) previously printed to stdout or abruptly exited.
* **Fix:**
  - Introduced explicit `game_over` state tracking within `GameEngine`.
  - Added a semi-transparent darkened overlay (`pygame.SRCALPHA`) with a clear **GAME OVER** banner.
  - Displays the player's **Final Score** and interactive prompt options.
  - Suspends gameplay movement physics while gracefully capturing player inputs.

### Task 3: Replay Menu & Dynamic Difficulty Tuning
* **Issue:** Players had to relaunch the entire game upon dying.
* **Fix:**
  - Added full replay functionality directly from the Game Over screen without restarting the Python process.
  - Implemented 3 selectable difficulty levels with custom-tuned gravity and jump impulse parameters:
    - **Easy (`1` / `E`):** `gravity = 0.45`, `jump_strength = -13.0` (Floaty, forgiving jumps)
    - **Medium (`2` / `M` / `Space` / `Enter`):** `gravity = 0.60`, `jump_strength = -12.0` (Standard balanced platformer physics)
    - **Hard (`3` / `H`):** `gravity = 0.78`, `jump_strength = -11.0` (Fast falls, tight jump timing)
  - Exit shortcut (`Q` / `Escape`) to cleanly quit the application.

### Task 4: Sound Effects & Audio Integration
* **Issue:** The original starter game had zero audio feedback.
* **Fix:**
  - Developed a standalone `SoundManager` class (`game/sound.py`) interfacing with `pygame.mixer`.
  - Synthesized clean 16-bit 44.1 kHz PCM audio assets in `assets/sounds/`:
    - `jump.wav`: Upward frequency sweep triggered when jumping.
    - `goal.wav`: Multi-tone arpeggio fanfare played when touching the green goal pole.
    - `death.wav`: Low-frequency rumble/noise burst played on hazard collision or fall deaths.
  - Built with graceful fallback handling if audio drivers or hardware are unavailable.

### Bonus Balancing: Hazard Geometry Optimization
* **Issue:** The default hazard was positioned awkwardly, rendering the jump nearly impossible on higher difficulties.
* **Fix:** Resized the hazard hitbox to 40px width and centered it cleanly on the platform (`Platform(220, ...)`), making the obstacle fair, readable, and rewarding to leap over.

---

## Controls & Gameplay

| Action | Primary Key | Secondary Key |
| :--- | :--- | :--- |
| **Move Left** | `Left Arrow` | `A` |
| **Move Right** | `Right Arrow` | `D` |
| **Jump** | `Spacebar` | `Up Arrow` / `W` |
| **Replay - Easy** | `1` | `E` |
| **Replay - Medium** | `2` / `Spacebar` / `Enter` | `M` |
| **Replay - Hard** | `3` | `H` |
| **Quit Game** | `Escape` | `Q` |

---

## Directory Structure

```text
simple-platformer-main/
├── assets/
│   └── sounds/
│       ├── jump.wav                 # Synthesized jumping sound effect
│       ├── goal.wav                 # Level completion chime
│       └── death.wav                # Game-over sound effect
├── game/
│   ├── game_engine.py               # Core loop, collision physics & rendering
│   ├── player.py                    # Player entity, movement, jumping & states
│   ├── platform.py                  # Platform dimensions and bounding rect
│   ├── hazard.py                    # Hazard entity & collision boundaries
│   └── sound.py                     # SoundManager & audio loader
├── main.py                          # Game entry point and Pygame initialization
├── requirements.txt                 # Project dependencies (pygame)
├── README.md                        # Complete project documentation
├── Lab-4/
│   ├── Lab4_Chat_History.pdf        # Exported AI pair-programming transcript (PDF)
│   └── Lab4_Chat_History.docx       # Exported AI pair-programming transcript (DOCX)
├── before_coding.mp4                # Gameplay video demonstrating original bugs
└── after_sorting_errors.mp4         # Gameplay video showing all fixes & features
```

---

## Installation & Setup

1. **Prerequisites:** Python 3.10 or higher.
2. **Clone the repository:**
   ```bash
   git clone https://github.com/nidhi832/44_simple-platformer_SE_LAB4.git
   cd 44_simple-platformer_SE_LAB4
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Launch the game:**
   ```bash
   python main.py
   ```

---

## Submission Deliverables Checklist

- [x] **Video (Before Coding):** `before_coding.mp4` — Demonstrates baseline bugs (tunneling fall-through, missing death screen/sound).
- [x] **Video (After Sorting Errors):** `after_sorting_errors.mp4` — Demonstrates fixed continuous collision, audio effects, score counter, game-over screen, and difficulty replays.
- [x] **Updated Code:** All 4 tasks completed, organized, and modularized under `game/` and `assets/`.
- [x] **Chat History Document:** Complete AI pair-programming transcript exported under `Lab-4/` as [`Lab4_Chat_History.pdf`](Lab-4/Lab4_Chat_History.pdf).
