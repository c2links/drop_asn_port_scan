# Drop ASN List Port Scans

This Python script pulls the bad ASNs from Spamhaus drop list (https://www.spamhaus.org/drop/asndrop.json), gets the IP prefixes for each ASN and then exapands the prefixes to IP addresses. The IP addresses are saved to a file that is then used for a Masscan command.

The IP prefixes are collected using Hurricane Electric Internet Services (bgp.he.net) and the RIPE NCC database (https://stat.ripe.net).


# Setup

```
apt-get install masscan
git clone https://github.com/c2links/drop_asn_port_scan.git
cd drop_asn_port_scan
pip3 install -r requirements.txt
```

# Run

```
python3 drop_asn_port_scan.py

```
<b>Depending on your system, you may have to run the script at a root / system level in order for Masscan to work. </b>

# Output

Results are sent to the <i>'out'</i> folder, and overwrite the file, <i>'asn_port_scan.json'</i>. A sample output is below.

```
{"command_line": "masscan -oJ - 194.36.175.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 5.105.75.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 5.105.128.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 23.27.250.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 23.230.223.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 46.34.44.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 63.161.22.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 80.71.237.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
{"command_line": "masscan -oJ - 85.133.166.0/24 -p 80,8080,443,8443 --max-rate 10000", "scan": {}}
```

# Logging

Log data will be saved to a file named <i>asnPortScan.log</i>

```
root - INFO - Started at 2024-01-23 09:52:28.791409
root - INFO - Found 186 ASN's from the drop list
root - INFO - Found 2301 IP prefixes
...
root - INFO - Finished at 2024-01-23 09:56:40.980295
```



