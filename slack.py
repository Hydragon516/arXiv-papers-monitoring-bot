from slacker import Slacker

token = '****'
slack = Slacker(token)

def send_mdg_to_slack(message):
    slack.chat.post_message('#general', message)

def send_file_to_slack(file):
    slack.files.upload(file, channels='#general')