# Matrix Multiplier

Matrix Multiplier is a Python GUI application built with Tkinter and Sympy that allows you to create, manipulate, and perform operations on matrices containing symbolic values. The application supports operations such as multiplication, addition, subtraction, transpose, and conjugate. All results are rendered in a neat LaTeX-like format.

## Features

- **Dynamic Matrix Creation:** Add or remove matrices on the fly.
- **Customizable Matrix Size:** Select matrix dimensions using dropdowns.
- **Symbolic Computation:** Work with numbers and symbolic expressions using Sympy.
- **Multiple Operations:** Choose operations (Multiply, Add, Subtract, Transpose, Conjugate) from a dropdown menu.
- **LaTeX Rendered Output:** View results as rendered mathematical expressions.
- **User-Friendly Interface:** Simple and intuitive layout using Tkinter.

## Detailed Features

- **Matrix Setup:** Easily create matrices with user-defined rows and columns.
- **Real-Time Updates:** Instantly see changes as you modify matrices.
- **Error Handling:** Prompts for invalid entries to help maintain correct symbolic or numeric input.
- **Flexible Operations:** Support for combining symbolic algebra with numerical calculations.
- **Visual Output:** Matplotlib integration provides a clear, well-formatted view of results.
- **Interactive UI:** Intuitive Tkinter-based interface for seamless user interactions.

## Requirements

- Python 3.x
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with Python)
- [Sympy](https://www.sympy.org/en/index.html)
- [Pillow (PIL)](https://python-pillow.org/)
- [Matplotlib](https://matplotlib.org/)

## Installation

Install the required packages using pip:

```bash
pip install sympy pillow matplotlib
```

## Usage

Run the application by executing:

```bash
python d:\Repos\matrix-multiplier\matrix_multiplier.py
```

Use the GUI to add matrices, set their dimensions, enter values (numeric or symbolic), and select the desired operation from the dropdown menu to see the result rendered in a mathematical format.

## License

This project is licensed under the MIT License.