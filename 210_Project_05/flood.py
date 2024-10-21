"""Flood-fill to count chambers in a cave.
CS 210 project.
<Your name here>, <date>
Credits: Chat GPT when it comes to the empty_space = 0, 
I originally had empty_space = [] and it should have been a counter not a list

"""
import doctest
import cave 
import config
import cave_view


def scan_cave(cavern: list[list[str]]) -> int:
    """Scan the cave for air pockets.  Return the number of
    air pockets encountered.

    >>> cavern_1 = cave.read_cave("data/tiny-cave.txt")
    >>> scan_cave(cavern_1)
    1
    >>> cavern_2 = cave.read_cave("data/cave.txt")
    >>> scan_cave(cavern_2)
    3
    """
    empty_space = 0
    for row_i in range(len(cavern)):
        for col_i in range(len(cavern[0])):
            if cavern[row_i][col_i] == config.AIR:
                #add to the counter of empty space
                empty_space += 1
                fill(cavern, row_i, col_i)
                cave_view.change_water()
    return empty_space


def fill(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
    #base case check if the rows and columns are inside the cave
    if row_i < 0 or row_i >= len(cavern) or col_i < 0 or col_i >= len(cavern[0]):
        return
    if cavern[row_i][col_i] == config.AIR:
        # if the cavern is air, configure it to have water
        cavern[row_i][col_i] = config.WATER
        cave_view.fill_cell(row_i, col_i)
        #recursively call fill
        fill(cavern, row_i, col_i - 1)
        fill(cavern, row_i, col_i + 1)
        fill(cavern, row_i - 1, col_i)
        fill(cavern, row_i + 1, col_i)
    else: 
        return




def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern,  config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.redisplay(cavern)
    cave_view.prompt_to_close()
    
if __name__ == "__main__":
    main()
