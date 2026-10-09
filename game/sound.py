import os
import math
import wave
import struct
import pygame

class SoundManager:
    """Manages game audio and sound effects (jump, goal, death)."""

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sounds_dir = os.path.join(base_dir, "assets", "sounds")
        self.enabled = False
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._ensure_sound_files()
            self._load_sounds()
            self.enabled = True
        except Exception as e:
            # Fallback gracefully if system audio device is unavailable
            print(f"[Audio Notice] Sound disabled: {e}")
            self.enabled = False

    def _ensure_sound_files(self):
        os.makedirs(self.sounds_dir, exist_ok=True)
        jump_path = os.path.join(self.sounds_dir, "jump.wav")
        goal_path = os.path.join(self.sounds_dir, "goal.wav")
        death_path = os.path.join(self.sounds_dir, "death.wav")

        sample_rate = 44100

        # Jump sound: upward frequency sweep
        if not os.path.exists(jump_path):
            duration = 0.15
            n_samples = int(sample_rate * duration)
            with wave.open(jump_path, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                for i in range(n_samples):
                    t = i / sample_rate
                    freq = 260 + (620 - 260) * (t / duration)
                    sample = int(16000 * math.sin(2 * math.pi * freq * t) * (1 - t / duration))
                    f.writeframes(struct.pack("<h", sample))

        # Goal sound: uplifting 4-note chime
        if not os.path.exists(goal_path):
            notes = [523.25, 659.25, 783.99, 1046.50]
            note_dur = 0.08
            with wave.open(goal_path, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                for freq in notes:
                    n_note_samples = int(sample_rate * note_dur)
                    for i in range(n_note_samples):
                        t = i / sample_rate
                        env = math.sin(math.pi * (i / n_note_samples))
                        sample = int(18000 * math.sin(2 * math.pi * freq * t) * env)
                        f.writeframes(struct.pack("<h", sample))

        # Death sound: descending pitch sweep with decay
        if not os.path.exists(death_path):
            duration = 0.35
            n_samples = int(sample_rate * duration)
            with wave.open(death_path, "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                for i in range(n_samples):
                    t = i / sample_rate
                    freq = max(70, 380 - (380 - 70) * (t / duration))
                    decay = (1 - t / duration) ** 2
                    val = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)
                    sample = int(18000 * val * decay)
                    sample = max(-32767, min(32767, sample))
                    f.writeframes(struct.pack("<h", sample))

    def _load_sounds(self):
        self.sounds["jump"] = pygame.mixer.Sound(os.path.join(self.sounds_dir, "jump.wav"))
        self.sounds["goal"] = pygame.mixer.Sound(os.path.join(self.sounds_dir, "goal.wav"))
        self.sounds["death"] = pygame.mixer.Sound(os.path.join(self.sounds_dir, "death.wav"))

    def play_jump(self):
        if self.enabled and "jump" in self.sounds:
            self.sounds["jump"].play()

    def play_goal(self):
        if self.enabled and "goal" in self.sounds:
            self.sounds["goal"].play()

    def play_death(self):
        if self.enabled and "death" in self.sounds:
            self.sounds["death"].play()
