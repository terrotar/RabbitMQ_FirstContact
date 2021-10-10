<h1>About</h1>

That's project is a simple application with Python/Flask/RabbitMQ. It basically has two URL, is_primo and get_primo, the first one is used to know if a number(n) is a prime number or not and the second URL is used to calculate a range until the number inserted(total) and it display how many and which one of those are primes.

<h1>How to run</h1>

To run the program is very simple and I'll kist the steps right below:

- Open 2 terminals;

- The first one you will start the receiver_prime.py by the command:

    python receiver_prime.py

- The seccond one you will start the Flask application with the command:

    python prime.py
    

- Now, you open your browser and acess your localhost:5000 or http://127.0.0.1:5000.

- You have two URL's to acess, and each one of them has 1 variable to be inserted.

- http://127.0.0.1:5000/is_prime/?n=10

    Note that the URL(is_prime) accept one variable called n, which will be the number you want to check if it is prime or not.
    
- http://127.0.0.1:5000/get_prime/?total=10

    Note that the URL(get_prime) accept one variable called total, which will be the final number you want to verify from 2 until the number inserted to calculate the prime numbers and how many they are.
    

OBS: Don't forget to type the '?' before the variable, wich indicates that the next value will be a variable.


For every search you do using the URL's, a message in your other terminal with the receiver_prime.py will display when the process starts and the results when it's done. You can try with some small number(10) and a bigger(100000) after to test the time response of Python to calculate. All the response were created with RabbitMQ, a new tool that I'm studying and learning.
