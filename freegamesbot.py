import requests
import tweepy
import os
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from tokens import *

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
            sleep(2)

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
                    jogosGratis.append([nomeJogo, self.browser.current_url, ateQuando, 'Epic Games Store', 'game'])
                    # print(nomeJogo + ' | ' + self.browser.current_url + ' | ' + 'Jogo Grátis!')
            except:
                pass
            sleep(2)

        return jogosGratis
    
    def procurarFreeSteamKeys(self):
        def verificarExpirado(self, divPostThumbnail):
            try:
                divPostThumbnail.find_element_by_class_name('expire_stamp')
                return True
            except:
                return False
                
        def acessarAnalizarPaginaDoJogo(self, link, linksJogos):
            def tratarLink(self, link):
                linkTratado = ''
                for contador, caractere in enumerate(link):
                    if contador > 23:
                        if caractere == "'": break
                        linkTratado += caractere
                
                return linkTratado

            self.browser.get(link)
            sleep(2)
            ancoras = self.browser.find_elements_by_tag_name('a')

            for ancora in ancoras:
                try:
                    linkTratado = tratarLink(self, ancora.get_attribute('onclick'))
                    if 'store.steampowered' in linkTratado:
                        print(linkTratado + ' | Jogo Steam!')
                        linksJogosSteam.append(linkTratado)
                except NoSuchElementException:
                    pass


        def pegarUltimoVistoFreeSteamKeys(self):
            with open('ultimovisto_freesteamkeys.txt') as arquivo:
                return arquivo.read()
        
        def atualizarUltimoVistoFreeSteamKeys(self, ultimoVisto):
            with open('ultimovisto_freesteamkeys.txt', 'w') as arquivo:
                arquivo.write(ultimoVisto)

        self.browser.get('https://www.freesteamkeys.com/')
        sleep(2)
        divPostItems = self.browser.find_element_by_id('post-items')
        articles = divPostItems.find_elements_by_tag_name('article')
        linksJogos = list()
        linksJogosSteam = list()
        contador = 0

        for article in articles:
            itemId = article.get_attribute('id')
            print(itemId)

            if itemId == pegarUltimoVistoFreeSteamKeys(self):
                print('Nenhuma atualização no site.')
                break

            if not itemId == 'post-':
                if contador == 0: atualizarUltimoVistoFreeSteamKeys(self, itemId)
                try:
                    divPostThumbnail = article.find_element_by_class_name('post-thumbnail')

                    if not verificarExpirado(self, divPostThumbnail):
                        link = divPostThumbnail.find_element_by_tag_name('a').get_attribute('href')
                        linksJogos.append(link)
                except NoSuchElementException:
                    pass
                except:
                    print('OCORREU UMA EXCEÇÃO EM "def procurarSteamKeys()"')
                contador += 1

        for link in linksJogos:
            sleep(1)
            acessarAnalizarPaginaDoJogo(self, link, linksJogos)
                
        return linksJogosSteam

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
            
        def criarTexto(self):
            hashtags = f'#freegames #freegame #{dadosJogo[0].replace(" ", "").lower()} '
            if 'epic' in dadosJogo[3].lower(): hashtags += '#epic #epicgames #pcgaming'
            string = f'🎮A NEW {dadosJogo[4].upper()} IS FOR FREE!🎮\n{dadosJogo[0]} está de graça na {dadosJogo[3]}!\nVálido até {pegarData(dadosJogo[2])[:-5]}.\n{hashtags}\n{dadosJogo[1]}'

            return string

        # self.api.update_status(f'{dadosJogo[0]} está de graça na {dadosJogo[3]}!\nVálido até {pegarData(dadosJogo[2])[:-5]}.\n{dadosJogo[1]}')
        print(criarTexto(self))

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
        print('BUSCANDO!')
        buscar = SeleniumBusca()
        # jogos = buscar.epicGamesStore()
        # buscar.fecharNavegador()
        # print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

        # twitterBot = TwitterBotClass()
        # # twitterBot.mandarMensagem()
                           
        # for jogo in jogos:
        #     salvarJogoGratis(jogo)
        #     twitterBot.criarTweet(jogo)

        sleep(10)
        
