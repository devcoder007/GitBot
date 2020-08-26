from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from dynamo_search import search
from get_secrets import get_secret
client = WebClient(token=get_secret())


def push_message(filtered_data, channel):
    
    if filtered_data["action"] == "opened" or filtered_data["action"] == "reopened":
        color = "#36a64f"
    else:
        color = "#ff0808" 
    
    slack_user_id = ("<@{}>".format(search(filtered_data["user"])))

    payload = {
        "channel": channel,
        "attachments": [
            {
                "mrkdwn_in": ["text"],
                "color": color, 
                "pretext": ("A pull request has been {} by {} | {}".format(filtered_data["action"], filtered_data["user"], slack_user_id)),
                "author_name": filtered_data["user"],
                "author_link": filtered_data["user_url"],
                "author_icon": filtered_data["user_avatar_url"],
                "title": ("#{} {}".format(filtered_data["pull_request_number"], filtered_data["pull_request_title"])),
                "title_link": filtered_data["pull_request_url"],
                "text": ("{}".format(filtered_data["body"])),
                "thumb_url": filtered_data["user_avatar_url"],
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