import tweepy
import os
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
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
        sleep(5)
        elementos = self.browser.find_elements_by_xpath('//div[@data-component="CardGridDesktopBase"]')
        jogos = list()
        jogosGratis = list()

        for elemento in elementos: jogos.append(elemento.find_element_by_tag_name('a').get_attribute('href'))

        for jogo in jogos:
            self.browser.get(jogo)
            sleep(5)

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
            sleep(5)

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
            sleep(5)
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
        sleep(5)
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

            sleep(5)
            try:
                nomeJogo = self.browser.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[3]').text#'//div[@class="apphub_AppName"').text
            except NoSuchElementException:
                nomeJogo = 'Not Found'
    
            urlJogo = self.browser.current_url

            try:
                divGameAreaDLCBubble = self.browser.find_element_by_class_name("game_area_dlc_bubble")
                gameOuDlc = 'dlc'
                gameNecessario = divGameAreaDLCBubble.find_element_by_tag_name('a').text
            except:
                gameOuDlc = 'game'
                gameNecessario = 'nenhum'

            try: ateQuando = pegarData(self, self.browser.find_element_by_css_selector('p.game_purchase_discount_quantity ').text)
            except NoSuchElementException: ateQuando = 'Information Unavailable'
            except: print('ERRO AQUI')

            dadosJogo = {'nome':nomeJogo, 'url':urlJogo, 'validoAte': ateQuando, 'loja':'steam', 'gameOuDlc':gameOuDlc, 'gameNecessario':gameNecessario}
            salvarJogoGratis(str(dadosJogo))

            return dadosJogo

        print('\nCOLETANDO DADOS DOS JOGOS STEAM\n')
        jogosGratisSteam = list()

        for link in links:
            self.browser.get(link)
            sleep(5)

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
    
    def psnStore(self):
        def buscarDadosJogoPSNStore(self, listaURLSJogos):
            def verificarJogoNaListaPSN(self, urlJogo):
                arquivo = open('games_list.txt')
                for linha in arquivo:
                    if urlJogo in linha:
                        return True

            def atualizarJogoGratisPSN(self, jogo):
                arquivo = open('games_list.txt', 'a')
                arquivo.write(str(jogo) + '\n')


            def pegarAteQuando(self):
                def tratarHora(self, strHora, periodo):
                    if 'pm' in periodo:  return str(int(strHora) + 12)
                    else: return strHora

                def tratarAteQuando(self, ateQuando, hora):
                    ateQuandoLista = ateQuando.split('/')
                    ano = ateQuandoLista[2]
                    mes = ateQuandoLista[1]
                    dia = '0' + ateQuandoLista[0]
                    data = ano + mes + dia + hora

                    return data

                ateQuandoTexto = self.browser.find_element_by_class_name('price-availability').text.split()
                ateQuando = tratarAteQuando(self, ateQuandoTexto[-3], tratarHora(self, ateQuandoTexto[-2][:2], ateQuandoTexto[-1]))

                return ateQuando

            for url in listaURLSJogos:
                self.browser.get(url)
                sleep(10)
                nome = self.browser.find_element_by_class_name('pdp__title').text
                ateQuando = pegarAteQuando(self)
                dadosJogo = {'nome': nome, 'url': url, 'validoAte': ateQuando, 'gameOuDlc': 'game', 'loja': 'psn'}
                if not verificarJogoNaListaPSN(self, dadosJogo['url']):
                    jogosGratisPSN.append(dadosJogo)
                    atualizarJogoGratisPSN(self, dadosJogo)
                
        print('PROCURANDO JOGOS PSN')
        jogosGratisPSN = list()
        self.browser.get('https://store.playstation.com/pt-br/grid/STORE-MSF77008-PSPLUSFREEGAMES/1')
        sleep(10)
        jogosDivs = self.browser.find_elements_by_css_selector('div.grid-cell-row__container > div')
        jogosPSN = list()
        for jogoDiv in jogosDivs: jogosPSN.append(jogoDiv.find_element_by_tag_name('a').get_attribute('href'))
        buscarDadosJogoPSNStore(self, jogosPSN)
        return jogosGratisPSN

    def fecharNavegador(self):
        os.remove('geckodriver.log')
        self.browser.quit()

class TwitterBotClass():
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        self.auth.set_access_token(accessKey, accessSecret)
        self.api = tweepy.API(self.auth)

    def postarTweet(self, dadosJogo, tipo):
        def tratarData(self, data):
            if not 'information unavailable' in data.lower(): dataTratada = f'{data[0:4]}-{data[4:6]}-{data[6:8]}'
            else: dataTratada = data
            return dataTratada

        def criarTextoTweet(self):
            hashtags = f'#freegames #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").replace("™", "").lower()} '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''):
                hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']:
                hashtags += '#steam #pcgaming'
            elif 'psn' in dadosJogo['loja']:
                hashtags += '#console #playstation #psn'
            string = f'🎮 A NEW {dadosJogo["gameOuDlc"].upper()} IS FOR FREE! 🎮\n\n{dadosJogo["nome"]} is for free on {dadosJogo["loja"].upper()}!\n\n'
            if dadosJogo['gameOuDlc'] == 'dlc': string += f"it's necessary the base game {dadosJogo['gameNecessario']}.\n\n"
            string += f'Valid until: {tratarData(self, dadosJogo["validoAte"])}\n\nFavorite ❤️ and Reply ↩️\n\n{hashtags}\n{dadosJogo["url"]}'

            return string

        def criarTextoTweetLembrete(self):
            hashtags = f'#freegames #freegame #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").lower()} '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''):
                hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']:
                hashtags += '#steam #pcgaming'
            string = f"⚠️ REMINDER ⚠️\n\nIt's your last chance to take {dadosJogo['nome']} for free on {dadosJogo['loja'].capitalize()}. It will expire in the next few hours!\n\nValid until: {tratarData(self, dadosJogo['validoAte'])}\n\nFavorite ❤️ and Reply ↩️\n\n{hashtags}\n{dadosJogo['url']}"

            return string
            
        if tipo == 'PostarJogo':
            textoTweet = criarTextoTweet(self)
            print(textoTweet)
        elif tipo == 'PostarLembrete':
            textoTweet = criarTextoTweetLembrete(self)
            print(textoTweet)

        
        self.api.update_status(textoTweet)

    def mandarMensagem(self):
        self.api.send_direct_message(minhaContaPrincipal, 'TESTE BEM SUCEDIDO')

def esperar(hora):
    sleep(60 * 60 * hora)

def salvarJogoGratis(jogo):
    with open('games_list.txt', 'a') as gamesLista:
        gamesLista.write(str(jogo) + '\n')
        gamesLista.close()

def verificarJogosAindaValidosEPostarLembrete(twitterBot):
    def verificarData(dataGame):
        from datetime import datetime

        data = datetime.now()
        dataGameAno = int(dataGame[0:4])

        if dataGameAno > data.year:
            return True
        elif dataGameAno == data.year:
            dataGameMes = int(dataGame[4:6])
            if dataGameMes > data.month:
                return True
            elif dataGameMes == data.month:
                dataGameDia = int(dataGame[6:8])
                if dataGameDia > data.day:
                    return True
                elif dataGameDia == data.day:
                    dataGameHora = int(dataGame[8:10])
                    if dataGameHora > data.hour:
                        if dataGameHora - data.hour<= 5:
                            twitterBot.postarTweet(dicionarioJogo, 'PostarLembrete')
                        else:
                            return True
                else:
                    return False
            else:
                return False
        else:
            return False

    from ast import literal_eval
    
    listaJogos = open('games_list.txt')
    listaTemp = open('games_listTemp.txt', 'a')
    sleep(2)

    for jogo in listaJogos:
        dicionarioJogo = literal_eval(jogo.replace('\n', ''))
        if dicionarioJogo['validoAte'].isnumeric():
            if verificarData(dicionarioJogo['validoAte']):
                listaTemp.write(jogo)
    
    listaJogos.close()
    listaTemp.close()
    os.remove('games_list.txt')
    os.rename('./games_listTemp.txt', 'games_list.txt')

if __name__ == '__main__':
    while True:
        buscar = SeleniumBusca()

        jogosFreeSteamKeys = buscar.procurarFreeSteamKeys()
        jogosSteam = buscar.steamStore(jogosFreeSteamKeys)
        twitterBot = TwitterBotClass()
        verificarJogosAindaValidosEPostarLembrete(twitterBot)

        for jogo in jogosSteam:
            print('JOGO STEAM')
            print(jogo)

            print('TWEET STEAM')
            twitterBot.postarTweet(jogo, 'PostarJogo')

        print('\n===================================================================================================\n')

        jogosPSN = buscar.psnStore()
        for jogoPSN in jogosPSN:
            twitterBot.postarTweet(jogoPSN, 'PostarJogo')

        print('\n===================================================================================================\n')

        jogosEpic = buscar.epicGamesStore()
        for jogo in jogosEpic:
            print('JOGO EPIC GAMES')
            print(jogo)

            print('TWEET EPIC')
            twitterBot.postarTweet(jogo, 'PostarJogo')
        
#         #twitterBot.mandarMensagem()
        buscar.fecharNavegador()
        print('PROCURANDO NOVAMENTE EM 1 HORA...')
        esperar(1)

#estão comentadas as linhas quem postam o tweet e mandam a mensagem
