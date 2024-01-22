import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(100, 100)
        pyxel.mouse(True)
        self.reset_game()
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.maze = Maze(10, 10)
        self.player = Player(45, 45)
        self.goal_x, self.goal_y = 80, 80
        self.maze.clear_path_to_goal(self.goal_x, self.goal_y)
        self.game_clear = False

    def setup_sound(self):
        pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
        pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30)

    def update(self):
        if self.game_clear:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                if 35 <= mx <= 65 and 60 <= my <= 70:  
                    self.reset_game()
        else:
            self.player.move(self.maze)
            self.check_goal()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.maze.click(pyxel.mouse_x, pyxel.mouse_y)

    def draw(self):
        if self.game_clear:
            pyxel.cls(0)
            pyxel.text(30, 50, "Game Clear!", 7)
            pyxel.rect(35, 60, 30, 10, 7)  
            pyxel.text(40, 62, "Retry", 0)
        else:
            pyxel.cls(4)
            self.maze.draw()
            self.player.draw()
            pyxel.rect(self.goal_x, self.goal_y, 5, 5, 11)

    def check_goal(self):
        if self.player.x in range(self.goal_x, self.goal_x + 6) and self.player.y in range(self.goal_y, self.goal_y + 6):
            self.game_clear = True

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 7
        self.h = 7
        pyxel.image(0).set(0, 0, ["777A777","77AAA77","7AAAAA7","AAAAAAA","7AAAAA7","77AAA77","777A777"])

    def draw(self):
        pyxel.blt(self.x - 3, self.y - 3, 0, 0, 0, 7, 7, 7)

    def move(self, maze):
        new_x, new_y = self.x, self.y
        if pyxel.btn(pyxel.KEY_RIGHT):
            new_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            new_x -= 1
        elif pyxel.btn(pyxel.KEY_UP):
            new_y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            new_y += 1

        new_x = max(0, min(new_x, pyxel.width - self.w))
        new_y = max(0, min(new_y, pyxel.height - self.h))

        if not maze.is_wall(new_x, new_y):
            if new_x != self.x or new_y != self.y:  
                pyxel.play(0, 0)  
            self.x, self.y = new_x, new_y

class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.maze = self.generate_maze()

    def generate_maze(self):
        return [[random.randint(0, 1) for _ in range(self.width)] for _ in range(self.height)]

    def click(self, x, y):
        maze_x, maze_y = x // 10, y // 10
        if 0 <= maze_x < self.width and 0 <= maze_y < self.height:
            if self.maze[maze_y][maze_x] == 1: 
                self.maze[maze_y][maze_x] = 0
                pyxel.play(0, 1)  

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 1:
                    pyxel.rect(x * 10, y * 10, 10, 10, 0)

    def is_wall(self, x, y):
        maze_x, maze_y = x // 10, y // 10
        if 0 <= maze_x < self.width and 0 <= maze_y < self.height:
            return self.maze[maze_y][maze_x] == 1
        return False

    def clear_path_to_goal(self, goal_x, goal_y):
        for x in range(goal_x - 10, goal_x + 15, 10):
            for y in range(goal_y - 10, goal_y + 15, 10):
                self.maze[y // 10][x // 10] = 0

App()
