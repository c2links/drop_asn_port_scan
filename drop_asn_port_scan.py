import requests
import json
import ipaddress
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(filename='asnPortScan.log', filemode='w', level =  logging.INFO , format='%(name)s - %(levelname)s - %(message)s')

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

def cleanOutput(scanout):
    final = []

    for record in scanout:
        record = json.loads(record)
        for k,v in record.items():
            if k == "scan":
                print(vv)
                for kk,vv in v.items():
                    final.append(dict(ip=kk,ports=vv))
    return final

def main():

    logging.info(f"Started at {datetime.now()}")
    scanout = []

    ASNLIST = getDropASN()
    logging.info(f"Found {len(ASNLIST)} ASN's from the drop list")
    IPRANGES = asn2range(ASNLIST)
    logging.info(f"Found {len(IPRANGES)} IP prefixes")
    IPS = iprange2ips(IPRANGES)
    logging.info(f"Found {len(IPS)} IP Addresses")
    logging.info("Writing IP addresses to file\n")

    with open(f"in/ip_addresses.txt","w") as oF:
        for ip in IPS:
            oF.write(f"{ip}\n")

    logging.info(f"Finished at {datetime.now()}\n")

if __name__ == "__main__":
    main()