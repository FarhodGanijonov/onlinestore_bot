# bot/utils/redis_client.py
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def save_cart(user_id: int, cart_data: list):
    redis_client.setex(f"cart:{user_id}", 300, json.dumps(cart_data))  # 24 soat

def get_cart(user_id: int) -> list:
    data = redis_client.get(f"cart:{user_id}")
    return json.loads(data) if data else []

def clear_cart(user_id: int):
    redis_client.delete(f"cart:{user_id}")
