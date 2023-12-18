from pushbullet import PushBullet
from apikeys import access_token_pushbullet


def notify(message,title="Unwrapped"):
    pb = PushBullet(access_token_pushbullet)
    push = pb.push_note(title,message)