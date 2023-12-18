from pushbullet import PushBullet
from apikeys import access_token_pushbullet

from vars import usePushbullet

def notify(message,title="Unwrapped"):
    if usePushbullet:
        pb = PushBullet(access_token_pushbullet)
        push = pb.push_note(title,message)