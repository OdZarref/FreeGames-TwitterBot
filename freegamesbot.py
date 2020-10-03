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
        print('BUSCANDO EM EPIC GAMES STORE\n')
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
                
                def pegarData(self, dataNaoTratada):
                    dataTratada = ''
                    for caractere in dataNaoTratada:
                        if caractere.isnumeric():
                            dataTratada += caractere
                    
                    dia = dataTratada[0:2]
                    mes = dataTratada[2:4]
                    ano = dataTratada[4:8]
                    hora = dataTratada[8:10]
                    data = f'{ano}{mes}{dia}{hora}'

                    return data
                    
                ateQuando = pegarData(self, self.browser.find_element_by_class_name('css-etnin6').text)
                nomeJogo = self.browser.title

                if not verificarJogoNaLista(self, self.browser.current_url):
                    dadosJogo = {'nome': nomeJogo, 'url': self.browser.current_url, 'validoAte': ateQuando, 'loja':'Epic Games Store', 'gameOuDlc': 'game'}
                    jogosGratis.append(dadosJogo)
                    salvarJogoGratis(str(dadosJogo))
                    # print(nomeJogo + ' | ' + self.browser.current_url + ' | ' + 'Jogo Grátis!')
            except:
                pass
            sleep(2)

        print('-------------------------------------------------------')
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

        print('\nBUSCANDO EM FREESTEAMKEYS')
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
                break

            if not itemId == 'post-':
                if contador == 0: ultimoVistoId = itemId
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
            try:
                atualizarUltimoVistoFreeSteamKeys(self, ultimoVistoId)
            except UnboundLocalError:
                pass
        return linksJogosSteam

    def steamStore(self, links):
        def coletarDadosJogo(self):
            def pegarData(self, textoData):
                from datetime import datetime

                ano = datetime.now().year
                listaAbreviacoesMeses = ['jan', 'fev', 'mar', 'abr', 'maio', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

                for posicao, mes in enumerate(listaAbreviacoesMeses):
                    if mes in textoData:
                        numeroMes = posicao + 1
                        
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric():
                            dia = caractere + textoData[posicao + 1]
                        else:
                            dia = '0' + caractere

                        break
                
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric() and textoData[posicao + 2] == ':':
                            hora = caractere + textoData[posicao + 1]


                return f'{ano}{numeroMes}{dia}{hora}'

            sleep(1)
            try:
                nomeJogo = self.browser.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[3]').text#'//div[@class="apphub_AppName"').text
            except NoSuchElementException:
                nomeJogo = 'Not Found'
    
            urlJogo = self.browser.current_url

            try:
                self.browser.find_element_by_class_name("game_area_dlc_bubble")
                gameOuDlc = 'dlc'
                # gameNecessario = 
            except: gameOuDlc = 'game'

            try: ateQuando = pegarData(self, self.browser.find_element_by_css_selector('p.game_purchase_discount_quantity ').text)
            except NoSuchElementException: ateQuando = 'Information Unavailable'
            except: print('ERRO AQUI')

            dadosJogo = {'nome':nomeJogo, 'url':urlJogo, 'validoAte': ateQuando, 'loja':'steam', 'gameOuDlc':gameOuDlc}
            salvarJogoGratis(str(dadosJogo))

            return dadosJogo

        print('\nCOLETANDO DADOS DOS JOGOS STEAM\n')
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
        def criarTexto(self):
            def tratarData(self, data):
                if not 'information unavailable' in data.lower(): dataTratada = f'{data[0:4]}-{data[4:6]}-{data[6:8]}'
                else: dataTratada = data
                return dataTratada

            hashtags = f'#freegames #freegame #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").lower()} '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''):
                hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']:
                hashtags += '#steam #pcgaming'
            string = f'🎮A NEW {dadosJogo["gameOuDlc"].upper()} IS FOR FREE!🎮\n\n{dadosJogo["nome"]} is for free on {dadosJogo["loja"].capitalize()}!\n\nValid until: {tratarData(self, dadosJogo["validoAte"])}\n\n{hashtags}\n{dadosJogo["url"]}'

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
        buscar = SeleniumBusca()
        jogosFreeSteamKeys = buscar.procurarFreeSteamKeys()
        jogosSteam = buscar.steamStore(jogosFreeSteamKeys)
        twitterBot = TwitterBotClass()
        for jogo in jogosSteam:
            print('JOGO STEAM')
            print(jogo)
            print('\n------------------------------------------------------------\n')

            print('TWEET STEAM')
            twitterBot.criarTweet(jogo)
            print('\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')
        print('====================================================================================================\n')

        jogosEpic = buscar.epicGamesStore()
        for jogo in jogosEpic:
            print('JOGO EPIC GAMES')
            print(jogo)
            print('\n------------------------------------------------------------\n')

            print('TWEET EPIC')
            twitterBot.criarTweet(jogo)
            print('\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')
        
        #twitterBot.mandarMensagem()
        buscar.fecharNavegador()
        print('PROCURANDO NOVAMENTE EM 2 HORAS...')
        sleep(10)
    