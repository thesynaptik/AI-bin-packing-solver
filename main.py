from genetic_algo import genetic_algorithm
from backtracking_algo import BacktrackingBinPacking
import gui

def main():
    print("Bin Packing Solver\n")

    items = list(map(int, input("Enter items: ").split()))
    capacity = int(input("Enter capacity: "))

    print("\n1- Genetic")
    print("2- Backtracking")
    print("3- Both")

    choice = input("> ")

    if choice == "1":
        print("\nGenetic Result:", genetic_algorithm(items, capacity))

    elif choice == "2":
        solver = BacktrackingBinPacking(items, capacity)
        print("\nBacktracking Result:", solver.solve())

    elif choice == "3":
        print("\nGenetic:", genetic_algorithm(items, capacity))  

        solver = BacktrackingBinPacking(items, capacity)
        print("\nBacktracking:", solver.solve())


if __name__ == "__main__":
    main()