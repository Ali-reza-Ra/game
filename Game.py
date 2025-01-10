from curses import initscr, noecho, cbreak, nocbreak, echo, error, endwin
from random import random, randint
from time import sleep, time


class Game:
    """
    A simple terminal-based game where the player collects food while avoiding enemies.
    The player moves around using WASD keys, collecting $ symbols for points while
    avoiding E enemies and . obstacles.
    """
    def __init__(self):
        # Core game display variables
        self.screen = None        # Terminal screen object
        self.maxlines = 0         # Maximum number of lines in terminal
        self.maxcols = 0          # Maximum number of columns in terminal
        
        # Game state variables
        self.world = []           # 2D world grid
        self.food = []            # List of food items (position and age)
        self.enemy = []           # List of enemy positions
        self.playing = True       # Game running state
        self.player_l = 0         # Player line position
        self.player_c = 0         # Player column position
        self.score = 0            # Current game score
        self.frame_duration = 1 / 30  # Target frame duration for consistent game speed

    def setup_curses(self):
        """Initialize the curses library and set up the terminal display"""
        self.screen = initscr()
        noecho()                  # Don't show typed characters
        cbreak()                  # React to keys instantly without Enter
        self.screen.keypad(True)  # Enable special keys
        self.screen.nodelay(True) # Non-blocking input
        self.maxlines, self.maxcols = self.screen.getmaxyx()
        self.maxlines -= 1        # Adjust for zero-based indexing
        self.maxcols -= 1

    def cleanup_curses(self):
        """Restore terminal to its original state"""
        self.screen.keypad(False)
        nocbreak()
        echo()
        endwin()

    def random_place(self):
        """Find a random empty position in the world grid
        
        Returns:
            tuple: A pair of (line, column) coordinates
        """
        while True:
            a = randint(0, self.maxlines - 1)
            b = randint(0, self.maxcols - 1)
            if self.world[a][b] == ' ':
                return a, b

    def load_high_score(self):
        """Load the high score from file
        
        Returns:
            int: The highest score achieved, 0 if no score file exists
        """
        try:
            with open('score.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        """Save a new high score to file
        
        Args:
            score (int): The new high score to save
        """
        with open('score.txt', 'w')as file:
            file.write(str(score))

    def check_high_score(self, current_score):
        """Check if current score is a new high score and display appropriate message
        
        Args:
            current_score (int): The score to check
            
        Returns:
            int: The highest score (either the current or previous high score)
        """
        high_score = self.load_high_score()
        if current_score > high_score:
            self.save_high_score(current_score)
            self.screen.addstr(
                self.maxlines // 2, self.maxcols // 2 - 10, f'congratulations new record: {current_score}'
            )
            sleep(2)
            return current_score
        else:
            self.screen.addstr(self.maxlines // 2, self.maxcols // 2 - 10, f'high score: {high_score}')
            self.screen.addstr(self.maxlines // 2, self.maxcols // 2 - 10, f'current score: {current_score}')
            sleep(2)
            return high_score

    def init_world(self):
        """Initialize the game world with obstacles, food, and enemies"""
        # Create world grid with random obstacles
        for i in range(self.maxlines + 1):
            self.world.append([])
            for j in range(self.maxcols + 1):
                self.world[i].append(' ' if random() > 0.03 else '.')

        # Place food items with random ages
        for _ in range(10):
            foodlines, foodcols = self.random_place()
            foodage = randint(500, 1000)
            self.food.append((foodlines, foodcols, foodage))

        # Place enemies
        for _ in range(4):
            enemylines, enemycols = self.random_place()
            self.enemy.append((enemylines, enemycols))

    def draw(self):
        """Draw all game elements on the screen"""
        # Draw world grid (obstacles)
        for i in range(self.maxlines):
            for j in range(self.maxcols):
                self.screen.addch(i, j, self.world[i][j])

        # Display current score
        self.screen.addstr(1, 1, f'Score: {self.score}')

        # Draw food items ($)
        for f in self.food:
            foodlines, foodcols, foodage = f
            self.screen.addch(foodlines, foodcols, '$')

        # Draw enemies (E)
        for e in self.enemy:
            enemylines, enemycols = e
            self.screen.addch(enemylines, enemycols, 'E')

        # Draw player (P)
        self.screen.addch(self.player_l, self.player_c, 'P')
        self.screen.refresh()

    @staticmethod
    def in_range(num, minimum, maximum):
        """Ensure a number stays within a specified range
        
        Args:
            num (int): Number to check
            minimum (int): Minimum allowed value
            maximum (int): Maximum allowed value
            
        Returns:
            int: The number clamped to the allowed range
        """
        return min(max(num, minimum), maximum)

    def move_player(self, direction):
        """Handle player movement based on input direction
        
        Args:
            direction (str): One of 'w', 'a', 's', 'd' indicating direction
        """
        if direction == 'w' and self.world[self.player_l - 1][self.player_c] != '.':
            self.player_l -= 1
        elif direction == 's' and self.world[self.player_l + 1][self.player_c] != '.':
            self.player_l += 1
        elif direction == 'd' and self.world[self.player_l][self.player_c + 1] != '.':
            self.player_c += 1
        elif direction == 'a' and self.world[self.player_l][self.player_c - 1] != '.':
            self.player_c -= 1

        # Keep player within screen bounds
        self.player_l = self.in_range(self.player_l, 0, self.maxlines - 1)
        self.player_c = self.in_range(self.player_c, 0, self.maxcols - 1)

    def check_food(self):
        """Update food states and handle food collection"""
        for i in range(len(self.food)):
            foodlines, foodcols, foodage = self.food[i]
            foodage -= 1
            # Check if player collected food
            if self.player_l == foodlines and self.player_c == foodcols:
                self.score += 10
                foodlines, foodcols = self.random_place()
                foodage = randint(500, 1000)

            # Respawn food if it's too old
            if foodage <= 0:
                foodlines, foodcols = self.random_place()
                foodage = randint(250, 500)

            self.food[i] = (foodlines, foodcols, foodage)

    def move_enemy(self):
        """Update enemy positions and check for collisions with player"""
        for i in range(len(self.enemy)):
            enemyline, enemycols = self.enemy[i]
            # Enemies move toward player with 10% chance each frame
            if random() > 0.9:
                if enemyline > self.player_l:
                    enemyline -= 1
                if enemycols > self.player_c:
                    enemycols -= 1
                if enemyline < self.player_l:
                    enemyline += 1
                if enemycols < self.player_c:
                    enemycols += 1
            
            # Keep enemies within bounds
            enemyline = self.in_range(enemyline, 0, self.maxlines)
            enemycols = self.in_range(enemycols, 0, self.maxcols)
            self.enemy[i] = (enemyline, enemycols)
            
            # Check for collision with player
            if enemyline == self.player_l and enemycols == self.player_c:
                self.screen.addstr(self.maxlines // 2, self.maxcols // 2 - 3, 'you dead!')
                self.screen.refresh()
                self.check_high_score(self.score)
                self.screen.refresh()
                sleep(2)
                self.playing = False

    def run(self):
        """Main game loop"""
        try:
            self.setup_curses()
            self.init_world()
            while self.playing:
                start_time = time()

                # Handle input
                try:
                    c = self.screen.getkey()
                except (error, ValueError, TypeError):
                    c = ''
                if c in 'wasd':
                    self.move_player(c)
                elif c == 'q':
                    self.playing = False

                # Update game state
                self.draw()
                self.check_food()
                self.move_enemy()

                # Maintain consistent frame rate
                elapsed = time() - start_time
                if elapsed < self.frame_duration:
                    sleep(self.frame_duration - elapsed)

            # Show exit message
            self.screen.addstr(
                self.maxlines // 2,
                self.maxcols // 2 - 8,
                'thanks for playing ♥'
            )
            self.screen.refresh()
            sleep(2)
        finally:
            self.cleanup_curses()


if __name__ == "__main__":
    game = Game()
    game.run()