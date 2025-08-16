from colorama import Fore, Back, Style, init
init(autoreset=True)  # Resets colors after every print

import random

grid = [[ random.randint(0,10) for _ in range(10)] for _ in range(10)]
for row in grid:
    for value in row:
        if value > 8:
            print(Fore.RED + f"{value:2}", end=" ")
        elif value >= 5:
            print(Fore.YELLOW + f"{value:2}", end=" ")
        else:
            print(Fore.GREEN + f"{value:2}", end=" ")
    print()
    
def color_demand(value): # Universal conditional function for demand
    if value > 8:
        return Fore.RED + str(value)
    elif value > 5:
        return Fore.YELLOW + str(value)
    else:
        return Fore.GREEN + str(value)

def iterate_demand_grid(): # Just interates the grid and prints vals, probably not needed
    for row in range(10):
        for col in range(10):
            print(f"{row}, and {col}, has demand of {grid[row][col]}")

def get_demand(row, col): # Demand at a certain cell
    if 0 <= row < 10 and 0 <= col < 10:
        return grid[row][col]
    else:
        print("Out of bounds")
        raise IndexError("Row or column index out of bounds")
    
def high_demand_locations(demand): # prints all cells above a specific demand
    high_demand = []
    not_found = 0
    for row in range(10):
        for col in range(10):
            if grid[row][col] > demand:
                high_demand.append((row, col, grid[row][col]))
                print(f"High demand at ({row}, {col}) with demand {grid[row][col]}")
            else:
                not_found += 1
                if not_found == 100:
                    print("No locations with high demand found")
                    return high_demand
                else:
                    pass
    print(high_demand)
    return high_demand


def get_coverage_cells(row, col, radius): # Uses Manhattan distance, to find cells within the radius
    coverage_cells = []
    for r in range(10):
        for c in range(10):
            if abs(r - row) + abs(c - col) <= radius: # Switch to Euclidean later
                coverage_cells.append((r, c))
    
    print('\n')
    demand_coverage = sum(grid[r][c] for r, c in coverage_cells)
    for r in range(10):
        for c in range(10):
            value = grid[r][c]
            if (r,c) in coverage_cells:
                print(Back.GREEN + f"{value:2}", end=" ")
            else:
                print(Back.WHITE + f"{value:2}", end=" ")

        print()
    print(coverage_cells)
    print(f"Demand covered in this configuration: {demand_coverage}")
    return coverage_cells
            
def covered_demand(row, col, radius):
    cells = get_coverage_cells(row, col, radius)
    cell_sum = sum(grid[r][c] for r, c in cells)
    print(cell_sum)
    return cell_sum           
def place_reactors(grid, num_reactors, radius):
    placed_reactors = []
    remaining_demand = [row.copy() for row in grid]

    for _ in range(num_reactors):
        best_cell = None
        max_covered = -1

        # Scan the whole grid to find the best place for this reactor
        for row in range(10):
            for col in range(10):
                coverage = get_coverage_cells(row, col, radius)  # You might want a no-print version
                covered = sum(remaining_demand[r][c] for r, c in coverage)

                if covered > max_covered:
                    max_covered = covered
                    best_cell = (row, col)

        if best_cell is None:
            break  # No more demand left

        # Place the reactor
        placed_reactors.append(best_cell)

        # Remove demand that this reactor now covers
        for r, c in get_coverage_cells(*best_cell, radius):
            remaining_demand[r][c] = 0

    print(f"Placed reactors at: {placed_reactors}")
    return placed_reactors

                

# place_reactors(grid, 3, 2) 



