
import os
import io

from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)
if slack_client.rtm_connect(with_team_state=False):
    print("Starter Bot connected and running!")

def send_message(message, attachment=None):
    slack_client.api_call(
        "chat.postMessage",
        channel="#general",
        text=message,
        attachments=attachment
    )
    # print('Notifiying')

def upload_file(slack_filename, file):
    slack_client.api_call(
    "files.upload",
    filename=slack_filename,
    channels='#general',
    file=open(file, 'rb')
    )
