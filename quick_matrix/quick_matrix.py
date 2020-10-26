import curses
import traceback
import clipboard

'''
By Torin Kovach
Run in the Terminal -- allows you to easily make a LaTeX matrix
'''


def get_number(stdscr):
    cool_num = ""
    length = 0
    while True:
        ch = stdscr.getch()
        if str(ch) == "127":
            if length > 0:
                length -= 1
                cool_num = cool_num[1:]
                stdscr.addstr("\b \b")
        elif str(ch) == "10":
            if length > 0:
                return int(cool_num)
        else:
            s = str(chr(int(str(ch))))
            if s.isdigit():
                cool_num += s
                stdscr.addstr(s)
                length += 1


def move_newpos(stdscr, tr_x, tr_y, space, rows, cols, lengths, posx, posy):
    if posy >= rows or posx >= cols or posy < 0 or posx < 0:
        return
    else:
        x_pos = tr_x + posy
        y_pos = tr_y + posx * (space + 1) + lengths[posx][posy] - 1
        stdscr.move(x_pos, y_pos + 1)


def modify_matrix(stdscr, tr_x, tr_y, space, rows, cols):
    stdscr.keypad(True)
    lengths = [[1 for i in range(rows)] for j in range(cols)]
    values = [["0" for i in range(cols)] for j in range(rows)]
    pos = [0, 0]
    stdscr.move(tr_x, tr_y + 1)
    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_UP:
            if pos[1] != 0:
                pos[1] -= 1
                move_newpos(stdscr, tr_x, tr_y,
                            space, rows, cols,
                            lengths, pos[0], pos[1])
        elif ch == curses.KEY_DOWN:
            if pos[1] != rows - 1:
                pos[1] += 1
                move_newpos(stdscr, tr_x, tr_y,
                            space, rows, cols,
                            lengths, pos[0], pos[1])
        elif ch == curses.KEY_RIGHT:
            if pos[0] != cols - 1:
                pos[0] += 1
                move_newpos(stdscr, tr_x, tr_y,
                            space, rows, cols,
                            lengths, pos[0], pos[1])
        elif ch == curses.KEY_LEFT:
            if pos[0] != 0:
                pos[0] -= 1
                move_newpos(stdscr, tr_x, tr_y,
                            space, rows, cols,
                            lengths, pos[0], pos[1])
        else:
            try:
                if str(ch) == "127":
                    if(lengths[pos[0]][pos[1]] > 0):
                        stdscr.addstr("\b \b")
                        lengths[pos[0]][pos[1]] -= 1
                        values[pos[1]][pos[0]] = values[pos[1]][pos[0]][:-1]
                elif str(ch) == "10":
                    curses.ungetch(curses.KEY_DOWN)
                elif str(ch) == "9":
                    return values
                else:
                    s = str(chr(int(str(ch))))[0]
                    lengths[pos[0]][pos[1]] += 1
                    values[pos[1]][pos[0]] += s
                    stdscr.addstr(s)
            except Exception as _:
                return


try:
    # -- Initialize --
    stdscr = curses.initscr()
    curses.noecho()
    # stdscr.keypad(True)
    # -- Perform an action with Screen --
    stdscr.border(0)
    stdscr.addstr(0, 0, 'Latex Matrix Builder', curses.A_BOLD)

    # GET ROWS
    stdscr.addstr(1, 1, 'Enter number of rows: ', curses.A_NORMAL)
    rows = get_number(stdscr)
    stdscr.addstr(2, 1,
                  'You have entered ' + str(rows) + ' rows.',
                  curses.A_NORMAL)

    # GET COLS
    stdscr.addstr(3, 1, 'Enter number of cols: ', curses.A_NORMAL)
    cols = get_number(stdscr)
    stdscr.addstr(4, 1,
                  'You have entered ' + str(rows) + ' cols.',
                  curses.A_NORMAL)
    space = 10
    row_template = (" " * space).join(["0" for i in range(cols)])

    diff = 6

    for line_num in range(diff, rows + diff):
        stdscr.addstr(line_num, 3, row_template, curses.A_NORMAL)

    matrix = modify_matrix(stdscr, diff, 3, space, rows, cols)
    return_str = "\\begin{pmatrix}" + \
        "\\\\".join(["&".join(i) for i in matrix]) + "\\end{pmatrix}"
    stdscr.addstr(diff + rows + 3, 1, "Latex output:", curses.A_NORMAL)
    stdscr.addstr(diff + rows + 4, 1, return_str, curses.A_NORMAL)
    clipboard.copy(return_str)
    stdscr.addstr(diff + rows + 6, 1,
                  "Output has been copied to clipboard. Press 'q' to exit.",
                  curses.A_NORMAL)

    while True:
        # stay in this loop till the user presses 'q'
        ch = stdscr.getch()
        if ch == ord('q'):
            break

    # -- End of user code --

except Exception as _:
    traceback.print_exc()     # print trace back log of the error

finally:
    # --- Cleanup on exit ---
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
