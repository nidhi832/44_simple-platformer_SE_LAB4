import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard

# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gravity = 0.6

        self.start_x, self.start_y = 40, height - 120
        self.player = Player(self.start_x, self.start_y)

        # A simple hand-built level: platforms with gaps between them
        # (falling into a gap means falling off the bottom of the
        # screen), one hazard, and a goal near the right edge.
        ground_y = height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(240, ground_y - 14, 100)]
        self.goal_x = 740

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 54, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 32)
        self.prompt_font = pygame.font.SysFont("Arial", 22)
        self.game_over = False

    def reset_game(self):
        self.player.x, self.player.y = self.start_x, self.start_y
        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False
        self.score = 0
        self.game_over = False
        self._game_over_logged = False

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r):
                self.reset_game()
            return

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            self.player.jump()

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.game_over:
            return

        self.terminal_velocity = 16.0
        self.player.vy = min(self.player.vy + self.gravity, self.terminal_velocity)
        self.player.x = max(0, self.player.x + self.player.vx)

        # Swept vertical collision detection:
        # Check if the player's vertical trajectory crosses any platform top surface
        # during this frame, preventing tunneling at high fall speeds.
        prev_bottom = self.player.y + self.player.height
        new_y = self.player.y + self.player.vy
        new_bottom = new_y + self.player.height

        self.player.on_ground = False
        if self.player.vy >= 0:
            best_platform = None
            for platform in self.platforms:
                # Check horizontal overlap with platform
                if self.player.x + self.player.width > platform.x and self.player.x < platform.x + platform.width:
                    # Did the player cross or land onto the platform top surface?
                    if prev_bottom <= platform.y + 4 and new_bottom >= platform.y:
                        if best_platform is None or platform.y < best_platform.y:
                            best_platform = platform

            if best_platform:
                self.player.y = best_platform.y - self.player.height
                self.player.vy = 0
                self.player.on_ground = True
            else:
                self.player.y = new_y
        else:
            self.player.y = new_y

        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self.game_over = True
                return

        if self.player.y > self.height:
            self.game_over = True
            return

        if self.player.x >= self.goal_x:
            self.score += 1
            self.player.x, self.player.y = self.start_x, self.start_y
            self.player.vy = 0

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            if not getattr(self, "_game_over_logged", False):
                print("Game over! Final score:", self.score)
                self._game_over_logged = True

            # Dark translucent overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            # Game Over Title
            title_surf = self.title_font.render("GAME OVER", True, RED)
            title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 60))
            screen.blit(title_surf, title_rect)

            # Final Score
            score_surf = self.subtitle_font.render(f"Final Score: {self.score}", True, GOLD)
            score_rect = score_surf.get_rect(center=(self.width // 2, self.height // 2 + 5))
            screen.blit(score_surf, score_rect)

            # User input prompt
            prompt_surf = self.prompt_font.render("Press SPACE or ENTER to Continue", True, GRAY)
            prompt_rect = prompt_surf.get_rect(center=(self.width // 2, self.height // 2 + 65))
            screen.blit(prompt_surf, prompt_rect)
