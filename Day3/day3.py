"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

def part1():
    def is_a_symbol(character):
        if not character.isdigit() and character != ".":
            return True

    def check_left(start_boundry, lines):
        if start_boundry == 0:
            return False
        else:
            for line in lines:
                if line and is_a_symbol(line[start_boundry - 1]):
                    return True
        return False


    def check_right(end_boundry, lines, max_length):
        if end_boundry == max_length - 1:
            return False
        else:
            for line in lines:
                if line and is_a_symbol(line[end_boundry + 1]):
                    return True
        return False

    def check_up_and_down(start_boundry, end_boundry, previous_and_next_line):
        for line in previous_and_next_line:
            if line:
                if [item for item in line[start_boundry:end_boundry + 1] if is_a_symbol(item)]:
                    return True
        return False

    with open('input.txt', 'r') as my_input:
        all_lines = my_input.readlines()
        sum_of_parts = 0

        for line_number in range(0, len(all_lines)):
            current_line = all_lines[line_number].strip()
            previous_line = all_lines[line_number - 1].strip() if line_number > 0 else None
            next_line = all_lines[line_number + 1].strip() if line_number < len(all_lines) - 1 else None
            lines_to_check = [current_line, previous_line, next_line]
            start_boundry = None
            end_boundry = None
            for i in range(0, len(current_line)):
                if current_line[i].isdigit() and start_boundry == None:
                    start_boundry = i
                elif current_line[i].isdigit():
                    if i == len(current_line) - 1:
                        end_boundry = i
                else:
                    if start_boundry != None:
                        end_boundry = i - 1
                if start_boundry != None and end_boundry != None:
                    if check_left(start_boundry, lines_to_check):
                        sum_of_parts += int(current_line[start_boundry:end_boundry + 1])
                        start_boundry = None
                        end_boundry = None
                        continue
                    if check_right(end_boundry, lines_to_check, max([len(line) for line in lines_to_check if line])):
                        sum_of_parts += int(current_line[start_boundry:end_boundry + 1])
                        start_boundry = None
                        end_boundry = None
                        continue
                    if check_up_and_down(start_boundry, end_boundry, [previous_line, next_line]):
                        sum_of_parts += int(current_line[start_boundry:end_boundry + 1])
                        start_boundry = None
                        end_boundry = None
                        continue

                    start_boundry = None
                    end_boundry = None
    return sum_of_parts


"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help",
so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window.
There stands the engineer, holding a phone in one hand and waving with the other.
You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong.
A gear is any * symbol that is adjacent to exactly two part numbers.
Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345.
The second gear is in the lower right; its gear ratio is 451490.
(The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Answer:

Although it hasn't changed, you can still get your puzzle input.

You can also [Shareon Twitter Mastodon] this puzzle.
"""

def get_left_number(current_line, start_index):
    number = ''
    if start_index == 0:
        return None
    elif not current_line[start_index - 1].isdigit():
        return None
    else:
        iterator_index = start_index
        while True:
            if current_line[iterator_index - 1].isdigit():
                iterator_index = iterator_index - 1
                if iterator_index == 0:
                    break
            else:
                break
        while True:
            if current_line[iterator_index].isdigit():
                number = number + current_line[iterator_index]
                iterator_index += 1
            else:
                break

    return number

def get_right_number(current_line, start_index):
    number = ''
    if start_index == len(current_line) - 1:
        return None
    elif not current_line[start_index + 1].isdigit():
        return None
    else:
        while True:
            if current_line[start_index + 1].isdigit():
                number = number + current_line[start_index + 1]
                start_index = start_index + 1
                if start_index == len(current_line) - 1:
                    break
            else:
                break
    
    return number

def get_vertical_numbers(line_to_check, start_index):
    if not line_to_check:
        return None, None
    else:
        line_to_check[start_index]
        if not line_to_check[start_index].isdigit():
            left_number = get_left_number(line_to_check, start_index)
            right_number = get_right_number(line_to_check, start_index)
            return (left_number, right_number)
        else:
            if start_index == 0 or not line_to_check[start_index - 1].isdigit():
                left_number = None
                right_number = get_right_number(line_to_check, start_index - 1)
                return (left_number, right_number)
            if start_index == len(line_to_check) - 1 or not line_to_check[start_index + 1].isdigit():
                left_number = get_left_number(line_to_check, start_index + 1)
                right_number = None
                return (left_number, right_number)
            else:
                while True:
                    if line_to_check[start_index - 1].isdigit():
                        start_index -= 1
                    else:
                        break

                    left_number = get_left_number(line_to_check, start_index + 1)
                    right_number = None
                    return (left_number, right_number)
                    

def part2():    
    with open('input.txt', 'r') as my_input:
        all_lines = my_input.readlines()
        gear_ratio_sum = 0

        for line_number in range(0, len(all_lines)):
            current_line = all_lines[line_number].strip()
            previous_line = all_lines[line_number - 1].strip() if line_number > 0 else None
            next_line = all_lines[line_number + 1].strip() if line_number < len(all_lines) - 1 else None
            lines_to_check = [current_line, previous_line, next_line]
            for i in range(0, len(current_line)):
                if current_line[i] == '*':
                    left_number = get_left_number(current_line, i)
                    right_number = get_right_number(current_line, i)
                    left_above, right_above = get_vertical_numbers(previous_line, i)
                    left_below, right_below = get_vertical_numbers(next_line, i)

                    all_numbers = [left_number, right_number, left_above, left_below, right_above, right_below]

                    stripped_all_numbers = [number for number in all_numbers if number != None]

                    if len(stripped_all_numbers) == 2:
                        gear_ratio_sum += (int(stripped_all_numbers[0]) * int(stripped_all_numbers[1]))


    return gear_ratio_sum


if __name__ == "__main__":
    print(part1())
    print(part2())






