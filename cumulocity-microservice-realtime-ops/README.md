## About

A simple cumulocity microservice that listens to all operations on a tenant it is subscribed to and logs them.

## How to run

1. [Create your microservice application](https://cumulocity.com/guides/microservice-sdk/java/#create-the-application)
2. [Obtain your bootstrap credentials](https://cumulocity.com/guides/microservice-sdk/java/#acquire-the-microservice-bootstrap-user).
3. Put the bootstrap credentials in [application-dev.properties](src/main/resources/application-dev.properties#L10-L13)
4. Build the microservice: `mvn clean install`
5. Run the microservice: `mvn spring-boot:run `
