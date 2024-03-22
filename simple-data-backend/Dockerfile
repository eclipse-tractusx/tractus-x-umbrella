# Copyright (c) 2022,2024: Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# Copyright (c) 2021,2024 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0. *
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# * SPDX-License-Identifier: Apache-2.0

# Dependencies
FROM maven:3-eclipse-temurin-21-alpine AS maven
ARG BUILD_TARGET=simple-data-backend

WORKDIR /build

COPY . .

# the --mount option requires BuildKit.
RUN --mount=type=cache,target=/root/.m2 mvn -B clean package -am -DskipTests


# Copy the jar and build image
FROM eclipse-temurin:21-jre-alpine AS simple-data-backend

ARG UID=10000
ARG GID=3000

WORKDIR /app

COPY --chmod=755 --from=maven /build/target/simple-data-backend*.jar app.jar

USER ${UID}:${GID}

ENTRYPOINT ["java", "-jar", "app.jar"]
