#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This module's docstring summary line.

This is a multi-line docstring. Paragraphs are separated with blank lines.
Lines conform to 79-column limit.

Module and packages names should be short, lower_case_with_underscores.
Notice that this in not PEP8-cheatsheet.py

Seriously, use flake8. Atom.io with https://atom.io/packages/linter-flake8
is awesome!
See http://www.python.org/dev/peps/pep-0008/ for more PEP-8 details




@todo: Create proper project structure
@todo: Check class syntax
@todo: Check class naming convention
@todo:  Create runner.py and import snake.py
@todo: Check proper ways of documentation / doxygen etc. 
@todo: Proper commenting




"""

from random import randrange # STD lib imports first
import curses # 3rd party stuff next



class Snake():
    """Write docstrings for ALL public classes, funcs and methods.

    Functions use snake_case.
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

    points = 0

    # def __init__(self):
    #     self.data = []

    def _init(self, num_rows, num_cols):

        # Create snake
        pos_x = int(num_cols / 2)
        pos_y = int(num_rows / 2)    

        self.snake = [[pos_x    , pos_y],
                      [pos_x + 1, pos_y],
                      [pos_x + 2, pos_y]]

        # Generate inital food
        self.food =  [randrange(1, num_cols - 1), 
                      randrange(1, num_rows - 1)] 

        self.direction = [ -1, 0 ]

        self.refresh_rate = 200

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
            self.snake.insert(0, tuple(map(sum, zip(self.snake[0], self.direction))) ) 

            # Create new food if food was eaten
            if self.snake[0][0] == self.food[0] and self.snake[0][1] == self.food[1]:
                # Add points
                self.points = self.points + 10

                # Generate new food
                self.food = []
                while self.food == []:
                    tmp_food = [randrange(1, num_cols - 1), 
                                randrange(1, num_rows - 1)] 

                    # Make sure that food is not generated within snake 
                    if tmp_food not in self.snake:
                        self.food = tmp_food
            else:
                self.snake.pop() # Remove last snake element if no food was eaten

            # Draw food
            curses_screen.addch(self.food[1], self.food[0], "♥" )

            # Draw snake
            for i, snake_element in enumerate(self.snake):
                # Defaut element
                ch = "o"        
                # Head element      
                if i == 0:
                    ch = "x"    
                curses_screen.addch(snake_element[1], snake_element[0], ch )

            # Check border contact
            border_contact = False
            if ( self.snake[0][0] in [0, num_cols - 1] ) or ( self.snake[0][1] in [0, num_rows - 1] ):
                border_contact = True

            # Check snake contact
            snake_contact = False
            if self.snake[0] in self.snake[1:]:
                snake_contact = True

            if border_contact or snake_contact:
                curses_screen.addstr(5,5, "You lost! Try again [Y/N]?")
                curses_screen.nodelay(False)

                c = curses_screen.getch()

                if c == ord("y"):    
                    # ReInitialize game
                    self._init(num_rows, num_cols)
                elif c == ord("n"):
                    # Quit game
                    run_game = False                
            else:        
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

            curses.napms( int(self.refresh_rate) )

            # Redraw
            curses_screen.refresh()

        # Terminate
        curses.nocbreak()
        curses_screen.keypad(0)
        curses_screen.echo()
        curses_screen.endwin()

    

    


# Start curses application
if __name__ == "__main__":
    s = Snake()

    s.run()
