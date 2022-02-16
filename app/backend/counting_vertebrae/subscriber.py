# from google.cloud import pubsub_v1
# from concurrent.futures import TimeoutError
# import environ

# env = environ.Env()

# subscriber = pubsub_v1.SubscriberClient()

# project_id = env('PROJECT_ID')
# subscription_id = env('SUBSCRIPTION_ID')

# subscription_path = subscriber.subscription_path(project_id, subscription_id)

# def callback(message: pubsub_v1.subscriber.message.Message) -> None:
#     print(f"Received: {message}")
#     message.ack()

# def start_listening():
#     streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
#     print(f"Listening for messages on {subscription_path}...\n")

#     with subscriber:
#         try:
#             streaming_pull_future.result()
#         except TimeoutError:
#             streaming_pull_future.cancel()
#             streaming_pull_future.result()