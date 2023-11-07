from apiflask import APIFlask
from redis import Redis

redis = Redis(host="redis", port=6379, db=5, charset="utf-8", decode_responses=True)

app = APIFlask(import_name="web-app")

ALARM_MEMORY_VALUE = 2500000


