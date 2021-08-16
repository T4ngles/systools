"""
    ip tools
    to add:
        -
        -udp firewall hole punching comms
"""

import urllib.request

def find_pub_ip():    
    #curl ifconfig.co
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip

def func2():
    pass

def main():
    print(find_pub_ip())

if __name__ == '__main__':
    main()