from flask import Flask, request, jsonify

# Manipulate RabbitMQ
import pika


# Instancia do Flask
app = Flask(__name__)


# Define the host of connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# connect to the IP
channel = connection.channel()
channel.queue_declare(queue='prime')


# Function of prime numbers
def is_prime(n):
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
@app.route("/is_prime/", methods=["GET"])
def prime():
    if (request.method == "GET"):
        if (request.args.get("n")):
            n = request.args.get("n")
            # Send a message when get the variable
            # and starts calculating
            channel.basic_publish(exchange='',
                                  routing_key='prime',
                                  body="Calculating...")
            print({"URI": "/is_prime", "n": f"{n}"})
            try:
                checker = is_prime(n)
                if (checker is True):
                    channel.basic_publish(exchange='',
                                          routing_key='prime',
                                          body=f"{n} is a prime number.")
                    print({"n": f"{n}", "is_prime": "True"})
                    return {"prime": "True"}
                if (checker is False):
                    channel.basic_publish(exchange='',
                                          routing_key='prime',
                                          body=f"{n} is not prime number.")
                    print({"n": f"{n}", "is_prime": "False"})
                    return {"prime": "False"}
            except Exception:
                return {"prime": "False", "ValueError": "Type a valid number"}
        else:
            return {"n": "null", "InputError": "Type some value"}


# URL Calculate the first n range numbers that is prime
@ app.route("/get_prime/", methods=["GET"])
def get_prime():
    if (request.method == "GET"):
        if (request.args.get("total")):
            try:
                total = int(request.args.get("total"))
                # Send a message when get the variable
                # and starts calculating
                channel.basic_publish(exchange='',
                                      routing_key='prime',
                                      body="Calculating...")
                print({"URI": "/get_prime", "total": f"{total}"})
                all_prime = []
                for n in range(2, total+1):
                    checker = is_prime(n)
                    if (checker is True):
                        all_prime.append(n)
                if (len(all_prime) > 0):
                    channel.basic_publish(exchange='',
                                          routing_key='prime',
                                          body=f"First {total} numbers has {len(all_prime)} prime numbers.")
                    print({"total": f"{total}", "primes": f"{len(all_prime)}"})
                    return jsonify(all_prime)
                else:
                    return {"Type": "Invalid", "ValueError": "Type a number >= 2"}
            except Exception:
                return {"Type": "not_int", "ValueError": "Type a valid number"}
        else:
            return {"n": "null", "InputError": "Type some value"}


if __name__ == "__main__":
    print(' [*] Waiting to search...')
    app.run(host="127.0.0.1", port=5000, debug=True)
