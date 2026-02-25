package org.eclipse.tractusx.simpledataservice;

import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

class SimpleDataServiceControllerTest {

    @Test
    void shouldStoreData() {
        // Arrange
        final SimpleDataServiceController simpleDataServiceController = new SimpleDataServiceController();
        final String payload = """
                {
                    "test": "data"
                }
                """;

        // Act
        simpleDataServiceController.addData("test", payload);

        // Assert
        final Object actualResponse = simpleDataServiceController.getData("test");
        assertThat(actualResponse).isEqualTo(payload);
    }

    @Test
    void shouldOverwriteData() {
        // Arrange
        final SimpleDataServiceController simpleDataServiceController = new SimpleDataServiceController();
        final String initialPayload = """
                {
                    "test": "initial"
                }
                """;
        final String updatedPayload = """
                {
                    "test": "updated"
                }
                """;

        // Act
        simpleDataServiceController.addData("test", initialPayload);
        simpleDataServiceController.addData("test", updatedPayload);

        // Assert
        final Object actualResponse = simpleDataServiceController.getData("test");
        assertThat(actualResponse).isEqualTo(updatedPayload);
    }

    @Test
    void shouldThrowNotFoundException() {
        // Arrange
        final SimpleDataServiceController simpleDataServiceController = new SimpleDataServiceController();

        // Act & Assert
        assertThatExceptionOfType(ResponseStatusException.class).isThrownBy(() -> simpleDataServiceController.getData("test"));
    }
}