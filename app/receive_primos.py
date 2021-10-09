import pika


def main():
    # Create connection and channel it
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # In case of doubt, declare a queue again...
    # It does not duplicate !!!
    channel.queue_declare(queue='primo')

    # Callback function
    def callback(ch, method, properties, body):
        print(f" [x] API message received: {body}")

    # Set the callback when receive a message
    channel.basic_consume(queue='primo', on_message_callback=callback, auto_ack=True)

    # waitting for messages
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
