import json
import logging
import ssl
import time

import paho.mqtt.client as mqtt
import requests

# Configuration
domain: str = 'georgi.latest.stage.c8y.io'
client_id: str = 'my-cert-mqtt-device'  # Must be identical to the CN of the device certificate
client_cert: str = 'certs/device_chain.crt'
client_key: str = 'certs/device.key'
ca_cert: str = 'certs/latest.stage.c8y.io.cer'
log_level: int = logging.INFO

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(log_level)
handler: logging.Handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)7s - %(filename)s:%(lineno)d - %(message)s'))
handler.setLevel(log_level)
log.addHandler(handler)

jwt_token: str = ""


def on_connect(client, userdata, flags, rc: int) -> None:
    log.info(f'Connected with result code:{rc}')
    log.debug(f'flags:{flags}, userdata:{userdata}')

    client.subscribe('s/e', 0)  # Error reporting
    client.subscribe('s/dat', 0)  # JWT


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
    message: str = msg.payload.decode()
    log.log(logging.WARN if msg.topic == 's/e' else logging.DEBUG,
            f'Message received: {msg.topic} {msg.payload.decode()}')
    log.debug(f'userdata: {userdata}')

    if msg.topic == 's/dat' and message.startswith('71,'):  # Persist JWT token
        global jwt_token
        jwt_token = message.split(',')[1]
        log.info(f'JWT token received: f{jwt_token}')


def formatted_request_response(resp: requests.Response) -> str:
    return \
        f'' \
        f'REQUEST:\n' \
        f'{resp.request.method} {resp.request.url}\n' \
        f'{json.dumps(dict(resp.request.headers), indent=2)}\n' \
        f'RESPONSE: {resp.status_code}\n' \
        f'{resp.headers}\n' \
        f'{json.dumps(resp.json(), indent=2) if resp.headers["content-type"].find("json") >= 0 else resp.content}'


if __name__ == '__main__':
    mqtt_client: mqtt.Client = mqtt.Client(client_id)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set(ca_cert,
                        certfile=client_cert,
                        keyfile=client_key,
                        tls_version=ssl.PROTOCOL_TLSv1_2,
                        cert_reqs=ssl.CERT_NONE)
    mqtt_client.connect(domain, 8883, 60)

    mqtt_client.loop_start()

    while True:
        while not jwt_token:
            log.info('Fetching JWT token')
            mqtt_client.publish('s/uat', '500')  # Request JWT
            time.sleep(1)

        resp: requests.Response = requests.get(
            f'https://{domain}/user/currentUser',
            headers={
                'Authorization': f'Bearer {jwt_token}',
                'Accept': 'application/json'
            }
        )
        log.debug(formatted_request_response(resp))
        if resp.status_code / 100 == 2:
            log.info(f'Current user: {resp.json()["id"]}')
        elif resp.status_code == 401:
            log.info('Token expired')
            jwt_token = ""
        else:
            log.error(f'Unexpected response:{resp.status_code}')
        time.sleep(60)
