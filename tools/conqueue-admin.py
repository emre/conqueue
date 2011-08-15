import redis

redis_connection = redis.Redis(host = 'localhost', port= 6379, db= 0)

# remember that it's blocking
# a proper frontend for monitoring/administration
# is planned for the future.
keys = redis_connection.keys("conqueue:*")

keys = sorted(keys)
for key in keys:
    print key, redis_connection.llen(key)