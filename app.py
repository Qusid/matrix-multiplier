from flask import Flask, render_template, request, flash
import sympy

app = Flask(__name__)
app.secret_key = "secret-key"  # change for production

def parse_matrix(text):
    # Parse matrix input: each nonempty line is a row; numbers separated by spaces or commas.
    rows = []
    for line in text.strip().splitlines():
        if line.strip():
            numbers = [sympy.sympify(x) for x in line.replace(',', ' ').split()]
            rows.append(numbers)
    return sympy.Matrix(rows)

@app.route("/", methods=["GET", "POST"])
def index():
    result_latex = None
    result_text = ""
    matrix_values = {}
    if request.method == "POST":
        op = request.form.get("operation")
        matrices = []
        # Collect matrices from any field whose name starts with "matrix"
        for key, value in request.form.items():
            if key.startswith("matrix") and value.strip():
                try:
                    m = parse_matrix(value)
                    matrices.append(m)
                    matrix_values[key] = value  # save original text
                except Exception as e:
                    flash("Error parsing matrix: " + str(e))
        if op in ["Multiply", "Add", "Subtract"] and len(matrices) < 2:
            flash("At least two matrices are required for this operation.")
        else:
            try:
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
                result_latex = sympy.latex(result)
                result_text = str(result)
            except Exception as e:
                flash("Error during computation: " + str(e))
    return render_template("index.html", result_latex=result_latex,
                           result_text=result_text, matrix_values=matrix_values)

if __name__ == "__main__":
    app.run(debug=True)
