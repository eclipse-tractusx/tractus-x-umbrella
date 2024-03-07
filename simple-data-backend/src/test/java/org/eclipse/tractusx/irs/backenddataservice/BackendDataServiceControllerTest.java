package org.eclipse.tractusx.irs.backenddataservice;

import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

class BackendDataServiceControllerTest {

    @Test
    void shouldStoreData() {
        // Arrange
        final BackendDataServiceController backendDataServiceController = new BackendDataServiceController();
        final String payload = """
                {
                    "test": "data"
                }
                """;

        // Act
        backendDataServiceController.addData("test", payload);

        // Assert
        final Object actualResponse = backendDataServiceController.getData("test");
        assertThat(actualResponse).isEqualTo(payload);
    }

    @Test
    void shouldThrowNotFoundException() {
        // Arrange
        final BackendDataServiceController backendDataServiceController = new BackendDataServiceController();

        // Act & Assert
        assertThatExceptionOfType(ResponseStatusException.class).isThrownBy(() -> backendDataServiceController.getData("test"));
    }
}