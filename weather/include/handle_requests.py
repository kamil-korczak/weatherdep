import requests


class HandleRequests:

    @classmethod
    def get(cls, url):
        try:
            # TODO handle weather_data.status_code
            # for example status_code=502

            return requests.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
        except ConnectionError:
            print("ConnectionError")
            return False
