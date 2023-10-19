import os
import json

from datetime import datetime

from assign_reviewer import assign_reviewer
from pull_request import push_message
from dynamo_search import search

def lambda_handler(event, context):

    channel = "demo" #os.environ["channel"]
    payload = event
    filtered_data = {}
    if payload["action"]:
        if payload["action"] == "review_requested":
            filtered_data["action"] = payload["action"]
            filtered_data["reviewer_url"] = (payload["requested_reviewer"]["repos_url"])
            filtered_data["reviewer_name"] = (payload["requested_reviewer"]["login"])
            try:
                filtered_data["slack_user_id"] = search(filtered_data["reviewer_name"] )
                filtered_data["slack_user_id"] = ("<@{}>".format(filtered_data["slack_user_id"]))
            except:
                filtered_data["slack_user_id"] = ("{}, please add your github using /github-add <your-git-usertname>".format(filtered_data["reviewer_name"]))
            filtered_data["pull_request_url"] = (payload["pull_request"]["html_url"])
            filtered_data["user"] = (payload["pull_request"]["user"]["login"])
            filtered_data["user_url"] = (payload["pull_request"]["user"]["html_url"])
            filtered_data["pull_request_number"] = (payload["pull_request"]["number"])
            filtered_data["pull_request_title"] = (payload["pull_request"]["title"])
            filtered_data["name"] = (payload["pull_request"]["head"]["repo"]["full_name"])
            filtered_data["tstamp"] = (payload["pull_request"]["created_at"])
            filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
            filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
            assign_reviewer(filtered_data, channel)

        if payload["action"] == "opened" or payload["action"] == "reopened" or payload["action"] == "closed":
            action = payload["action"]
                
            if action == "opened":
                filtered_data["tstamp"] = (payload["pull_request"]["created_at"])
                filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
                filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
            elif action == "reopened":
                filtered_data["tstamp"] = (payload["pull_request"]["updated_at"])
                filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
                filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
            else:
                filtered_data["tstamp"] = (payload["pull_request"]["closed_at"])
                filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
                filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)

            filtered_data["action"] = payload["action"]
            filtered_data["pull_request_url"] = (payload["pull_request"]["html_url"])
            filtered_data["pull_request_number"] = (payload["pull_request"]["number"])
            filtered_data["pull_request_title"] = (payload["pull_request"]["title"])
            filtered_data["user"] = (payload["pull_request"]["user"]["login"])
            filtered_data["body"] = (payload["pull_request"]["body"])
            filtered_data["user_url"] = (payload["pull_request"]["user"]["html_url"])
            filtered_data["user_avatar_url"] = (payload["pull_request"]["user"]["avatar_url"])
            filtered_data["name"] = (payload["pull_request"]["head"]["repo"]["full_name"])

            push_message(filtered_data, channel)


# import os
# import json

# from datetime import datetime

# from assign_reviewer import assign_reviewer
# from pull_request import push_message
# from dynamo_search import search
# from pull_request_state import pr_state

# def lambda_handler(event, context):

#     channel = "github-channel"
#     payload = event
#     filtered_data = {}
#     if payload["action"]:
#         if payload["action"] == "submitted":
#             if payload["review"]["state"] == "approved" or payload["review"]["state"] == "changes_requested":
#                 if payload["review"]["state"] == "approved":
#                     filtered_data["text"] = "your PR is approved"
#                     filtered_data["approver"] = payload["review"]["user"]["login"]
#                 else:
#                     filtered_data["text"] = "Changes requested in your PR"
#                 filtered_data["user"] = (payload["pull_request"]["user"]["login"])
#                 filtered_data["body"] = (payload["review"]["body"])

#                 try:
#                     filtered_data["slack_user_id"] = search(filtered_data["user"])
#                     filtered_data["slack_user_id"] = "<@" + filtered_data["slack_user_id"] + ">"
#                     filtered_data["approver_slack_user_id"] = search(filtered_data["approver"])
#                     filtered_data["approver_slack_user_id"] = "<@" + filtered_data["approver_slack_user_id"] + ">"
#                 except Exception as e:
#                     print("User not found", e)
#                 filtered_data["pull_request_url"] = (payload["pull_request"]["html_url"])
#                 filtered_data["pull_request_number"] = (payload["pull_request"]["number"])
#                 filtered_data["pull_request_title"] = (payload["pull_request"]["title"])
#                 filtered_data["tstamp"] = (payload["review"]["submitted_at"])
#                 filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
#                 filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
#                 pr_state(filtered_data, channel)

#         if payload["action"] == "review_requested":
#             filtered_data["action"] = payload["action"]
#             filtered_data["reviewer_url"] = (payload["requested_reviewer"]["repos_url"])
#             filtered_data["reviewer_name"] = (payload["requested_reviewer"]["login"])
#             try:
#                 filtered_data["slack_user_id"] = search(filtered_data["reviewer_name"])
#             except Exception as e:
#                 filtered_data["slack_user_id"] = ''
#                 print("User not found", e)
#             filtered_data["pull_request_url"] = (payload["pull_request"]["html_url"])
#             filtered_data["user"] = (payload["pull_request"]["user"]["login"])
#             filtered_data["user_url"] = (payload["pull_request"]["user"]["html_url"])
#             filtered_data["pull_request_number"] = (payload["pull_request"]["number"])
#             filtered_data["pull_request_title"] = (payload["pull_request"]["title"])
#             filtered_data["name"] = (payload["pull_request"]["head"]["repo"]["full_name"])
#             filtered_data["tstamp"] = (payload["pull_request"]["created_at"])
#             filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
#             filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
#             assign_reviewer(filtered_data, channel)

#         if payload["action"] == "opened" or payload["action"] == "reopened" or payload["action"] == "closed":
#             action = payload["action"]
                
#             if action == "opened":
#                 filtered_data["tstamp"] = (payload["pull_request"]["created_at"])
#                 filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
#                 filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
#             elif action == "reopened":
#                 filtered_data["tstamp"] = (payload["pull_request"]["updated_at"])
#                 filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
#                 filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)
#             else:
#                 filtered_data["tstamp"] = (payload["pull_request"]["closed_at"])
#                 filtered_data["tstamp"] = datetime.strptime(filtered_data["tstamp"], '%Y-%m-%dT%H:%M:%SZ')
#                 filtered_data["tstamp"] = int(filtered_data["tstamp"].timestamp() * 1000)

#             filtered_data["action"] = payload["action"]
#             filtered_data["pull_request_url"] = (payload["pull_request"]["html_url"])
#             filtered_data["pull_request_number"] = (payload["pull_request"]["number"])
#             filtered_data["pull_request_title"] = (payload["pull_request"]["title"])
#             filtered_data["user"] = (payload["pull_request"]["user"]["login"])
#             filtered_data["body"] = (payload["pull_request"]["body"])
#             filtered_data["user_url"] = (payload["pull_request"]["user"]["html_url"])
#             filtered_data["user_avatar_url"] = (payload["pull_request"]["user"]["avatar_url"])
#             filtered_data["name"] = (payload["pull_request"]["head"]["repo"]["full_name"])

#             push_message(filtered_data, channel)

