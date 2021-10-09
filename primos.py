from flask import Flask, request, jsonify


# Instancia do Flask
app = Flask(__name__)


# Funcao base de primo
def is_primo(n):
    n = int(n)
    check = 0
    if (n <= 1):
        return False
    for count in range(2, n):
        if (n % count == 0):
            check += 1
    if (check == 0):
        return True
    else:
        return False


# URL calcular se um numero e primo
@app.route("/is_primo/", methods=["GET"])
def primo():
    if (request.method == "GET"):
        if (request.args.get("n")):
            n = request.args.get("n")
            try:
                checker = is_primo(n)
                if (checker is True):
                    return {"primo": "True"}
                if (checker is False):
                    return {"primo": "False"}
            except Exception:
                return {"primo": "False", "ValueError": "Digite um número válido"}
        else:
            return {"n": "null", "InputError": "Digite algum valor"}


# URL calcular n primos ate n
@app.route("/get_primos/", methods=["GET"])
def get_primos():
    if (request.method == "GET"):
        if (request.args.get("total")):
            try:
                total = int(request.args.get("total"))
                all_primos = []
                for n in range(2, total+1):
                    checker = is_primo(n)
                    if (checker is True):
                        all_primos.append(n)
                if (len(all_primos) > 0):
                    return jsonify(all_primos)
                else:
                    return {"Type": "Invalid", "ValueError": "Digite um número maior ou igual a 2"}
            except Exception:
                return {"Type": "not_int", "ValueError": "Digite um número válido"}
        else:
            return {"n": "null", "InputError": "Digite algum valor"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
