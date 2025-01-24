#!/usr/bin/env python3

"""Module to extract device list in JSON from a BGP 320 router."""

try:
    from lxml import html
    import json
    import re
    import requests
    import urllib3
    import click
except ImportError:
    print("import errors, need to pip install -r requirements.txt?")

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def handle_ipaddr(key, value, d):
    """handle the IP address and name."""
    for k, v in zip(key.split("/"), value.split("/")):
        d[k.strip()] = v.strip()

def handle_cspeed(key, value, d):
    """handle the Connection Speed."""
    d[key] = value.strip().replace('\t',' ')

def handle_ctype(value, d):
    """handle the Connection Type."""
    wifiptn = re.compile(
        r"""Wi-Fi\s*(?P<Frequency>\d*[.]?\d* GHz.*)
            Type: (?P<NetworkType>Guest|Home)
            Name: (?P<NetworkName>\w+)""", re.VERBOSE)
    m = re.search(wifiptn, value)
    if m:
        gd = m.groupdict()
        gd['Type'] = 'Wi-Fi'
        d['Connection'] = gd
    else:
        d['Connection'] = value.strip()

@click.command()
@click.option('--url',
              default='https://192.168.1.254/cgi-bin/devices.ha',
              help='Your AT&T Fiber Router URL.')
def bgp320_devices(url):
    """Get the device list from the router."""
    response = requests.get(url, verify=False, timeout=5)
    s = response.content

    doc = html.fromstring(s)
    table = doc.find_class("table100")[0]
    rows = iter(table)
    alldicts = []
    rowdict = {}

    ipptn = r"IPv4 Address / Name"
    ctypeptn = r"Connection Type"
    cspeedptn = r"Connection Speed"

    for row in rows:
        value = row.xpath(".//td")
        key = row.xpath(".//th")
        if key:
            if value:
                if re.search(ipptn, key[0].text_content().strip()):
                    handle_ipaddr(key[0].text_content().strip(),
                                  value[0].text_content().strip(),
                                  rowdict)
                elif re.search(ctypeptn, key[0].text_content().strip()):
                    handle_ctype(value[0].text_content(), rowdict)
                elif re.search(cspeedptn, key[0].text_content().strip()):
                    handle_cspeed(key[0].text_content().strip(), value[0].text_content(), rowdict)
                else:
                    rowdict[key[0].text_content().strip()] = value[0].text_content().strip()
            else:
                rowdict[key[0].text_content().strip()] = ""
        else:
            alldicts.append(rowdict)
            rowdict = {}

    if rowdict:
        alldicts.append(rowdict)
    click.echo(f"{json.dumps(alldicts, indent=2)}")

if __name__ == "__main__":
    bgp320_devices()
