from flask import Flask, request, jsonify

# Manipulate RabbitMQ
import pika


# Instancia do Flask
app = Flask(__name__)


# Define the host of connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# connect to the IP
channel = connection.channel()


# Declare the queue name to send msgs
channel.queue_declare(queue='primo')


# Function of prime numbers
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


# URL Calculate if a number is prime
@app.route("/is_primo/", methods=["GET"])
def primo():
    if (request.method == "GET"):
        if (request.args.get("n")):
            n = request.args.get("n")
            # Send a message when get the variable
            # and starts calculating
            channel.basic_publish(exchange='',
                                  routing_key='primo',
                                  body="Calculating...")
            print({"URI": "/is_primo", "n": f"{n}"})
            try:
                checker = is_primo(n)
                if (checker is True):
                    channel.basic_publish(exchange='',
                                          routing_key='primo',
                                          body=f"{n} is a prime number.")
                    print({"n": f"{n}", "is_prime": "True"})
                    return {"primo": "True"}
                if (checker is False):
                    channel.basic_publish(exchange='',
                                          routing_key='primo',
                                          body=f"{n} is not prime number.")
                    print({"n": f"{n}", "is_prime": "False"})
                    return {"primo": "False"}
            except Exception:
                return {"primo": "False", "ValueError": "Digite um número válido"}
        else:
            return {"n": "null", "InputError": "Digite algum valor"}


# URL Calculate the first n range numbers that is prime
@ app.route("/get_primos/", methods=["GET"])
def get_primos():
    if (request.method == "GET"):
        if (request.args.get("total")):
            try:
                total = int(request.args.get("total"))
                # Send a message when get the variable
                # and starts calculating
                channel.basic_publish(exchange='',
                                      routing_key='primo',
                                      body=f"Calculating...")
                print({"URI": "/get_primos", "n": f"{total}"})
                all_primos = []
                for n in range(2, total+1):
                    checker = is_primo(n)
                    if (checker is True):
                        all_primos.append(n)
                if (len(all_primos) > 0):
                    channel.basic_publish(exchange='',
                                          routing_key='primo',
                                          body=f"First {total} numbers has {len(all_primos)} prime numbers.")
                    print({"n": f"{total}", "primos": f"{len(all_primos)}"})
                    return jsonify(all_primos)
                else:
                    return {"Type": "Invalid", "ValueError": "Digite um número maior ou igual a 2"}
            except Exception:
                return {"Type": "not_int", "ValueError": "Digite um número válido"}
        else:
            return {"n": "null", "InputError": "Digite algum valor"}


if __name__ == "__main__":
    print(' [*] Waiting to search...')
    app.run(host="127.0.0.1", port=5000, debug=True)
