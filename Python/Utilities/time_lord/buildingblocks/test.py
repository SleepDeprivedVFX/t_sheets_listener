# import requests
#
# headers = {
#     'Content-type': 'application/json',
# }
#
#
# data = '{"blocks": [{"type": "section","text": {"type": "mrkdwn","text": "Danny Torrence left the following review' \
#        ' for your property:"}},{"type": "actions","elements": [{"type": "button","text": {"type": "plain_text","text":' \
#        ' "Find Them and Kill Them","emoji": true},"value": "click_me_123"},{"type": "button","text": {"type": ' \
#        '"plain_text","text": "Approve","emoji": true},"value": "click_me_123"}]}]}'
#
# response = requests.post('https://hooks.slack.com/services/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',
#                          headers=headers, data=data)
#
# print response
#

intersect = set(range(2000)) & set(range(1000, 3000))
print intersect

a = 10
b = 4

print(a & b)
print(a | b)
print(~a)
print(range(2000))
print(set(range(2000)))
print range(1000, 3000)