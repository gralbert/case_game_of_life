from tkinter import *
from classes import Cell

root = Tk()
root.title('Game of Life')
root.geometry('500x500')


def play_help():
    """ Help def play() to stop. """
    global stop
    stop = False
    play()


def play():
    """ Starting the game. """
    global stop
    if not stop:
        one_step()
        root.after(400, play)


def stopping():
    """ Stop the game. """
    global stop
    stop = True


def one_step():
    """ Make one step of the game. """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].neighbours = 0
            for i_ in range(i-1, i+2):
                for j_ in range(j-1, j+2):
                    try:
                        if grid[i_][j_].get_status() \
                                and (i_ != i or j_ != j):
                            grid[i][j].add_neighbour()
                    except IndexError:
                        pass
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            if grid[i][j].get_neighbours() == 3 \
                    and not grid[i][j].get_status():
                grid[i][j].change_color()

            elif (grid[i][j].get_neighbours() < 2
                  or grid[i][j].get_neighbours() > 3) \
                    and grid[i][j].get_status():
                grid[i][j].change_color()


def clear():
    """ Clear game grid. """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].clear()


def remake(sizex, sizey):
    """ Make grid with new sizes. """
    global root
    root.geometry('{}x{}'.format(sizex*20,sizey*20 + 20))
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].destroy()
    grid = create_grid(sizex, sizey)
    create_menu()
    global stop
    stop = False


def ten():
    """ Make grid 10x10. """
    remake(10,10)


def fifteen():
    """ Make grid 15x15. """
    remake(15, 15)


def twenty():
    """ Make grid 25x25. """
    remake(25, 25)


def exit_game():
    """ Exit from the game. """
    root.destroy()


def save():
    """ Save position of the cells to the file. """
    with open('my_game.txt', 'w') as f:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j].get_status():
                    f.write('1')
                else:
                    f.write('0')
            f.write('\n')


def upload():
    """ Open position of the cells from the file. """
    with open('my_game.txt', 'r') as f:
        tr = 0
        td = 0
        for i in f:
            for j in i.strip():
                try:
                    if j == '1' and not grid[tr][td].get_status():
                        grid[tr][td].change_color()
                    elif j == '0' and grid[tr][td].get_status():
                        grid[tr][td].change_color()
                except IndexError:
                    pass
                if j == '0' or j == '1':
                    td += 1
            tr += 1
            td = 0


def create_grid(sizex, sizey):
    """ Make new grid at first. """
    y = -20

    grid = [[] * sizex for i in range(sizey)]
    for i in range(int(sizex)):
        x = -20
        y += 20
        for j in range(int(sizey)):
            x += 20
            grid[i].append(Cell())
            grid[i][j].place(x=x, y=y)

    return grid


def create_menu():
    """ Make menu of the programm. """
    main_menu = Menu(root)
    root.configure(menu=main_menu)
    file = Menu(main_menu, tearoff=0)
    run = Menu(main_menu, tearoff=0)
    size = Menu(main_menu, tearoff=0)

    file.add_cascade(label='Import', command=upload)
    file.add_cascade(label='Export', command=save)
    file.add_cascade(label='Exit', command=exit_game)

    run.add_cascade(label='Run', command=play_help)
    run.add_cascade(label='Stop', command=stopping)
    run.add_cascade(label='One step', command=one_step)
    run.add_cascade(label='Clear', command=clear)

    size.add_cascade(label='10 x 10', command=ten)
    size.add_cascade(label='15 x 15', command=fifteen)
    size.add_cascade(label='25 x 25', command=twenty)

    main_menu.add_cascade(label='File', menu=file)
    main_menu.add_cascade(label='Run', menu=run)
    main_menu.add_cascade(label='Size', menu=size)


if __name__ == '__main__':
    create_menu()
    stop = False
    grid = create_grid(25, 25)
    root.mainloop()
