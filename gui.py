import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt

from genetic_algo import genetic_algorithm
from backtracking_algo import BacktrackingBinPacking


# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Bin Packing Solver")
window.geometry("950x650")

# ---------------- INPUTS ----------------
frame = tk.Frame(window)
frame.pack(pady=10)

tk.Label(frame, text="Items").grid(row=0, column=0, padx=5)
items_entry = tk.Entry(frame, width=40)
items_entry.grid(row=0, column=1)
items_entry.insert(0, "4 8 1 4 2 1")

tk.Label(frame, text="Capacity").grid(row=1, column=0, padx=5)
capacity_entry = tk.Entry(frame, width=40)
capacity_entry.grid(row=1, column=1)
capacity_entry.insert(0, "10")

algo_combo = ttk.Combobox(
    frame,
    values=["Backtracking", "Genetic", "Compare"],
    width=37
)
algo_combo.grid(row=2, column=1, pady=10)
algo_combo.current(0)

# ---------------- RESULT ----------------
result_label = tk.Label(window, font=("Arial", 12, "bold"))
result_label.pack()

# ---------------- CANVAS ----------------
canvas = tk.Canvas(window, width=900, height=400, bg="white")
canvas.pack(pady=10)


# ---------------- DRAW ----------------
def draw_bins(bins, items, title):
    canvas.delete("all")

    canvas.create_text(
        450, 20,
        text=title,
        font=("Arial", 16, "bold")
    )

    x = 40

    for i, b in enumerate(bins):

        canvas.create_rectangle(x, 60, x + 120, 320, width=2)

        canvas.create_text(
            x + 60, 40,
            text=f"Bin {i+1}",
            font=("Arial", 11, "bold")
        )

        y = 310

        total = 0

        for idx in b:
            size = items[idx]
            h = size * 10

            canvas.create_rectangle(
                x + 10, y - h,
                x + 110, y
            )

            canvas.create_text(
                x + 60,
                y - h / 2,
                text=str(size)
            )

            y -= h + 5
            total += size

        canvas.create_text(
            x + 60, 340,
            text=f"Total = {total}"
        )

        x += 140


# ---------------- GRAPH ----------------
def graph(bt, ga):

    names = ["Backtracking", "Genetic"]
    times = [bt, ga]

    plt.figure(figsize=(7, 5))

    bars = plt.bar(names, times, width=0.5)

    plt.title("Execution Time Comparison", fontsize=16)
    plt.xlabel("Algorithms", fontsize=12)
    plt.ylabel("Time (seconds)", fontsize=12)

    plt.grid(axis='y', linestyle='--', alpha=0.7)

   
    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.6f}s",
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.tight_layout()
    plt.show()


# ---------------- SOLVE ----------------
def solve():

    try:
        items = list(map(int, items_entry.get().split()))
        capacity = int(capacity_entry.get())

    except:
        messagebox.showerror("Error", "Invalid Input")
        return

    choice = algo_combo.get()

    # ---------- BACKTRACKING ----------
    if choice == "Backtracking":

        start = time.perf_counter()

        solver = BacktrackingBinPacking(items, capacity)
        result = solver.solve()

        t = time.perf_counter() - start

        bins = result["bins"]

        result_label.config(
            text=f"Bins: {len(bins)}   |   Time: {t:.6f}s"
        )

        draw_bins(bins, items, "Backtracking")

    # ---------- GENETIC ----------
    elif choice == "Genetic":

        start = time.perf_counter()

        solution = genetic_algorithm(items, capacity)

        t = time.perf_counter() - start

        bins_dict = {}

        for i, b in enumerate(solution):
            bins_dict.setdefault(b, []).append(i)

        bins = list(bins_dict.values())

        result_label.config(
            text=f"Bins: {len(bins)}   |   Time: {t:.6f}s"
        )

        draw_bins(bins, items, "Genetic")

    # ---------- COMPARE ----------
    else:

        # Backtracking
        start = time.perf_counter()

        solver = BacktrackingBinPacking(items, capacity)
        bt_result = solver.solve()

        bt_time = time.perf_counter() - start

        # Genetic
        start = time.perf_counter()

        ga_solution = genetic_algorithm(items, capacity)

        ga_time = time.perf_counter() - start

        ga_dict = {}

        for i, b in enumerate(ga_solution):
            ga_dict.setdefault(b, []).append(i)

        ga_bins = list(ga_dict.values())

        result_label.config(
            text=
            f"Backtracking: {len(bt_result['bins'])} bins ({bt_time:.6f}s)    ||    "
            f"Genetic: {len(ga_bins)} bins ({ga_time:.6f}s)"
        )

        draw_bins(bt_result["bins"], items, "Best Backtracking Solution")

        graph(bt_time, ga_time)


# ---------------- BUTTON ----------------
tk.Button(
    window,
    text="Solve",
    command=solve,
    bg="lightblue",
    font=("Arial", 12, "bold")
).pack(pady=10)

# ---------------- RUN ----------------
if __name__ == "__main__":
    window.mainloop()