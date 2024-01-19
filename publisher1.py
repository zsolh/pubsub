import os
from google.cloud import pubsub_v1

credentials_path = '/home/figura/Dokumentumok/Aaron/pubsub/pp-demo.private-key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/total-media-411521/topics/MyTopic1'


data = 'MyTopic1 data'
data = data.encode('utf-8')
attributes = {
    'nextTopicName': 'projects/total-media-411521/topics/MyTopic2',
    'nextSubscriptionName': 'projects/total-media-411521/subscriptions/MyTopic2-sub',
}

future = publisher.publish(topic_path, data, **attributes)
print(f'published message id {future.result()}')


