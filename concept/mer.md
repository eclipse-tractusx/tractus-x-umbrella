
# test

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
 
  ss --> industry

  subgraph industry
    direction RL
    subgraph dp1
      direction LR
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

  industry --> businessApp

  subgraph businessApp 
    subgraph tracexa
      trEDC
      trRegistry
      trTrace
      trEDCnotification
      trIRS
    end
  end





```