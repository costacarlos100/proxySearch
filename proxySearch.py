import urllib.request
import socket
import urllib.error
import asyncio
import json
import telegram
import requests

# Inicializa o bot
bot = telegram.Bot(token='TOKEN_DO_BOT')

async def enviar_mensagem(texto):
    chat_id = 'ID_DO_SEU_GRUPO'
    #Caso tenha um tópico especifico, informar o id aqui
    topic_id = 'ID_DO_TÓPICO'
    mensagem = texto
    #Envia mensagem para um tópico
    await bot.send_message(chat_id=chat_id, text=mensagem, message_thread_id=topic_id)
    #Envia mensagem para o grupo 
    #await bot.send_message(chat_id, mensagem)

def buscaProxys():
    #asyncio.run(enviar_mensagem("🔎 BUSCANDO NOVOS PROXYS 🔍"))
    response = requests.get("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies")
    proxys = response.text
    proxys = proxys.split("\r")
    dicionario = {}
    voltas: int = 0
    for proxy in proxys:
        if voltas != 400:
            proxy = proxy.replace("\n", "")
            separado = proxy.split(":")
            dicionario[separado[0]] = separado[1]
            voltas = voltas + 1
        else:
            break
    return dicionario
def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'https': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('https://httpbin.org/ip')  # change the URL to test here
        sock=urllib.request.urlopen(req)
        print(sock.read())
    except urllib.error.HTTPError as e:
        #print('Error code: ')
        return e.code
    except Exception as detail:
        #print("ERROR:")
        return True
    return False

def main(proxyList):
    socket.setdefaulttimeout(120)
    for currentProxy in proxyList:
        if proxyTest(currentProxy):
            print("❌ Proxy off: %s" % (currentProxy))
        else:
            print("✅ %s está funcionando" % (currentProxy))
            host = currentProxy.split(":")
            localizaIp = requests.get(f"http://ip-api.com/json/{host[0]}")
            localizacao = localizaIp.json()
            mensagem = f"PROXY HTTPs ✅\n🗺️ PAÍS: {localizacao['country']}\n🌆 CIDADE: {localizacao['city']}\n🛜 PROVEDOR: {localizacao['org']}\n🌐 IP: {host[0]}\n🚪 PORTA: {host[1]}"
            asyncio.run(enviar_mensagem(mensagem))

if __name__ == '__main__':
    proxies = buscaProxys()
    proxy = []
    for chave, valor in proxies.items():
        proxy.append(chave+":"+valor)

    main(proxy)