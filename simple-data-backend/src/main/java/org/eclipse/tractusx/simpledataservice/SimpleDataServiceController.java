/********************************************************************************
 * Copyright (c) 2022,2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
 * Copyright (c) 2021,2024 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 ********************************************************************************/
package org.eclipse.tractusx.simpledataservice;

import java.util.HashMap;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping
@Slf4j
public class SimpleDataServiceController {
    private final HashMap<String, Object> data = new HashMap<>();

    @PostMapping("/{id}")
    public void addData(@PathVariable final String id, @RequestBody final Object payload) {
        log.info("Adding data for id '{}'", id);
        data.put(id, payload);
    }

    @GetMapping({"/{id}", "/{id}/$value"})
    public Object getData(@PathVariable final String id) {
        if (data.containsKey(id)) {
            log.info("Returning data for id '{}'", id);
            return data.get(id);
        } else {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No data found with id '%s'".formatted(id));
        }
    }
}
