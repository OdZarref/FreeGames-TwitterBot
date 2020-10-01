import requests
import tweepy
import os
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
from time import sleep
from tokens import *

class ProcurarFreeSteamKeys():
    def __init__(self):
        def logProjeto(self, textoLog):
            with open('bot_log.txt', 'a') as log:
                log.write(textoLog)

        def pegarUltimoVistoFreeSteamKeys(self):
            with open('ultimovisto_freesteamkeys.txt') as arquivo:
                return arquivo.read()

        def atualizarUltimoVistoFreeSteamKeys(self, ultimoVisto):
            with open('ultimovisto_freesteamkeys.txt', 'w') as arquivo:
                arquivo.write(ultimoVisto)

        def acessarPaginaDoJogo(url):
            paginaDoJogo = requests.get(url)
            paginaDoJogoSopa = BeautifulSoup(paginaDoJogo.text, 'html.parser')
            ancora = paginaDoJogoSopa.find('a', class_='zf-edit-button')
            botaoJogo = paginaDoJogoSopa.find('a', class_='item-url custom_link_button')

            if ancora.get('href')[7:] in botaoJogo.get('onclick'):
                logProjeto(self, f'JOGO STEAM! + {ancora.get("href")}' + '\n')

        self.pagina = requests.get('https://www.freesteamkeys.com/')
        self.sopa = BeautifulSoup(self.pagina.text, 'html.parser')
        self.articles = self.sopa.find(id='post-items')

        for contador, article in enumerate(self.articles, start=0):
            divPostThumbnail = article.find(class_='post-thumbnail')
            try:
                if article.get('id') == pegarUltimoVistoFreeSteamKeys(self):
                    break

                if not divPostThumbnail.find('div', class_='expire_stamp'):
                    print(divPostThumbnail.find('a').get('href'))
                    acessarPaginaDoJogo(divPostThumbnail.find('a').get('href'))
            except: 
                pass

            if contador == 1:
                print('ISTO OCORREU')
                atualizarUltimoVistoFreeSteamKeys(self, article.get('id'))

class SeleniumBusca:
    def __init__(self):
        if os.name == 'nt':
            self.browser = Firefox(executable_path='./webdrivers/geckodriver.exe')
        else:
            self.browser = Firefox(executable_path='./webdrivers/geckodriver')

    def epicGamesStore(self):
        self.browser.get('https://www.epicgames.com/store/pt-BR/free-games')
        elementos = self.browser.find_elements_by_xpath('//div[@data-component="CardGridDesktopBase"]')
        jogos = list()
        jogosGratis = list()

        for elemento in elementos: jogos.append(elemento.find_element_by_tag_name('a').get_attribute('href'))

        for jogo in jogos:
            self.browser.get(jogo)

            try:
                botoes = self.browser.find_elements_by_tag_name('button')

                for botao in botoes:
                    if 'continuar' in botao.text.lower():
                        botao.click()
            except:
                pass
            
            try:
                def verificarJogoNaLista(self, jogo):
                    gamesLista = open('games_list.txt')

                    for linha in gamesLista:
                        if jogo in linha:
                            return True
                    
                ateQuando = self.browser.find_element_by_class_name('css-etnin6').text
                nomeJogo = self.browser.title

                if not verificarJogoNaLista(self, self.browser.current_url):
                    jogosGratis.append([nomeJogo, self.browser.current_url, ateQuando, 'Epic Games Store'])
                    # print(nomeJogo + ' | ' + self.browser.current_url + ' | ' + 'Jogo Grátis!')
            except:
                pass
            sleep(2)

        return jogosGratis
    
    def fecharNavegador(self):
        os.remove('geckodriver.log')
        self.browser.quit()

class TwitterBotClass():
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        self.auth.set_access_token(accessKey, accessSecret)
        self.api = tweepy.API(self.auth)

    def criarTweet(self, dadosJogo):
        def pegarData(self):
            data = ''

            for caractere in dadosJogo[2]:
                if caractere.isnumeric() or caractere == '/' or caractere == ':':
                    data += caractere
            
            return data

        self.api.update_status(f'{dadosJogo[0]} está de graça na {dadosJogo[3]}!\nVálido até {pegarData(dadosJogo[2])[:-5]}.\n{dadosJogo[1]}')
        print(f'{dadosJogo[0]} está de graça na {dadosJogo[3]}! {dadosJogo[1]}!\nVálido até {pegarData(dadosJogo[2])[:-5]}')

    def mandarMensagem(self):
        self.api.send_direct_message(minhaContaPrincipal, 'TESTE BEM SUCEDIDO')

def esperar():
    sleep(60 * 60 * 2)

def salvarJogoGratis(jogo):
    with open('games_list.txt', 'a') as gamesLista:
        gamesLista.write(str(jogo) + '\n')
        gamesLista.close()

if __name__ == '__main__':
    while True:
        # print('BUSCANDO!')
        # procurarFreeSteamKeys = ProcurarFreeSteamKeys()
        # print(procurarFreeSteamKeys)
        buscar = SeleniumBusca()
        jogos = buscar.epicGamesStore()
        buscar.fecharNavegador()
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

        twitterBot = TwitterBotClass()
        twitterBot.mandarMensagem()
                           
        for jogo in jogos:
            salvarJogoGratis(jogo)
            twitterBot.criarTweet(jogo)

        sleep(1000)
        
