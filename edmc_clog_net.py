from requests import get, ConnectTimeout, ConnectionError, HTTPError, ReadTimeout

from edmc_clog_utils import APP_VER

def call_service(pilot_name):
    try:
        r = get(f"http://roa.services.seldonlabs.com/?pattern={pilot_name}", headers={
          'User-Agent': f"EDMC-CLog-v-{APP_VER}"
        }, timeout=5)

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
