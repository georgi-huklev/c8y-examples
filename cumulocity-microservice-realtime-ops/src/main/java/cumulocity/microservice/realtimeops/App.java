package cumulocity.microservice.realtimeops;

import com.cumulocity.microservice.autoconfigure.MicroserviceApplication;
import com.cumulocity.model.idtype.GId;
import com.cumulocity.rest.representation.operation.OperationRepresentation;
import com.cumulocity.sdk.client.PlatformParameters;
import com.cumulocity.sdk.client.notification.Subscriber;
import com.cumulocity.sdk.client.notification.SubscriberBuilder;
import org.springframework.boot.SpringApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@MicroserviceApplication
public class App {
    public static void main (String[] args) {
        SpringApplication.run(App.class, args);
    }

    @Bean
    public Subscriber<GId, OperationRepresentation> allOperationsSubscriber(PlatformParameters parameters) {
        return SubscriberBuilder.<GId, OperationRepresentation>anSubscriber()
                .withEndpoint("/notification/realtime")
                .withSubscriptionNameResolver(gId -> "/operations/*")
                .withParameters(parameters)
                .withDataType(OperationRepresentation.class)
                .withMessageDeliveryAcknowlage(true)
                .build();
    }
}