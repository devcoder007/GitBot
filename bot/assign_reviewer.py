from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from dynamo_search import search
from get_secrets import get_secret

client = WebClient(token=get_secret())



def assign_reviewer(filtered_data, channel):
    user = ("<@{}>".format(search(filtered_data["user"])))
    payload = {
        "channel": channel,
        "attachments": [
            {
                "mrkdwn_in": ["text"],
                "color": "#36a64f", 
                "pretext": ("A pull request created by {} is waiting for your review {}, please look into it.".format(user, filtered_data["slack_user_id"])),
                "author_name": user,
                "author_link": filtered_data["user_url"],
                "title": ("#{} {}".format(filtered_data["pull_request_number"], filtered_data["pull_request_title"])),
                "title_link": filtered_data["pull_request_url"],
                "footer": filtered_data["name"],
                "footer_icon": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
                "ts": filtered_data["tstamp"]
            }
        ]
    }


    try:
        response = client.chat_postMessage(**payload)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")