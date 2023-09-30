from twilio.rest import Client

account_sid = 'ACd21d6fd8b5835d77e6075545ccb1cafd'
auth_token = '947e68b4049c7a1f8dfdb31202bfc9e5'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+19092740982',
  to='+12268999842'
)

print(message.sid)
