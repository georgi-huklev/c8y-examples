## Generate Certificates

#### 1. Create a Self-Signed Root CA

```commandline
openssl req -x509 -sha256 -nodes -days 1825 -newkey rsa:2048 -keyout rootCA.key -out rootCA.crt
```

#### 2. Upload the generated root certificate to Cumulocity
Documentation can be found [here](https://cumulocity.com/guides/users-guide/device-management/#trusted-certificates).

#### 3. Create private key and a certificate signing request for the device

```commandline
openssl req -newkey rsa:2048 -nodes -keyout device.key -out device.csr
```
Note: The CN of the device certificate must match the MQTT Client ID.

#### 4. Sign the device CSR with the Root CA

```commandline
openssl x509 -req -CA rootCA.crt -CAkey rootCA.key -in device.csr -out device.crt -days 365 -CAcreateserial -extfile device.ext
```

#### 5. Save device chain to a file

```commandline
cat device.crt rootCA.crt > device_chain.crt
```

#### 6. Fetch server certificates

```commandline
openssl s_client -showcerts -verify 5 -connect {domain}:443 < /dev/null > {domain}.cer
```
 * **{domain}** - the domain of the mqtt server(e.g. cumulocity.com, us.cumulocity.com, eu-latest.cumulocity.com, etc.)

## Troubleshooting

#### Inspect certificates

```commandline
openssl x509 -text -noout -in device.crt
```


