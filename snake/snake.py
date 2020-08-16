#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""The old  game classic "Snake" in Python

Open issues:
@todo: Check class syntax
@todo: Check class naming convention
@todo: Add proper commenting
@todo: Requirements.txt test on linux (e.g. create install.py?)
"""

from random import randrange # STD lib imports first
import curses # 3rd party stuff next

# Constants
REFRESH_RATE_DEFAULT = 200


class Snake():
    """The old  game classic "Snake" in Python

    This is a very simple Python implementation of the game "Snake" 
    using the curses UI framework. 
    """

    # Snake elements
    snake = []

    # Food
    food = []

    # Direction
    # Right = [  1,  0 ]
    # Left  = [ -1,  0 ]
    # Down  = [  0,  1 ]
    # Up    = [ -1, -1 ]    
    # Diagonal will not be supported
    direction = [ -1, 0 ]

    # Refresh rate
    refresh_rate = 0

    # Points
    points = 0

    def _init(self, num_rows, num_cols):

        # Inital snake position 
        pos_x = int(num_cols / 2)
        pos_y = int(num_rows / 2)    

        # Generate snake
        self.snake = [[pos_x    , pos_y],
                      [pos_x + 1, pos_y],
                      [pos_x + 2, pos_y]]

        # Generate food
        self.food = self._generate_food(num_cols, num_rows)    

        self.direction = [ -1, 0 ]
        
        self.refresh_rate = REFRESH_RATE_DEFAULT
        
        self.points = 0

    def _setup_curses(self):
        
        # Initialize curses
        stdscr = curses.initscr()

        # Clear screen
        stdscr.clear()

        # Disable echoing
        curses.noecho()

        # Accept keys without <Enter>
        curses.cbreak()

        # Expect special keys (e.g. KEY_LEFT)
        stdscr.keypad(True)

        # Enable colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        # Window and background coloring
        stdscr.bkgd(curses.color_pair(1))
        stdscr.box()
        stdscr.refresh()

        # Disable cursor
        curses.curs_set(0)

        return stdscr


    def _generate_food(self, num_cols, num_rows):
        return  [randrange(1, num_cols - 1), 
                 randrange(1, num_rows - 1)] 

    def run(self):
        # Setup curses
        curses_screen = self._setup_curses()

        # Get screensize
        num_rows, num_cols = curses_screen.getmaxyx()

        # Initialize game
        self._init(num_rows, num_cols)

        # Game loop
        run_game = True
        while run_game:
            # Do not wait for any key when get user input
            curses_screen.nodelay(True)

            # Prepare screen
            curses_screen.clear()
            curses_screen.box()
            curses_screen.addstr(2, 2 , "Points: " + str(self.points))

            # Move snake in current direction
            self.snake.insert(0, list(map(sum, zip(self.snake[0], self.direction))) ) 

            # Create new food if food was eaten
            if self.snake[0] == self.food:
                # Add points
                self.points += 10

                # Generate new food
                self.food = []
                while self.food == []:
                    tmp_food = self._generate_food(num_cols, num_rows)  

                    # Make sure that food is not generated within snake 
                    if tmp_food not in self.snake:
                        self.food = tmp_food
            else:
                self.snake.pop() # Remove last snake element if no food was eaten

            # Draw food
            curses_screen.addch(self.food[1], self.food[0], "♥" )

            # Draw snake
            for i, snake_element in enumerate(self.snake):
                curses_screen.addch(snake_element[1], snake_element[0], "o" if i != 0 else "x" )

            # Check border contact
            border_contact = False
            if ( self.snake[0][0] in [0, num_cols - 1] ) or ( self.snake[0][1] in [0, num_rows - 1] ):
                border_contact = True

            # Check snake contact
            snake_contact = False
            if self.snake[0] in self.snake[1:]:
                snake_contact = True

            # Check if game is over
            if border_contact or snake_contact:
                curses_screen.addstr(5,5, "You lost! Try again [Y/*]?")
                curses_screen.nodelay(False)

                c = curses_screen.getch()

                if c == ord("y"):    
                    # ReInitialize game
                    self._init(num_rows, num_cols)
                else:
                    # Quit game
                    run_game = False                
            else:    
                # Get user input    
                c = curses_screen.getch()

                if c == curses.KEY_UP or c == ord("w"):
                    if self.direction[1] == 0:
                        self.direction = [0, -1]
                elif c == curses.KEY_DOWN or c == ord("s"):
                    if self.direction[1] == 0:
                        self.direction = [0, 1]
                elif c == curses.KEY_LEFT or c == ord("a"):
                    if self.direction[0] == 0:
                        self.direction = [-1, 0]
                elif c == curses.KEY_RIGHT or c == ord("d"):
                    if self.direction[0] == 0:
                        self.direction = [1, 0]
                elif c == ord("p"):
                    # Quit game
                    run_game = False     

            # Control update rate
            curses.napms( int(self.refresh_rate) )

            # Redraw
            curses_screen.refresh()

        # Terminate curses application
        curses.nocbreak()
        curses_screen.keypad(0)
        curses.echo()
        curses.endwin()
