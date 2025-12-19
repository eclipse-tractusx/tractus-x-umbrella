# Dependencies between Services




## Three Layer deployment

### Layer 1: Shared Services

``` mermaid
flowchart TB 

  s((start)) --> IDP

  subgraph ss [Shared Services]
    IDP --> Portal
    IDP --> MIW
    IDP --> DiscoveryServices
    IDP --> SemanticHub
    IDP --> GDPM
  end
 
  

```

Indication for relevant components: [Portal Data Flow Diagram](https://github.com/eclipse-tractusx/portal-assets/blob/main/docs/developer/Technical%20Documentation/Architecture/Security-Assessment.md#data-flow-diagram)

### Layer 2: Industry Core

``` mermaid
flowchart TD 
  s((start)) --> industry

  subgraph industry [Industry Core]

    subgraph DP1
      EDC --> Registry
      Registry --> SubmodelServer
    end
    
    subgraph DP2
      direction LR
      EDC2 --> Registry2
      Registry2 --> SubmodelServer2
    end

    subgraph DP3
      direction LR
      EDC3 --> Registry3
      Registry3 --> SubmodelServer3
    end
  end
```

### Layer 3: UseCases 

``` mermaid
flowchart TD
  s((start)) --> usecases

  subgraph usecases [Use Cases]
      direction LR
    subgraph TraceXA
      direction LR
      EDCA(EDC)
      EDCA2(EDC Notification)
      RegistryA(Registry)
      SubmodelServerA(Submodel Server)
      Trace-XA(Trace-X A)
      IRSA(IRS)
    end
    
    subgraph TraceXB
      direction LR
      EDCB(EDC)
      EDCB2(EDC Notification)
      RegistryB(Registry)
      SubmodelServerB(Submodel Server)
      Trace-XB(Trace-X B)
      IRSB(IRS)
    end

    TraceXA -->TraceXB
  end
```

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>

