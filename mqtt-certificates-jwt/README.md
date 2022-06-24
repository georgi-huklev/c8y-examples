## About

A python script connecting to Cumulocity IoT over MQTT using a device 
certificate. A JWT token is fetched and continuously used to fire HTTPS 
requests. Once the JWT token expires it is automatically renewed.  

## Requirements
1. [python 3.8](https://www.python.org/downloads/release/python-3813/)
2. [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

## How to run

1. Follow the instructions in [certs/README.md](certs/README.md) to generate your certs and upload them to your Cumulocity IoT tenant.
2. Install dependencies: `pipenv sync`
3. Open [main.py](main.py#L10-L11):
   1. Change the `domain` to your Cumulocity IoT domain
   2. Change the `client_id` to the CN of your device certificate generated in step 1.
4. Run the script: `pipenv run python main.py`

## Troubleshooting
Some additional console output is provided when `log_level` is set to `logging.Debug`