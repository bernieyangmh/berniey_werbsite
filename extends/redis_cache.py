# coding: utf-8

import tornadis
import tornado.gen

from config import redis_cache_config


class RedisCacheManager(object):

    def __init__(self, options):
        self.redis_connection_pool = None
        self.redis_client = None

    def get_connection_pool(self):
        if not self.redis_connection_pool:
            self.redis_connection_pool = tornadis.ClientPool(
                host=redis_cache_config['host'], port=redis_cache_config['port'],
                max_size=redis_cache_config['max_size'], client_timeout=redis_cache_config['client_timeout'])
        return self.redis_connection_pool

    @tornado.gen.coroutine
    def get_redis_client(self):
        redis_connection_pool = self.get_connection_pool()
        with (yield redis_connection_pool.connected_client()) as redis_client:
            if isinstance(redis_client, tornadis.TornadisException):
                print (redis_client.message)
            else:
                raise tornado.gen.Return(redis_client)
        self.redis_client = yield self.get_redis_client()

