from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
        try:
            a = float(request.form["a"])
            b = float(request.form["b"])
            op = request.form["op"]

            if op == "add":
                result = a + b
            elif op == "sub":
                result = a - b
            elif op == "mul":
                result = a * b
            elif op == "div":
                if b == 0:
                    error = "Không thể chia cho 0"
                else:
                    result = a / b
        except ValueError:
            error = "Vui lòng nhập số hợp lệ"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
