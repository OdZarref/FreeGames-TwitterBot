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
                    dadosJogo = {'nome': nomeJogo, 'url': self.browser.current_url, 'validoAte': ateQuando, 'loja':'Epic Games Store', 'gameOuDlc': 'game'}
                    jogosGratis.append(dadosJogo)
                    salvarJogoGratis(str(dadosJogo))
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
                except TypeError:
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

    def steamStore(self, links):
        def coletarDadosJogo(self):
            sleep(1)
            try:
                nomeJogo = self.browser.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[3]').text#'//div[@class="apphub_AppName"').text
            except NoSuchElementException:
                nomeJogo = 'Life is Strange 2 - Episode 1'
    
            urlJogo = self.browser.current_url

            try:
                self.browser.find_element_by_class_name("game_area_dlc_bubble")
                gameOuDlc = 'dlc'
                # gameNecessario = 
            except:
                gameOuDlc = 'game'

            dadosJogo = {'nome':nomeJogo, 'url':urlJogo, 'validoAte':'Informação indisponível', 'loja':'steam', 'gameOuDlc':gameOuDlc}
            salvarJogoGratis(str(dadosJogo))

            return dadosJogo

        jogosGratisSteam = list()

        for link in links:
            self.browser.get(link)
            sleep(1)

            try:
                self.browser.find_element_by_xpath('//option[@value="1990"]').click()
                tagsA = self.browser.find_elements_by_tag_name('a')
                for a in tagsA:
                    if 'acessar página' in a.text.lower():
                        a.click()
            except:
                pass
            
            jogosGratisSteam.append(coletarDadosJogo(self))
        
        return jogosGratisSteam
    
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

            for caractere in dadosJogo['validoAte']:
                if caractere.isnumeric() or caractere == '/' or caractere == ':':
                    data += caractere
            
            return data
            
        def criarTexto(self):
            hashtags = f'#freegames #freegame #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").lower()} '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''):
                hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']:
                hashtags += '#steam #pcgaming'
            string = f'🎮A NEW {dadosJogo["gameOuDlc"].upper()} IS FOR FREE!🎮\n{dadosJogo["nome"]} is for free on {dadosJogo["loja"].capitalize()}!\nValid until: {pegarData(dadosJogo["validoAte"])[:-5]}\n{hashtags}\n{dadosJogo["url"]}'

            return string

        textoTweet = criarTexto(self)
        print(textoTweet)
        self.api.update_status(textoTweet)

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
        print('BUSCANDO STEAM')
        buscar = SeleniumBusca()
        jogosFreeSteamKeys = buscar.procurarFreeSteamKeys()
        jogosSteam = buscar.steamStore(jogosFreeSteamKeys)
        for jogo in jogosSteam:
            print(jogo)
            twitterBot = TwitterBotClass()
            twitterBot.criarTweet(jogo)
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('BUSCANDO EPIC')

        jogosEpic = buscar.epicGamesStore()
        for jogo in jogosEpic:
            print(jogo)
            twitterBot = TwitterBotClass()
            twitterBot.criarTweet(jogo)
        
        buscar.fecharNavegador()
        # print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

        # twitterBot = TwitterBotClass()
        # # twitterBot.mandarMensagem()
                           
        # for jogo in jogos:
        #     salvarJogoGratis(jogo)
        #     twitterBot.criarTweet(jogo)

        sleep(1000)
        
