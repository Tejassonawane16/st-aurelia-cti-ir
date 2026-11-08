# Network diagram (owner: Arjun)

GitHub renders this Mermaid diagram automatically. For the report, export it as a PNG from https://mermaid.live, or redraw it in draw.io.

```mermaid
flowchart LR
    Internet((Internet))
    subgraph DMZ["DMZ"]
        VPN["VPN gateway<br/>MFA: admins only"]
        Portal["Patient portal"]
    end
    subgraph ADMIN["Admin network (VLAN 20)"]
        WS["Admin workstations<br/>(lab: ws-admin01)"]
        DC["Domain controllers<br/>Active Directory"]
    end
    subgraph CLIN["Clinical network (VLAN 30)"]
        EHR["EHR server<br/>(lab: ehr-srv01)"]
        PACS["PACS"]
        LIS["Lab interface"]
    end
    subgraph IOMT["IoMT network (VLAN 40)"]
        Pumps["Infusion pumps, monitors"]
    end
    subgraph SEC["Security"]
        SIEM["Wazuh SIEM<br/>(lab: wazuh-mgr)"]
        BK["Backup NAS"]
    end
    Vendor["Vendors x14"]
    Internet --> VPN
    Internet --> Portal
    Vendor --> VPN
    VPN --> WS
    VPN --> EHR
    WS --> DC
    WS -->|"weak: any-to-any allowed"| EHR
    EHR --> PACS
    EHR --> LIS
    CLIN --> IOMT
    WS -.logs.-> SIEM
    EHR -.logs.-> SIEM
    EHR --> BK
```

**Deliberate weaknesses.** The incident and the lessons learned in chapter 8 rely on these:

1. The VPN requires MFA only for IT admins.
2. The admin network can reach the EHR on any port.
3. The backup NAS is joined to the domain and reachable from the admin network.
4. The SIEM is monitored only during office hours.
