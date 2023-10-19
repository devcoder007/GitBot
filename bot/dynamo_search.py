import boto3

session = boto3.Session()
dynamodb = session.client('dynamodb',region_name='us-west-2')
tableName = "slack--user"


def search():
    response = dynamodb.get_item(
    Key={
    'GithubUserID': {
        'S': "shrikant1212",
    }
    },
    TableName=tableName,
    )

    return (response['Item']['SlackUserID']['S'])
 