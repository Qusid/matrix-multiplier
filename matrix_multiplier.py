import tkinter as tk
from tkinter import messagebox
import sympy
from io import BytesIO
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

default_size_options = ["2x2", "3x3", "4x4"]

def render_latex(expr):
    # Render a sympy expression to a PhotoImage using matplotlib mathtext
    plt.close('all')
    fig = plt.figure(figsize=(0.8, 0.5), dpi=100)
    fig.text(0.5, 0.5, "$" + sympy.latex(expr) + "$", horizontalalignment='center',
             verticalalignment='center', fontsize=12)
    buf = BytesIO()
    plt.axis('off')
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    buf.seek(0)
    img = Image.open(buf)
    photo = ImageTk.PhotoImage(img)
    return photo

def compute_operation(op):
    try:
        matrices = []
        for m in matrix_entries:
            grid = m["grid"]
            matrix_list = []
            for row in grid:
                matrix_row = []
                for entry in row:
                    val = entry.get().strip()
                    if val == "":  # fill empty cells with 0
                        val = "0"
                    matrix_row.append(sympy.sympify(val))
                matrix_list.append(matrix_row)
            matrices.append(sympy.Matrix(matrix_list))
        
        # For operations that need at least two matrices.
        if op in ["Multiply", "Add", "Subtract"] and len(matrices) < 2:
            messagebox.showerror("Error", "At least two matrices are required for this operation.")
            return

        if op == "Multiply":
            result = matrices[0]
            for mat in matrices[1:]:
                result = result * mat
        elif op == "Add":
            result = matrices[0]
            for mat in matrices[1:]:
                result = result + mat
        elif op == "Subtract":
            result = matrices[0]
            for mat in matrices[1:]:
                result = result - mat
        elif op == "Transpose":
            result = matrices[0].T
        elif op == "Conjugate":
            result = matrices[0].conjugate()
        else:
            result = matrices[0]

        # Display result as a grid of LaTeX-rendered images per cell.
        for widget in result_matrix_frame.winfo_children():
            widget.destroy()
        rows, cols = result.shape
        for i in range(rows):
            for j in range(cols):
                cell_value = result[i, j]
                photo = render_latex(cell_value)
                lbl = tk.Label(result_matrix_frame, image=photo, bg="white", relief="ridge")
                lbl.image = photo
                lbl.grid(row=i, column=j, padx=2, pady=2)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_grid(m, rows, cols):
    # Update the grid entries based on selected rows and columns
    r, c = int(rows), int(cols)
    for widget in m["grid_frame"].winfo_children():
        widget.destroy()
    grid = []
    for i in range(r):
        row_entries = []
        for j in range(c):
            entry = tk.Entry(m["grid_frame"], width=5, font=("Arial", 12), justify="center")
            entry.grid(row=i, column=j, padx=2, pady=2)
            row_entries.append(entry)
        grid.append(row_entries)
    m["grid"] = grid

def remove_matrix(m, container):
    # Remove matrix m and its container from the global list and update numbering
    global matrix_entries
    if m in matrix_entries:
        matrix_entries.remove(m)
    container.destroy()
    # Renumber remaining matrices
    for idx, mat in enumerate(matrix_entries, start=1):
        if "header" in mat:
            mat["header"].config(text=f"Matrix {idx}:")
    update_plus_button()

def add_matrix_entry():
    m = {}
    container = tk.Frame(matrix_container, bd=2, relief="groove", padx=10, pady=10, bg="#f0f0f0")
    container.pack(side=tk.LEFT, padx=10, pady=10)
    header_frame = tk.Frame(container, bg="#f0f0f0")
    header_frame.pack(fill="x")
    label = tk.Label(header_frame, text=f"Matrix {len(matrix_entries)+1}:", font=("Arial", 14), bg="#f0f0f0")
    label.pack(side=tk.LEFT, expand=True, pady=5)
    # Store header label for future renumbering
    m["header"] = label
    # Show remove button if at least one matrix already exists
    if len(matrix_entries) >= 1:
        tk.Button(header_frame, text="X", font=("Arial", 10), bg="red", fg="white",
                  command=lambda m=m, container=container: remove_matrix(m, container)).pack(side=tk.RIGHT, padx=5)
    
    # Horizontal drop-down menus for row and column selection without extra labels
    rows_options = ["2", "3", "4", "5"]
    cols_options = ["2", "3", "4", "5"]
    row_var = tk.StringVar(); row_var.set("3")
    col_var = tk.StringVar(); col_var.set("3")
    # Place drop-down menus side by side in a centered frame
    size_frame = tk.Frame(container, bg="#f0f0f0")
    size_frame.pack(anchor="center", pady=5)
    row_menu = tk.OptionMenu(size_frame, row_var, *rows_options, command=lambda r, m=m, cv=col_var: update_grid(m, r, cv.get()))
    row_menu.config(font=("Arial", 12), bg="white")
    row_menu.pack(side=tk.LEFT, padx=5)
    col_menu = tk.OptionMenu(size_frame, col_var, *cols_options, command=lambda c, m=m, rv=row_var: update_grid(m, rv.get(), c))
    col_menu.config(font=("Arial", 12), bg="white")
    col_menu.pack(side=tk.LEFT, padx=5)
    
    grid_frame = tk.Frame(container, bg="#f0f0f0")
    grid_frame.pack()
    m["grid_frame"] = grid_frame
    update_grid(m, row_var.get(), col_var.get())
    matrix_entries.append(m)
    update_plus_button()

app = tk.Tk()
app.title("Matrix Multiplier")
app.configure(bg="#e0e0e0")

# Horizontal layout: left frame for matrices, right frame for result
main_frame = tk.Frame(app, bg="#e0e0e0")
main_frame.pack(padx=20, pady=20)

matrix_frame = tk.Frame(main_frame, bg="#e0e0e0")
matrix_frame.pack(side=tk.LEFT, padx=10)
# New container to hold all matrices plus the plus button
matrix_container = tk.Frame(matrix_frame, bg="#e0e0e0")
matrix_container.pack()

result_frame = tk.Frame(main_frame, bg="#e0e0e0")
result_frame.pack(side=tk.RIGHT, padx=10)
tk.Label(result_frame, text="Result:", font=("Arial", 14), bg="#e0e0e0").pack(pady=5)
result_matrix_frame = tk.Frame(result_frame, bd=2, relief="groove", padx=10, pady=10, bg="white")
result_matrix_frame.pack(pady=5)

matrix_entries = []
plus_button = None  # global plus button reference

def update_plus_button():
    global plus_button
    # Remove the plus button if it exists and then add it at the end of matrix_container
    if plus_button:
        plus_button.pack_forget()
    plus_button = tk.Button(matrix_container, text="+", command=add_matrix_entry, font=("Arial", 12),
                            bg="lightgreen", padx=10, pady=5)
    plus_button.pack(side=tk.LEFT, padx=10, pady=10)

# Initially add two matrices and then show plus button
add_matrix_entry()
add_matrix_entry()
update_plus_button()

# Replace the original Multiply button with an operation dropdown in control_frame.
control_frame = tk.Frame(app, bg="#e0e0e0")
control_frame.pack(pady=10)
op_options = ["Multiply", "Add", "Subtract", "Transpose", "Conjugate"]
op_var = tk.StringVar(); op_var.set(op_options[0])
tk.Label(control_frame, text="Operation:", font=("Arial", 12), bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
op_menu = tk.OptionMenu(control_frame, op_var, *op_options, command=lambda op: compute_operation(op))
op_menu.config(font=("Arial", 12), bg="white")
op_menu.pack(side=tk.LEFT, padx=5)

app.mainloop()