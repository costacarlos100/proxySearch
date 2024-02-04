import socket
import time
import urllib

import requests

global firstProxy, proxiesOk
firstProxy = False
proxiesOk = []
proxiesFalse = []

def buscaProxys():
    time.sleep(5)
    response = requests.get("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies")
    proxys = response.text
    proxys = proxys.split("\r")
    dicionario = {}
    voltas: int = 0
    for proxy in proxys:
        if voltas != 80:
            proxy = proxy.replace("\n", "")
            separado = proxy.split(":")
            dicionario[separado[0]] = separado[1]
            voltas = voltas + 1
        else:
            break
    return dicionario

def verificaProxy(host, porta):
    proxy = host+":"+porta
    proxy_support = urllib.request.ProxyHandler({'http': f'http://{proxy}'})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    try:
        if proxy in proxiesOk:
            pass
        else:
            response = urllib.request.urlopen('http://testphp.vulnweb.com/login.php')
            print(f'O proxy {proxy} está funcionando corretamente')
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            proxiesOk.append(proxy)
    except Exception as e:
        if proxy in proxiesFalse:
            pass
        else:
            proxiesFalse.append(proxy)
        pass

def main(firstProxy):
    volta = 0
    proxies = buscaProxys()
    while volta < 1:
        for chave, valor in proxies.items():
            try:
                first = f"{chave}:{valor}"
            except:
                print(" ")
            if firstProxy == False:
                firstProxy = f'{chave}:{valor}'
                first = firstProxy
                verificaProxy(chave, valor)
                pass
            elif firstProxy == f'{chave}:{valor}':
                proxies = buscaProxys()
                firstProxy = False
                pass
            elif firstProxy != first:
                verificaProxy(chave, valor)
                pass
            else:
                proxies = buscaProxys()


print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
main(firstProxy)
