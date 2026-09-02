
def check_network_issue(symptom, evidence):
    text = f"{symptom} {evidence}".lower()
    rules = [
        (["vlan 20", "fa0/1", "vlan 10"], "Wrong VLAN Assignment", .95),
        (["not listed", "vlan 10"], "VLAN Not Created", .95),
        (["not in the allowed vlan", "vlan 10"], "VLAN Missing on Trunk", .95),
        (["administratively down"], "Switch Port Shutdown", .90),
        (["wrong default gateway"], "Wrong Default Gateway", .94),
        (["255.255.0.0", "255.255.255.0"], "Wrong Subnet Mask", .94),
        (["different mac", "same ip"], "Duplicate IP Address", .96),
        (["192.168.20.10", "192.168.10.0"], "Wrong Static IP Address", .93),
        (["apipa", "dhcp", "absent"], "DHCP Pool Missing", .95),
        (["0 available addresses"], "DHCP Pool Exhausted", .96),
        (["nxdomain"], "Missing DNS Record", .94),
        (["dns server", "unreachable"], "DNS Server Unreachable", .95),
        (["no route", "remote"], "Missing Static Route", .94),
        (["incorrect next hop"], "Wrong Static Route Next Hop", .94),
        (["not included", "routing protocol"], "Missing Dynamic Routing Network", .92),
        (["deny", "acl"], "ACL Blocking Traffic", .95),
        (["wrong interface", "acl"], "ACL Applied to Wrong Interface", .92),
        (["wrong direction", "acl"], "ACL Wrong Direction", .92),
        (["nat inside", "missing"], "NAT Inside Missing", .94),
        (["nat outside", "missing"], "NAT Outside Missing", .94),
        (["nat acl", "does not permit"], "NAT ACL Does Not Include Network", .93),
        (["ssid", "does not match"], "Wrong Wireless SSID", .91),
        (["security key", "does not match"], "Wrong Wireless Password", .91),
        (["wireless", "wrong vlan"], "Wireless Client in Wrong VLAN", .92),
        (["access point", "uplink", "down"], "Access Point Uplink Down", .94),
        (["wireless", "169.254"], "Wireless DHCP Failure", .94),
    ]
    for keywords, fault, confidence in rules:
        if all(k in text for k in keywords):
            return {"root_cause": fault, "confidence": confidence}
    return {"root_cause": "Insufficient evidence for a confident diagnosis", "confidence": .40}
