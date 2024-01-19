import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = '/home/figura/Dokumentumok/Aaron/pubsub/pp-demo.private-key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


timeout = 5.0                                                                       # timeout in seconds

global subscriber
subscriber = pubsub_v1.SubscriberClient()

subscription_path = 'projects/total-media-411521/subscriptions/MyTopic-sub'


def handle_message(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')

    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")

    subscription_path = message.attributes.get('nextSubscriptionName')
    print(subscription_path)
    subscriber.subscribe(subscription_path, callback=handle_message)    
    message.ack()           


if __name__ == "__main__":
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=handle_message)
    print(f'Listening for messages on {subscription_path}')

    with subscriber:                                                # wrap subscriber in a 'with' block to automatically call close() when done
        try:
            # streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()                          # going without a timeout will wait & block indefinitely
        except TimeoutError:
            streaming_pull_future.cancel()                          # trigger the shutdown
            streaming_pull_future.result()                          # block until the shutdown is complete
