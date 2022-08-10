## About

A python script demonstrating programmatic authentication using TOTP in Cumulocity IoT. 

## Requirements
1. [python 3.9](https://www.python.org/downloads/release/python-3913/)
2. [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

## How to run

1. Install dependencies: `pipenv sync`
2. Create a user in your tenant with TOTP Authenthication enabled
3. Login once with the created user and go through the TOTP setup. Note the TOTP secret under the QR code.
4. Open [main.py](main.py#L10-L14):
   1. Set the `domain` to your Cumulocity IoT domain
   2. Set the `tenant` to the ID of you Cumulocity IoT tenant
   3. Set the `user` to the username of your user
   4. Set the `pw` to the password of your user
   5. Set the `totp_secret` to match the secret obtained during TOTP setup (3.)
5. Run the script: `pipenv run python main.py`

## Troubleshooting
HTTP requests are logged when `log_level` is set to `logging.DEBUG`