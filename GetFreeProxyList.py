from bs4 import BeautifulSoup
import urllib
import requests
import codecs
import time
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.exceptions import ProxyError as urllib3_ProxyError

g_base_url = "https://free-proxy-list.net/"
g_proxy_file = "proxy.csv"

def write_to_csv(_ip, _port, _flag):

    fio = open(g_proxy_file, encoding='utf-8', mode="a")
    write_text =  _ip + ":"
    write_text += _port + ","
    write_text += _flag + "\n"
    print(write_text)
    fio.write(write_text)
    fio.close()

try:
    session = requests.Session()
    result = session.get(g_base_url)
    soup = BeautifulSoup(result.content, 'html.parser')
    table_arr = soup.select('table#proxylisttable')
    if len(table_arr) > 0:
        table_tbody_arr = table_arr[0].select('tbody')
        if len(table_tbody_arr) > 0:
            table_tbody = table_tbody_arr[0]
            tr_arr = table_tbody.select('tr')
            print("-:proxy count", len(tr_arr))
            for tr_body in tr_arr:
                td_arr = tr_body.select('td')
                if len(td_arr) == 8:
                    _proxy_ip = td_arr[0].text
                    _proxy_port = td_arr[1].text
                    _proxy_flag = "N"
                    if td_arr[6].text == "yes":
                        _proxy_flag = "Y"

                    write_to_csv(_proxy_ip, _proxy_port, _proxy_flag)
except ConnectionError as ce:
    if (isinstance(ce.args[0], MaxRetryError) and isinstance(ce.args[0].reason, urllib3_ProxyError)):
        print("unable to connect.")

