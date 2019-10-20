from requests import get, ConnectTimeout, ConnectionError, HTTPError, ReadTimeout


def call_service(pilot_name):
    try:
        r = get("http://roa.services.seldonlabs.com/?pattern={}".format(pilot_name), timeout=5)

        r.raise_for_status()

        return r.json()

    except ReadTimeout:
        return "Timeout Error"
    except ConnectTimeout:
        return "Connection Timeout"
    except HTTPError:
        return "Bad Request"
    except ConnectionError:
        return "Connection Error"
