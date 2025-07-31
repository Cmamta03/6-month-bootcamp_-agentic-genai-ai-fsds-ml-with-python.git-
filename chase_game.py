import streamlit as st
import random
import time
import json
from datetime import datetime

class ChaseGame:
    def __init__(self):
        self.grid_size = 20
        self.player_pos = [10, 10]
        self.enemies = []
        self.collectibles = []
        self.score = 0
        self.game_over = False
        self.level = 1
        self.max_enemies = 3
        self.enemy_speed = 1
        
    def initialize_game(self):
        """Initialize the game state"""
        self.player_pos = [10, 10]
        self.enemies = []
        self.collectibles = []
        self.score = 0
        self.game_over = False
        self.level = 1
        self.max_enemies = 3
        self.enemy_speed = 1
        self.spawn_enemies()
        self.spawn_collectibles()
    
    def spawn_enemies(self):
        """Spawn enemies at random positions"""
        self.enemies = []
        for _ in range(self.max_enemies):
            while True:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                # Make sure enemy doesn't spawn on player
                if [x, y] != self.player_pos:
                    self.enemies.append([x, y])
                    break
    
    def spawn_collectibles(self):
        """Spawn collectible items"""
        self.collectibles = []
        num_collectibles = 3
        for _ in range(num_collectibles):
            while True:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                # Make sure collectible doesn't spawn on player or enemies
                if [x, y] != self.player_pos and [x, y] not in self.enemies:
                    self.collectibles.append([x, y])
                    break
    
    def move_player(self, direction):
        """Move the player based on direction"""
        if self.game_over:
            return
            
        new_pos = self.player_pos.copy()
        
        if direction == "up" and new_pos[1] > 0:
            new_pos[1] -= 1
        elif direction == "down" and new_pos[1] < self.grid_size - 1:
            new_pos[1] += 1
        elif direction == "left" and new_pos[0] > 0:
            new_pos[0] -= 1
        elif direction == "right" and new_pos[0] < self.grid_size - 1:
            new_pos[0] += 1
        
        # Check if new position is valid (not occupied by enemy)
        if new_pos not in self.enemies:
            self.player_pos = new_pos
            self.check_collisions()
    
    def move_enemies(self):
        """Move enemies towards player with simple AI"""
        if self.game_over:
            return
            
        for i, enemy in enumerate(self.enemies):
            # Simple AI: move towards player
            dx = self.player_pos[0] - enemy[0]
            dy = self.player_pos[1] - enemy[1]
            
            new_x = enemy[0]
            new_y = enemy[1]
            
            # Move horizontally if there's a significant difference
            if abs(dx) > abs(dy):
                if dx > 0 and enemy[0] < self.grid_size - 1:
                    new_x = enemy[0] + 1
                elif dx < 0 and enemy[0] > 0:
                    new_x = enemy[0] - 1
            else:
                if dy > 0 and enemy[1] < self.grid_size - 1:
                    new_y = enemy[1] + 1
                elif dy < 0 and enemy[1] > 0:
                    new_y = enemy[1] - 1
            
            # Update enemy position
            self.enemies[i] = [new_x, new_y]
    
    def check_collisions(self):
        """Check for collisions with enemies and collectibles"""
        # Check collision with enemies
        if self.player_pos in self.enemies:
            self.game_over = True
            return
        
        # Check collision with collectibles
        if self.player_pos in self.collectibles:
            self.score += 10
            self.collectibles.remove(self.player_pos)
            
            # Level up if all collectibles are collected
            if not self.collectibles:
                self.level_up()
    
    def level_up(self):
        """Increase level and difficulty"""
        self.level += 1
        self.max_enemies = min(self.max_enemies + 1, 8)
        self.enemy_speed = min(self.enemy_speed + 0.2, 2.0)
        self.spawn_enemies()
        self.spawn_collectibles()
    
    def get_grid_display(self):
        """Create a visual representation of the game grid"""
        grid = [['⬜' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Place player
        grid[self.player_pos[1]][self.player_pos[0]] = '🟦'
        
        # Place enemies
        for enemy in self.enemies:
            grid[enemy[1]][enemy[0]] = '🟥'
        
        # Place collectibles
        for collectible in self.collectibles:
            grid[collectible[1]][collectible[0]] = '⭐'
        
        return grid

def save_high_score(score):
    """Save high score to session state"""
    if 'high_score' not in st.session_state:
        st.session_state.high_score = 0
    
    if score > st.session_state.high_score:
        st.session_state.high_score = score
        return True
    return False

def main():
    st.set_page_config(
        page_title="Chase Game",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 Chase Game")
    st.markdown("---")
    
    # Initialize game in session state
    if 'game' not in st.session_state:
        st.session_state.game = ChaseGame()
        st.session_state.game.initialize_game()
    
    game = st.session_state.game
    
    # Game controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.subheader("🎮 Controls")
        st.write("Use the buttons below to move:")
        
        # Movement buttons
        if st.button("⬆️ Up", key="up"):
            game.move_player("up")
        
        col_up = st.columns(3)
        with col_up[0]:
            if st.button("⬅️ Left", key="left"):
                game.move_player("left")
        with col_up[1]:
            st.write("")
        with col_up[2]:
            if st.button("➡️ Right", key="right"):
                game.move_player("right")
        
        if st.button("⬇️ Down", key="down"):
            game.move_player("down")
        
        st.markdown("---")
        
        # Game actions
        if st.button("🔄 New Game", key="new_game"):
            game.initialize_game()
            st.rerun()
        
        if st.button("⏸️ Pause/Resume", key="pause"):
            if 'paused' not in st.session_state:
                st.session_state.paused = False
            st.session_state.paused = not st.session_state.paused
    
    with col2:
        st.subheader("🎯 Game Board")
        
        # Display game grid
        grid = game.get_grid_display()
        
        # Create a visual grid
        grid_display = ""
        for row in grid:
            grid_display += " ".join(row) + "\n"
        
        # Use a monospace font container
        st.code(grid_display, language=None)
        
        # Game status
        if game.game_over:
            st.error("💀 Game Over!")
            if save_high_score(game.score):
                st.success("🏆 New High Score!")
        else:
            st.success("🎮 Game Running")
    
    with col3:
        st.subheader("📊 Game Stats")
        
        # Score and level
        st.metric("Score", game.score)
        st.metric("Level", game.level)
        st.metric("High Score", st.session_state.get('high_score', 0))
        
        # Game info
        st.markdown("---")
        st.write("**Game Info:**")
        st.write(f"• Enemies: {len(game.enemies)}")
        st.write(f"• Collectibles: {len(game.collectibles)}")
        st.write(f"• Enemy Speed: {game.enemy_speed:.1f}")
        
        # Instructions
        st.markdown("---")
        st.write("**How to Play:**")
        st.write("• 🟦 You (Blue)")
        st.write("• 🟥 Enemies (Red)")
        st.write("• ⭐ Collectibles (Stars)")
        st.write("• Avoid enemies, collect stars!")
        st.write("• Complete level to advance!")
    
    # Auto-move enemies
    if not game.game_over and not st.session_state.get('paused', False):
        game.move_enemies()
        game.check_collisions()
    
    # Game over handling
    if game.game_over:
        st.markdown("---")
        st.subheader("🏁 Game Over!")
        st.write(f"Final Score: {game.score}")
        st.write(f"Level Reached: {game.level}")
        
        if st.button("🔄 Play Again"):
            game.initialize_game()
            st.rerun()
    
    # Auto-refresh for real-time gameplay
    if not game.game_over and not st.session_state.get('paused', False):
        time.sleep(0.5)
        st.rerun()

if __name__ == "__main__":
    main() 