from colorama import Fore, Back, Style, init
init(autoreset=True)  

import matplotlib.pyplot as plt
import random

rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
num_reactors = int(input("Enter number of reactors to place: "))
radius = int(input("Enter reactor radius: "))
min_val = int(input("Enter minimum grid demand value: "))
max_val = int(input("Enter maximum grid demand value: "))


grid = [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


def print_colored_grid(grid):
    for row in grid:
        for value in row:
            if value > 8:
                print(Fore.RED + f"{value:2}", end=" ")
            elif value >= 5:
                print(Fore.YELLOW + f"{value:2}", end=" ")
            else:
                print(Fore.GREEN + f"{value:2}", end=" ")
        print()
print_colored_grid(grid)


def get_coverage_cells(row, col, radius):
    """Return list of cells covered by reactor at (row, col) with given radius."""
    coverage_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if abs(r - row) + abs(c - col) <= radius:
                coverage_cells.append((r, c))
    return coverage_cells

def covered_demand(row, col, radius):
    cells = get_coverage_cells(row, col, radius)
    return sum(grid[r][c] for r, c in cells)

def place_reactors(grid, num_reactors, radius):
    placed_reactors = []
    remaining_demand = [row.copy() for row in grid]

    for _ in range(num_reactors):
        best_cell = None
        max_covered = -1

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                coverage = get_coverage_cells(row, col, radius)
                covered = sum(remaining_demand[r][c] for r, c in coverage)
                if covered > max_covered:
                    max_covered = covered
                    best_cell = (row, col)

        if best_cell is None:
            break

        placed_reactors.append(best_cell)

        for r, c in get_coverage_cells(*best_cell, radius):
            remaining_demand[r][c] = 0

    print(f"\nPlaced reactors at: {placed_reactors}")
    return placed_reactors


def plot_final_coverage(grid, placed_reactors, radius):
    plt.imshow(grid, cmap="YlOrRd", origin="upper")
    plt.colorbar(label="Energy Demand")

    total_demand = sum(sum(row) for row in grid)
    total_covered = 0
    covered_cells = set()


    for row, col in placed_reactors:
        coverage_cells = get_coverage_cells(row, col, radius)
        for r, c in coverage_cells:
            covered_cells.add((r,c))
            plt.scatter(c, r, color="lime", marker="s")
        plt.scatter(col, row, color="blue", marker="x", s=100)
    
    total_covered = sum(grid[r][c] for r, c in covered_cells)
    coverage_text = f"Total demand covered by reactors: {total_covered}/{total_demand}  ({total_covered/total_demand:.1%})"

    plt.title("Final Reactor Placement & Coverage")
    plt.suptitle(coverage_text, y=0.92, fontsize=10, color="black")
    plt.show()


placed = place_reactors(grid, num_reactors, radius)
plot_final_coverage(grid, placed, radius)
