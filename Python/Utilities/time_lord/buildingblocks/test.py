import requests

headers = {
    'Content-type': 'application/json',
}


data = '{"blocks": [{"type": "section","text": {"type": "mrkdwn","text": "Danny Torrence left the following review' \
       ' for your property:"}},{"type": "actions","elements": [{"type": "button","text": {"type": "plain_text","text":' \
       ' "Find Them and Kill Them","emoji": true},"value": "click_me_123"},{"type": "button","text": {"type": ' \
       '"plain_text","text": "Approve","emoji": true},"value": "click_me_123"}]}]}'

response = requests.post('https://hooks.slack.com/services/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',
                         headers=headers, data=data)

print response

