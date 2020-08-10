
import curses
from random import randrange


def snake():

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
   
    # Get screensize
    num_rows, num_cols = stdscr.getmaxyx()

    # Snake
    pos_x = int(num_cols / 2)
    pos_y = int(num_rows / 2)    
    snake = [[pos_x    , pos_y],
             [pos_x + 1, pos_y],
             [pos_x + 2, pos_y]]

    # Generate inital food
    food =  [randrange(1, num_cols - 1), 
             randrange(1, num_rows - 1)] 

    # Direction
    # Right = [  1,  0 ]
    # Left  = [ -1,  0 ]
    # Down  = [  0,  1 ]
    # Up    = [ -1, -1 ]    
    # Diagonal will not be supported
    direction = [ -1, 0 ]
   
    speed = 200
    run_game = True
    points = 0

    while run_game:
        # Do not wait for any key when get user input
        stdscr.nodelay(True)

        # Prepare screen
        stdscr.clear()
        stdscr.box()
        stdscr.addstr(2, 2 , "Points: " + str(points))

        # Move snake in current direction
        snake.insert(0, tuple(map(sum, zip(snake[0], direction))) ) 

        # Create new food if food was eaten
        if snake[0][0] == food[0] and snake[0][1] == food[1]:
            # Add points
            points = points + 10

            # Generate new food
            food = []
            while food == []:
                tmp_food = [randrange(1, num_cols - 1), 
                            randrange(1, num_rows - 1)] 

                # Make sure that food is not generated within snake 
                if tmp_food not in snake:
                    food = tmp_food
        else:
            snake.pop() # Remove last snake element if no food was eaten

        # Draw food
        stdscr.addch(food[1], food[0], "♥" )

        # Draw snake
        for i, snake_element in enumerate(snake):
            # Defaut element
            ch = "o"        
            # Head element      
            if i == 0:
                ch = "x"    
            stdscr.addch(snake_element[1], snake_element[0], ch )

        # Check border contact
        border_contact = False
        if ( snake[0][0] in [0, num_cols - 1] ) or ( snake[0][1] in [0, num_rows - 1] ):
            border_contact = True

        # Check snake contact
        snake_contact = False
        if snake[0] in snake[1:]:
            snake_contact = True

        if border_contact or snake_contact:
            stdscr.addstr(5,5, "You lost! Try again [Y]?")
            stdscr.nodelay(False)

            c = stdscr.getch()

            if c == ord("y"):    
                # Reset game
                snake = [[pos_x    , pos_y],
                        [pos_x + 1, pos_y],
                        [pos_x + 2, pos_y]]
                direction = [ -1, 0 ]
            else:
                 # Quit game
                run_game = False                
        else:        
            c = stdscr.getch()

            if c == curses.KEY_UP or c == ord("w"):
                if direction[1] == 0:
                    direction = [0, -1]
            elif c == curses.KEY_DOWN or c == ord("s"):
                if direction[1] == 0:
                    direction = [0, 1]
            elif c == curses.KEY_LEFT or c == ord("a"):
                if direction[0] == 0:
                    direction = [-1, 0]
            elif c == curses.KEY_RIGHT or c == ord("d"):
                if direction[0] == 0:
                    direction = [1, 0]

        curses.napms( int(speed) )

        # Redraw
        stdscr.refresh()

    # Terminate
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


# Start curses application
if __name__ == "__main__":
    snake()
