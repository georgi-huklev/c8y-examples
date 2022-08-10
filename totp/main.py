import json
import logging
from base64 import b64encode

import mintotp
import requests
from requests.cookies import RequestsCookieJar

# Configuration
domain: str = 'mytenant.cumulocity.com'
tenant: str = 't12345'
user: str = 'user'
pw: str = 'pw'
totp_secret: str = 'NLQRMLG6APZO4A7Z'
log_level: int = logging.INFO

auth: str = b64encode(f'{user}:{pw}'.encode()).decode()
log: logging.Logger = logging.getLogger(__name__)
log.setLevel(log_level)
handler: logging.Handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)7s - %(filename)s:%(lineno)d - %(message)s'))
handler.setLevel(log_level)
log.addHandler(handler)


def formatted_request_response(resp: requests.Response) -> str:
    return \
        f'' \
        f'REQUEST:\n' \
        f'{resp.request.method} {resp.request.url}\n' \
        f'{json.dumps(dict(resp.request.headers), indent=2)}\n' \
        f'{resp.request.body}\n' \
        f'RESPONSE: {resp.status_code}\n' \
        f'{resp.headers}\n' \
        f'{json.dumps(resp.json(), indent=2) if resp.content and resp.headers.get("content-type") and resp.headers["content-type"].find("json") >= 0 else resp.content}'


def get_auth_cookies() -> RequestsCookieJar:
    headers: dict = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    payload: str = f'grant_type=PASSWORD&username={user}&password={pw}&tfa_code={mintotp.totp(totp_secret)}'
    resp: requests.Response = requests.post(f'https://{domain}/tenant/oauth?tenant_id={tenant}', headers=headers,
                                            data=payload)
    log.debug(formatted_request_response(resp))
    return resp.cookies


def get_current_user(cookies: RequestsCookieJar) -> None:
    resp: requests.Response = requests.get(f'https://{domain}/user/currentUser', cookies=cookies,
                                           headers={'X-XSRF-TOKEN': cookies.get('XSRF-TOKEN')})
    log.debug(formatted_request_response(resp))


if __name__ == '__main__':
    log.info("Getting auth cookies")
    cookies: RequestsCookieJar = get_auth_cookies()
    log.info("Getting current user")
    get_current_user(cookies)
