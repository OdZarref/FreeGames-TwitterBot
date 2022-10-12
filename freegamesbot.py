import tweepy
import os
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tokens import *
from datetime import datetime

class SeleniumBusca:
    """Classe responsável pela busca através do Selenium. Contem funções para busca em Epic Games Store, Steam e PSN.
    """
    def __init__(self):
        """Define os atributos da classe. Sendo este o objeto do navegador.
        """
        if os.name == 'nt': self.browser = Firefox(executable_path='./webdrivers/geckodriver.exe')
        else: self.browser = Firefox(executable_path='./webdrivers/geckodriver')

    def epicGamesStore(self):
        """Busca os jogos que estão gratuitos na Epic Games Store.

        Returns:
            list: Uma lista contendo os jogos que estão gratuitos por tempo limitado.
        """
        def tratarData(string):
            abreviacoesMeses = ['jan.', 'fev.', 'mar.', 'abr.', 'maio.', 'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
            palavrasString = string.split()
            contadorPalavrasNumericas = 0

            for palavra in palavrasString:
                if palavra.isnumeric() and contadorPalavrasNumericas == 0:
                    contadorPalavrasNumericas += 1
                    dia = palavra

                    if len(dia) < 2: dia = '0' + dia
                for abreviaturaMes in abreviacoesMeses:
                    if palavra == abreviaturaMes:
                        mes = abreviacoesMeses.index(palavra) + 1
                        break

            if mes == 'dez.' and dia >= 25: ano = datetime.now().year + 1
            else: ano = datetime.now().year


            return {'ano': str(ano), 'mes': str(mes), 'dia': str(dia), 'hora':'12'}

        def verificarJogoNaLista(jogo):
            """Verifica que o jogo do momento está na lista de jogos grátis já vistos.

            Args:
                jogo (str): O nome do jogo para verificação.

            Returns:
                boolean: "True" se o jogo já estiver na lista.
            """
            gamesLista = open('games_list.txt')
            for linha in gamesLista:
                if jogo in linha: return True

        def salvarJogoNaLista(jogo):
            with open('games_list.txt', 'a') as gamesLista:
                gamesLista.write(str(jogo) + '\n')


        print('BUSCANDO EM EPIC GAMES STORE\n')
        self.browser.get('https://www.epicgames.com/store/pt-BR/free-games')
        sleep(5)
        elementos = self.browser.find_elements_by_class_name('css-1ukp34s')
        jogos = list()
        jogosGratis = list()

        for elemento in elementos:
            jogoURL = elemento.find_element_by_tag_name('a').get_attribute('href')
            nomeJogo = elemento.text.split('\n')[1]
            dataEpic = tratarData(elemento.text.split('\n')[-1])

            try:
                if elemento.find_element_by_class_name('css-11xvn05') and not verificarJogoNaLista(nomeJogo):
                    jogosGratis.append({'nome': nomeJogo, 'url': jogoURL, 'validoAte': dataEpic, 'loja': 'Epic Games', 'gameOuDlc': 'game', 'lembretePostado': False})
                    salvarJogoNaLista({'nome': nomeJogo, 'url': jogoURL, 'validoAte': dataEpic, 'loja': 'Epic Games', 'gameOuDlc': 'game', 'lembretePostado': False})

            except NoSuchElementException: pass
            except: print('erro')

        return jogosGratis
    
    def procurarFreeSteamKeys(self):
        """Procura os jogos que estão gratuitos para Steam em "freesteamkeys.com".
        """
        def verificarExpirado(self, divPostThumbnail):
            """Verifica se o jogo do post atual está expirado ou não.

            Args:
                divPostThumbnail (webelement Selenium): Elemento que contem informações importantes sobre a postagem.

            Returns:
                boolean: "True" caso tenha expirado e "False" caso não.
            """
            try:
                divPostThumbnail.find_element_by_class_name('expire_stamp')
                return True
            except NoSuchElementException: return False
            except: print('Ocorreu uma exceção em "verificarExpirado()"')
                
        def acessarAnalizarPostagem(self, link):
            """Acessa a página da postagem e verifica se o jogo é diretamente gratuito no Steam.

            Args:
                link (str): O link da postagem.
            """
            def tratarLink(self, link):
                """A âncora que contem o link Steam dispara um evento javascript que dificulta em pegar o link Steam. Esta função irá remover as partes referentes a este evento.

                Args:
                    link (str): Link que a âncora contem.

                Returns:
                    str: O link Steam corretamente tratado.
                """
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
                except NoSuchElementException: pass
                except TypeError: pass
                except: print('Ocorreu uma exceção em "acessarAnalizarPostagem()"')


        def pegarUltimoVistoFreeSteamKeys(self):
            """Pegará o ID da última postagem vista pelo programa.

            Returns:
                str: O ID da última postagem.
            """
            with open('ultimovisto_freesteamkeys.txt') as arquivo:
                return arquivo.read()
        
        def atualizarUltimoVistoFreeSteamKeys(self, ultimoVisto):
            """Irá atualizar o ID do último visto no arquivo txt que contem esta informação pelo ID da última postagem vista.

            Args:
                ultimoVisto (str): O ID da última postagem vista.
            """
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

            try:
                if itemId == pegarUltimoVistoFreeSteamKeys(self):
                    break
            except FileNotFoundError: pass

            if not itemId == 'post-':
                if contador == 0: ultimoVistoId = itemId
                try:
                    divPostThumbnail = article.find_element_by_class_name('post-thumbnail')

                    if not verificarExpirado(self, divPostThumbnail):
                        link = divPostThumbnail.find_element_by_tag_name('a').get_attribute('href')
                        linksJogos.append(link)
                except NoSuchElementException: pass
                except: print('Ocorreu uma exceção em "procurarSteamKeys()"')
                contador += 1

        for link in linksJogos:
            sleep(1)
            acessarAnalizarPostagem(self, link)
            try: atualizarUltimoVistoFreeSteamKeys(self, ultimoVistoId)
            except UnboundLocalError: pass
            except: print('Ocorreu uma exceção no último try de "procurarFreeSteamKeys"')
        return linksJogosSteam

    def steamStore(self, links):
        """Acessará a página de cada jogo no Steam.

        Args:
            links (list): Lista com os jogos ou jogo gratuito.
        returns:
            jogosGratisSteam (list): Lista com os dicionários dos jogos.

        """
        def coletarDadosJogo(self):
            """Pegará as seguintes informações: link do jogo, nome do jogo, se é DLC ou não, o jogo base caso seja DLC, o nome da loja e até quando ficará gratuito. Colocará estas informações em um dicionário e irá inserir este dicionário em uma lista
            """
            def pegarData(self, textoData):
                """Pegará a frase que contem a data até quando o jogo ficará grátis e irá tratá-la. Deixando apenas os caracteres numéricos.

                Args:
                    textoData (str): A frase que contem a data.

                Returns:
                    dict: A data tratada.
                """
                ano = datetime.now().year
                listaAbreviacoesMeses = ['jan', 'fev', 'mar', 'abr', 'maio', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
                dataGame = dict()


                for posicao, mes in enumerate(listaAbreviacoesMeses):
                    if mes in textoData: dataGame['mes'] = posicao + 1
                        
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric(): dataGame['dia'] = caractere + textoData[posicao + 1]
                        else: dataGame['dia'] = '0' + caractere
                        break
                
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric() and textoData[posicao + 2] == ':':
                            dataGame['hora'] = caractere + textoData[posicao + 1]
                return dataGame

            sleep(5)
            try: nomeJogo = self.browser.find_element_by_id('appHubAppName').text
            except NoSuchElementException: nomeJogo = 'Name Not Found'
    
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

            dadosJogo = {'nome':nomeJogo, 'url':urlJogo, 'validoAte': ateQuando, 'loja':'steam', 'gameOuDlc':gameOuDlc, 'gameNecessario':gameNecessario, 'lembretePostado': False}
            if ateQuando != 'Information Unavailable':
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
                    if 'acessar página' in a.text.lower(): a.click()
            except NoSuchElementException: pass
            except: print('Ocorreu uma exceção no try de "steamStore()"')
            
            jogosGratisSteam.append(coletarDadosJogo(self))
        return jogosGratisSteam
    
    def psnStore(self):
        """Procurará os jogos grátis na PSN.

        returns:
            list: Lista com os dicionários dos jogos gratuitos.
        """
        def buscarDadosJogosPSNStore(listaURLSJogos):
            def verificarJogoNaListaPSN(self, urlJogo):
                """Verificará se o jogo já está na lista de jogos grátis.

                Args:
                    urlJogo (str): A URL do jogo.

                Returns:
                    boolean: "True" se o jogo já estiver na lista.
                """
                arquivo = open('games_list.txt')
                for linha in arquivo:
                    if urlJogo in linha: return True

            def atualizarJogoGratisPSN(self, jogo):
                """Adiciona o jogo na lista de jogos grátis do programa.

                Args:
                    jogo (dict): Dicionário com as informações do jogo.
                """
                arquivo = open('games_list.txt', 'a')
                arquivo.write(str(jogo) + '\n')

            for url in listaURLSJogos:
                self.browser.get(url)
                sleep(10)
                nome = self.browser.find_element_by_class_name('psw-t-title-l').text
                if nome == 'Edições': nome = self.browser.find_element_by_class_name('game-title').text
                elementosNome = self.browser.find_elements_by_class_name('psw-c-t-2')
                for elemento in elementosNome:
                    if 'oferta' in elemento.text:
                        palavras = elemento.text.split()
                        data = palavras[4].split('/')
                        dataTratada = dict()
                        if len(data[0]) == 1: dataTratada['dia'] = '0' + data[0]
                        else: dataTratada['dia'] = data[0]
                        dataTratada['mes'] = data[1]
                        dataTratada['ano'] = data[2]
                        dataTratada['hora']= palavras[5][0:2]
                        dadosJogo = {'nome': nome, 'url': url, 'validoAte': dataTratada, 'loja': 'PSN', 'gameOuDlc': 'game', 'lembretePostado': False}
                        print(dadosJogo)

                        with open('games_list.txt', 'r') as arquivoGames:
                            jogoJaExistente = False

                            for linha in arquivoGames.readlines():
                                if dadosJogo['nome'] in linha: jogoJaExistente = True

                            if not jogoJaExistente:
                                open('games_list.txt', 'a').write(str(dadosJogo) + '\n')
                                jogosGratisPSN.append(dadosJogo)
                
        print('PROCURANDO JOGOS PSN')
        jogosGratisPSN = list()
        urlJogosGratisPSN = list()
        self.browser.get('https://www.playstation.com/pt-br/ps-plus/whats-new/#monthly-games')
        sleep(10)
        elementos = self.browser.find_elements_by_class_name('cta__primary')
        for elemento in elementos:
            link = elemento.get_attribute('href')
            
            try:
                if 'https://www.playstation.com/pt-br/games/' in link: urlJogosGratisPSN.append(link)
            except TypeError: 
                pass

        buscarDadosJogosPSNStore(urlJogosGratisPSN)
        return jogosGratisPSN





    def fecharNavegador(self):
        """Fecha o navegador e apaga o arquivo de log gerado por ele.
        """
        self.browser.quit()
        # os.remove('geckodriver.log')

class TwitterBotClass():
    """Classe que contem os métodos referentes ao twitter.
    """
    def __init__(self):
        """Faz a validação do bot.
        """
        self.auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        self.auth.set_access_token(accessKey, accessSecret)
        self.api = tweepy.API(self.auth)

    def postarTweet(self, dadosJogo, tipo):
        """Posta um tweet com o texto contido na variável "string".

        Args:
            dadosJogo (dict): O jogo com os seus dados.
            tipo (str): Diz se o tweet será um novo jogo gratuito ou um lembrete.
        """
        def tratarData(self, data):
            """Irá remover a hora da data.

            Args:
                data (str): A data com a hora.

            Returns:
                str: A data sem a hora.
            """
            if not 'information unavailable' in str(data.lower()): dataTratada = f'{data[0:4]}-{data[4:6]}-{data[6:8]}'
            else: dataTratada = data
            return dataTratada

        def criarTextoTweet(self):
            """Criará o texto para postar um novo jogo gratuito.

            Returns:
                str: O texto a ser publicado.
            """
            dataJogo = dadosJogo['validoAte']
            hashtags = f'#freegames' + ' '
            if 'epicgames' == dadosJogo['loja'].lower().replace(' ', ''): hashtags += '#epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']: hashtags += '#steam #pcgaming'
            elif 'psn' in dadosJogo['loja']: hashtags += '#playstation #psn'
            string = f'🎮 A NEW {dadosJogo["gameOuDlc"].upper()} IS FOR FREE! 🎮\n\n{dadosJogo["nome"]} is for free on {dadosJogo["loja"].upper()}.\n\n'
            if dadosJogo['loja'].lower() == 'psn': string += f"⚠️ Note: It's required PSN PLUS to grab this game for free.\n\n"
            if dadosJogo['gameOuDlc'] == 'dlc': string += f"⚠️ Note: It's necessary the base game {dadosJogo['gameNecessario']}.\n\n"
            string += f'Valid until: {dataJogo["mes"]}/{dataJogo["dia"]}/{dataJogo["ano"]}\n\nFavorite ❤️ and Reply ↩️\n\n{hashtags}\n{dadosJogo["url"]}'
            return string

        def criarTextoTweetLembrete(self):
            """Cria o texto para o lembrete.

            Returns:
                str: O texto a ser publicado.
            """
            hashtags = f'#freegames' + ' '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''): hashtags += '#epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']: hashtags += '#steam #pcgaming'
            elif 'psn' in dadosJogo['loja'].lower(): hashtags += '#playstation #psn'
            string = f"⚠️ REMINDER ⚠️\n\nIt's your last chance to grab {dadosJogo['nome']} for free on {dadosJogo['loja'].upper()}. Will expire in the next few hours!\n\n"
            if dadosJogo['loja'].lower() == 'psn': string += f"⚠️ Note: It's required PSN PLUS to grab this game for free.\n\n"
            if dadosJogo['gameOuDlc'] == 'dlc': string += f"⚠️ Note: It's necessary the base game {dadosJogo['gameNecessario']}.\n\n"
            string += f"Valid until: {tratarData(self, dadosJogo['validoAte'])}\n\nFavorite ❤️ and Reply ↩️\n\n{hashtags}\n{dadosJogo['url']}"
            return string
            
        if tipo == 'PostarJogo':
            textoTweet = criarTextoTweet(self)
            print(textoTweet)
        elif tipo == 'PostarLembrete':
            textoTweet = criarTextoTweetLembrete(self)
            print(textoTweet)
        self.api.update_status(textoTweet)

    def mandarMensagem(self):
        """Manda uma mensagem na minha conta principal, mostrando que o bot continua funcionando.
        """
        # self.api.send_direct_message(minhaContaPrincipal, 'TESTE BEM SUCEDIDO')

def esperar(hora):
    """Função de espera.

    Args:
        hora (int): Quantas horas a função deve esperar.
    """
    sleep(60 * 60 * hora)

def salvarJogoGratis(jogo):
    """Adiciona o dicionário do jogo a lista de jogos gratuitos do programa.

    Args:
        jogo (str): Os dados do jogo.
    """
    with open('games_list.txt', 'a') as gamesLista:
        gamesLista.write(str(jogo) + '\n')
        gamesLista.close()

def verificarJogosAindaValidos(twitterBot):
    """Abre a lista de jogos grátis do programa, e analisa os jogos. Os que já são mais válidos, são excluídos da lista.

    Args:
        twitterBot (class): Instância de TwitterBotClass
    """
    def verificarDataEpostarLembrete(dataGame):
        """Verifica se a data do jogo é maior que a data do momento. E posta um lembrete se a data do momento estiver próxima.

        Args:
            dataGame (str): A data do jogo

        Returns:
            boolean: "True" se ainda for válido e "False" se não.
        """
        data = datetime.now()

        if int(dataGame['ano']) > data.year:
            return True
        elif int(dataGame['ano']) == data.year:
            if int(dataGame['mes']) > data.month:
                return True
            elif int(dataGame['mes']) == data.month:
                if int(dataGame['dia']) > data.day:
                    return True
                elif int(dataGame['dia']) == data.day:
                    if int(dataGame['hora']) > data.hour:
                        if int(dataGame['hora']) - data.hour <= 5:
                            try:
                                if not dicionarioJogo['lembretePostado']:
                                    twitterBot.postarTweet(dicionarioJogo, 'PostarLembrete')
                                    dicionarioJogo['lembretePostado'] = True
                            except KeyError:
                                print('KeyError')
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
        if dicionarioJogo['validoAte'] and dicionarioJogo['validoAte'] != 'Information Unavailable':
            print(dicionarioJogo['validoAte'])
            if verificarDataEpostarLembrete(dicionarioJogo['validoAte']): listaTemp.write(str(dicionarioJogo) + '\n')
    
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
        verificarJogosAindaValidos(twitterBot)
        for jogo in jogosSteam:
            print('JOGO STEAM\n', jogo)
            print('TWEET STEAM')
            twitterBot.postarTweet(jogo, 'PostarJogo')

        print('\n===================================================================================================\n')
        
        for jogo in buscar.psnStore():
            twitterBot.postarTweet(jogo, 'PostarJogo')

        print('\n===================================================================================================\n')
            
        jogosEpic = buscar.epicGamesStore()
        for jogo in jogosEpic:
            print('JOGO EPIC GAMES\n', jogo)

            print('TWEET EPIC')
            twitterBot.postarTweet(jogo, 'PostarJogo')
        
        twitterBot.mandarMensagem()
        buscar.fecharNavegador()
        print('PROCURANDO NOVAMENTE EM 1 HORA...')
        esperar(1)

#estão comentadas as linhas quem postam o tweet e mandam a mensagem
