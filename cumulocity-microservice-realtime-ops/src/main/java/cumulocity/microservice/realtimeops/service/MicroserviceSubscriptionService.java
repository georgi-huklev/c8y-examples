package cumulocity.microservice.realtimeops.service;

import com.cumulocity.microservice.context.ContextService;
import com.cumulocity.microservice.context.credentials.MicroserviceCredentials;
import com.cumulocity.microservice.subscription.model.MicroserviceSubscriptionAddedEvent;
import com.cumulocity.model.idtype.GId;
import com.cumulocity.rest.representation.operation.OperationRepresentation;
import com.cumulocity.sdk.client.notification.Subscriber;
import com.cumulocity.sdk.client.notification.Subscription;
import com.cumulocity.sdk.client.notification.SubscriptionListener;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor(onConstructor_ = @Autowired)
public class MicroserviceSubscriptionService {

    private final ContextService<MicroserviceCredentials> contextService;
    private final Subscriber<GId, OperationRepresentation> subscriber;

    @EventListener(MicroserviceSubscriptionAddedEvent.class)
    public void microserviceSubscribed(MicroserviceSubscriptionAddedEvent event) {
        log.info("Subscribing to all operations for tenant {}", event.getCredentials().getTenant());
        contextService.runWithinContext(event.getCredentials(), () -> {
            subscriber.subscribe(GId.asGId("123"), new SubscriptionListener<GId, OperationRepresentation>() {
                @Override
                public void onNotification(Subscription<GId> subscription, OperationRepresentation operationRepresentation) {
                    log.info("New operation notification {}", operationRepresentation);
                }

                @Override
                public void onError(Subscription<GId> subscription, Throwable throwable) {
                    log.error("Subscription error", throwable);
                }
            });
        });
    }

}
