from rest_framework.throttling import SimpleRateThrottle


class CustomRateThrottle(SimpleRateThrottle):
    scope = "custom"

    def allow_request(self, request, view):
        # Получаем ключ для кеширования (в данном случае, просто IP-адрес клиента)
        ident = self.get_ident(request)

        rate_str = self.get_rate()

        # Определяем скорость ограничения (10 запросов в минуту)
        rate = int(''.join(filter(str.isdigit, rate_str)))

        # Получаем ключ для кеширования с учетом идентификатора и области действия
        key = self.get_cache_key(request, view, ident, rate)

        # Получаем текущее количество запросов и время последнего запроса из кеша
        current, _ = self.cache.get(key, (0, 0))

        # Проверяем, не превышен ли лимит
        if int(current) >= rate:
            return False

        # Увеличиваем количество запросов и обновляем время последнего запроса в кеше
        self.cache.set(key, (current + 1, self.timer()), self.duration)

        return True

    def get_cache_key(self, request, view, ident, rate):
        # Возвращаем уникальный ключ для кеширования
        return f"{self.scope}:{ident}:{rate}"
