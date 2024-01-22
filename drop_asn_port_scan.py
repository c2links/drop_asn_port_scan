import requests
import json
import ipaddress
import pandas as pd
import masscan

# Description: Saves ASN and RIR from the Spamhaus ASN Drop list from https://www.spamhaus.org/drop/asndrop.json
# Input: None
# Output: List of dictionary object of the ASN and RIR [{asn:ASxxxx,rir:xxxxx}]

def getDropASN():
    asnList = []
    res = requests.get("https://www.spamhaus.org/drop/asndrop.json")
    asndrop = res.content.splitlines()

    for asn in asndrop:
        asn = json.loads(asn)
        try:
            asnList.append(dict(asn=asn['asn'],rir=asn['rir']))
        except KeyError:
            pass
    return asnList

# Description: Finds the IP prefixes (ranges) for the supplied ASNs. Uses the RIPE database and Hurricane Electric
# Input: List of ASN Dictionary objects [{asn:ASxxxx,rir:xxxxx}]
# Output: List of IP Ranges in the form 103.73.188.0/23

def asn2range(asnList):

    ipranges = []

    for asn in asnList:
        if asn['rir'] == 'ripencc':
            res = requests.get(f'https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn["asn"]}')
            record = json.loads(res.text)
            for prefix in record["data"]["prefixes"]:
                ipranges.append(prefix["prefix"])
        else:
            tables = pd.read_html(f"https://bgp.he.net/AS{asn['asn']}#_prefixes")
            for table in tables:
                try:
                    temp = table.Prefix
                    jsonObject = table.to_dict()
                    for k,v in jsonObject['Prefix'].items():
                        ipranges.append(v)
                except AttributeError:
                    pass
    return ipranges

# Description: Expands a IP Range to its IP Addresses
# Input: List of IP Ranges in the form 103.73.188.0/23
# Output: List of IP Addresses

def iprange2ips(ipRanges):
    ips = []
    for iprange in ipRanges:
        try:
            for ip in ipaddress.IPv4Network(iprange):
                ips.append(ip)
        except Exception as e:
            print(e)
    return ips

def main():
    ASNLIST = getDropASN()
    print(f"Found {len(ASNLIST)} ASN's from the drop list")
    IPRANGES = asn2range(ASNLIST)
    #IPS = iprange2ips(IPRANGES)

    # Foreach ip range, run masscan to see if ports 80, 8080, 443 or 8443 are open
    for iprange in IPRANGES:
        mas = masscan.PortScanner()
        print(f"Scanning {iprange}")
        mas.scan(iprange, ports='80,8080,443,8443', arguments='--max-rate 1000')
        iprangeF = iprange.replace("/","_")
        with open(f"out/{iprangeF}","w") as oF:
            oF.write(mas.scan_result)
if __name__ == "__main__":
    main()