import logging
from google.cloud import pubsub_v1
import time
import json
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build, build_from_document
from google.cloud import pubsub_v1
import os
import subprocess

CREDENTIALS_PATH_ENV_PROPERTY='GOOGLE_APPLICATION_CREDENTIALS'

class HangoutsBot:
    def __init__(self, project_id=None, subscription_name=None):
        self.logger = logger = logging.getLogger()
        self.logger.info("Initialised bot")
        self.subscription_name = os.getenv('CROUDBOT_SUBSCRIPTION_NAME', None) if subscription_name == None else subscription_name
        if self.subscription_name == None:
            raise Exception('CroudBot Subscription Name is not set')
        self.logger.info("Bot using Subscription Name '{}'".format(self.subscription_name))
        self.project_id = os.getenv('CROUDBOT_PROJECT_ID', None) if project_id == None else project_id
        if self.project_id == None:
            raise Exception('CroudBot Project Id is not set')
        self.logger.info("Bot using Project ID '{}'".format(self.project_id))

    def listen(self, callback=None):
        if callback == None:
            callback = self.listenerCallback
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            self.project_id, self.subscription_name)
        subscriber.subscribe(subscription_path, callback=callback)

        self.logger.info('Listening for messages on {}'.format(subscription_path))
        while True:
            time.sleep(60)

    def listenerCallback(self, message):
        print('Received message: {}'.format(message.data))

        event_data = json.loads(message.data.decode('utf-8'))
        space_name = event_data['space']['name']

        # If the bot was removed, we don't need to return a response.
        if event_data['type'] == 'REMOVED_FROM_SPACE':
            print('Bot removed rom space {}'.format(space_name))
            return

        response = self.formatResponse(event_data)

        thread_key = None
        if 'message' in event_data:
            if event_data['message']['thread'] != None:
                thread_key = event_data['message']['thread']

        # Send the asynchronous response back to Hangouts Chat

        self.sendMessage(response, space_name, thread_key)
        message.ack()

    def chat(self):
        if not hasattr(self, 'chat_object'):
            scopes = ['https://www.googleapis.com/auth/chat.bot']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                os.environ[CREDENTIALS_PATH_ENV_PROPERTY], scopes)
            http_auth = credentials.authorize(Http())
            self.chat_object = build('chat', 'v1', http=http_auth, cache_discovery=False)

        return chat_object

    def sendMessage(self, response, space_name, thread_key=None):
        scopes = ['https://www.googleapis.com/auth/chat.bot']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.environ[CREDENTIALS_PATH_ENV_PROPERTY], scopes)
        http_auth = credentials.authorize(Http())

        self.chat().spaces().messages().create(
            parent=space_name,
            body=response,
            threadKey=thread_key).execute()

    def formatResponse(self, event):
        """Determine what response to provide based upon event data.
        Args:
        event: A dictionary with the event data.
        """

        event_type = event['type']

        text = ""
        senderName = event['user']['displayName']

        # Case 1: The bot was added to a room
        if event_type == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
            text = 'Thanks for adding me to {}!'.format(event['space']['displayName'])

        # Case 2: The bot was added to a DM
        elif event_type == 'ADDED_TO_SPACE' and event['space']['type'] == 'DM':
            text = 'Thanks for adding me to a DM, {}!'.format(senderName)

        elif event_type == 'MESSAGE':
            text = 'Your message, {}: "{}"'.format(senderName, event['message']['text'])
            response = { 'text': text }

        return response

    def getSpaceByName(self, name):
        spaces = self.chat().spaces().list().execute()
        for space in spaces['spaces']:
            if space['displayName'] == self.space_name:
                space_object = space
                return space_object

        return None

