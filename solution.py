assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def find_units(x, y):
    """Find the unit in the sub groups
    Navigate through unitlists and find the unit list that consists of both x and y
    """
    set_x_y = set([x, y])
    sub_unit = [a for a in unitlists if set_x_y.issubset(set(a))]
    # print(find_units, sub_unit)
    return set(sum(sub_unit, [])) - set_x_y


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers in unit lists
    # print('naked_twins')
    # navigate through unitlists and find the keys with 2 matching values
    for u in unitlists:
        # print('current unit: ', u)
        # v_d = sorted(v_d, key=v_d.get)
        traversed_twins = []
        v_d = {x: values[x] for x in u if len(values[x]) == 2}
        for k, v in v_d.items():
            for k2, v2 in v_d.items():
                if k != k2 and v == v2 and k not in traversed_twins:
                    # print(f'twins found: {k} {k2} value {values[k]}')
                    # done with the construction of traversed_twins
                    # Now go and replace the values of the others
                    for x in u:
                        if x not in (k, k2):
                            temp = values[x]
                            # replace both values '2' and '3' from peers
                            # '23' gets split to '2' and '3'
                            for y in values[k]:
                                temp = temp.replace(y, '')
                            # Assign only if the value changed
                            if temp != values[x]:
                                # values[x] = temp
                                values = assign_value(values, x, temp)
                    pass
                # book keeping for traversed twins so double computation is eliminated
                    traversed_twins.extend([k, k2])
                    # print(traversed_twins)
                pass
            pass
        pass
    return values

    ### old code -- refactored to new code with efficient search ###
    # # twos_list = {k:v for k, v in values.items() if len(v) == 2}
    # for k, v in values.items():
    #     if len(v) == 2:
    #         for p in peers[k]:
    #             if values[p] == v and (k, p) not in traversed_twins:
    #                 print('found twin', k, p, values[k])
    #                 traversed_twins.extend([(k, p), (p, k)])
    #                 # print(traversed_twins)
    #                 # I was going through all the peers first but I should limit the search
    #                 # to the unitlists and not the entire peers
    #                 # not_twins = peers[k] - set([p])
    #                 not_twins = find_units(k, p)
    #                 # print(f'peers for {k},{p} are: {not_twins}')
    #                 # navigate through all the peers in unitlist
    #                 # ex: {'E1', 'A1', 'G1', 'B1', 'H1', 'D1', 'F1'}
    #                 for x in not_twins:
    #                     # break two digits and go through each value and replace them in unitlists
    #                     # '23' is split to '2' and '3'. '2','3' are replaced in unitlists
    #                     z = values[x]
    #                     for y in v:
    #                         z = z.replace(y, '')
    #                     if z != values[x]:
    #                         # print(f'changing {x} from {values[x]} to {z}')
    #                         assign_value(values, x, z)
    #                         values[x] = z
    #                     else:
    #                         # print(f'no change for {x}: {values[x]}')
    #                         pass
    #                     pass
    #                 pass
    #             pass
    #         pass
    # # print(len(values), values)
    # return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r + c for r in A for c in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
sqr_units = [cross(r, c) for r in ('ABC', 'DEF', 'GHI')
             for c in ('123', '456', '789')]
# find diagonal units
diag_units = [[x + y for x, y in zip(rows, cols)],
              [x + y for x, y in zip(rows, reversed(cols))]]

unitlists = row_units + col_units + sqr_units + diag_units
units = dict((s, [u for u in unitlists if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, 'length of the grid should be 81'
    d = {k: v if v != '.' else '123456789' for k, v in zip(boxes, grid)}
    [assign_value(d, k, v) for k, v in d.items() if len(v) == 1]
    # print(assignments)
    return d


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    pass


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # print('eliminate')
    for k, v in values.items():
        if len(v) == 1:
            for x in peers[k]:
                value = values[x].replace(v, '')
                values = assign_value(values, x, value)
                # values[x] = value
                pass
            pass
        pass
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # print('only_choice')
    for k, v in values.items():
        compound = ''.join([values[x] for x in peers[k]])
        uniq_values = set(v) - set(compound)
        if len(uniq_values) == 1:
            curr_v = list(uniq_values)[0]
            values = assign_value(values, k, curr_v)
            pass
        pass
    return values


def reduce_puzzle(values):
    # print('reduce_puzzle')
    stuck = False
    while not stuck:
        # print(values)
        ones_before = len([k for k, v in values.items() if len(v) == 1])

        # eliminate
        values = eliminate(values)
        # only choice
        values = only_choice(values)
        # find twins
        values = naked_twins(values)

        ones_after = len([k for k, v in values.items() if len(v) == 1])

        if ones_before == ones_after:
            stuck = True
            pass
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        pass
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # print('after ', values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    _, s = min((len(values[x]), x) for x in boxes if len(values[x]) > 1)
    # print(s)
    # print('in search ', s, values[s])
    # Now use recurrence to solve each one of the resulting sudokus, and
    for v in values[s]:
        new_dict = values.copy()
        new_dict[s] = v
        ## recursion 
        attempt = search(new_dict)
        if attempt:
            return attempt

    ## recursion will fail if I uncomment the line below why?
    # return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        print(assignments)
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
