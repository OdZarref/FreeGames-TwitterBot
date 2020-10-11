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
            list: Retorna uma lista contendo os jogos que estão gratuitos por tempo limitado.
        """
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
                    if 'continuar' in botao.text.lower(): botao.click()
            except NoSuchElementException: pass
            except: print('Ocorreu uma exceção no primeiro try de "epicGameStore()"')
            
            try:
                def verificarJogoNaLista(self, jogo):
                    """Verifica que o jogo do momento está na lista de jogos grátis já vistos.

                    Args:
                        jogo (str): A URL do jogo para verificação.

                    Returns:
                        boolean: Retorna "True" se o jogo já estiver na lista.
                    """
                    gamesLista = open('games_list.txt')
                    for linha in gamesLista:
                        if jogo in linha: return True
                
                def pegarData(self, dataNaoTratada):
                    """Pega a frase onde está a data e seleciona apenas os números e os organiza.

                    Args:
                        dataNaoTratada (str): A frase que contem a data.

                    Returns:
                        str: Retorna apenas os números e já organizados.
                    """
                    dataTratada = ''
                    for caractere in dataNaoTratada:
                        if caractere.isnumeric(): dataTratada += caractere
                    
                    dia = dataTratada[0:2]
                    mes = dataTratada[2:4]
                    ano = dataTratada[4:8]
                    hora = dataTratada[8:10]
                    data = f'{ano}{mes}{dia}{hora}'
                    return data
                    
                ateQuando = pegarData(self, self.browser.find_element_by_class_name('css-etnin6').text)
                nomeJogo = self.browser.title

                if not verificarJogoNaLista(self, self.browser.current_url):
                    dadosJogo = {'nome': nomeJogo, 'url': self.browser.current_url, 'validoAte': ateQuando, 'loja':'Epic Games', 'gameOuDlc': 'game', 'lembretePostado': False}
                    jogosGratis.append(dadosJogo)
                    salvarJogoGratis(str(dadosJogo))
            except NoSuchElementException: pass
            except: print('Ocorreu uma exceção no segundo try de "epicGameStore()"')
            sleep(5)
        return jogosGratis
    
    def procurarFreeSteamKeys(self):
        """Procura os jogos que estão gratuitos para Steam em "freesteamkeys.com".
        """
        def verificarExpirado(self, divPostThumbnail):
            """Verifica se o jogo do post atual está expirado ou não.

            Args:
                divPostThumbnail (webelement Selenium): Elemento que contem informações importantes sobre a postagem.

            Returns:
                boolean: Retorna "True" caso tenha expirado e "False" caso não.
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

            if itemId == pegarUltimoVistoFreeSteamKeys(self):
                break

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
                    str: A data tratada.
                """
                ano = datetime.now().year
                listaAbreviacoesMeses = ['jan', 'fev', 'mar', 'abr', 'maio', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

                for posicao, mes in enumerate(listaAbreviacoesMeses):
                    if mes in textoData: numeroMes = posicao + 1
                        
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric(): dia = caractere + textoData[posicao + 1]
                        else: dia = '0' + caractere
                        break
                
                for posicao, caractere in enumerate(textoData):
                    if caractere.isnumeric():
                        if textoData[posicao + 1].isnumeric() and textoData[posicao + 2] == ':':
                            hora = caractere + textoData[posicao + 1]
                return f'{ano}{numeroMes}{dia}{hora}'

            sleep(5)
            try: nomeJogo = self.browser.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[3]').text
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
            except: print('ERRO AQUI')

            dadosJogo = {'nome':nomeJogo, 'url':urlJogo, 'validoAte': ateQuando, 'loja':'steam', 'gameOuDlc':gameOuDlc, 'gameNecessario':gameNecessario, 'lembretePostado': False}
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
        def buscarDadosJogoPSNStore(self, listaURLSJogos):
            def verificarJogoNaListaPSN(self, urlJogo):
                """Verificará se o jogo já está na lista de jogos grátis.

                Args:
                    urlJogo (str): A URL do jogo.

                Returns:
                    boolean: Retorna "True" se o jogo já estiver na lista.
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

            def pegarAteQuando(self):
                """Pegará a data de até quando o jogo estará gratuito.
                """
                def tratarHora(self, strHora, periodo):
                    """Transformará o formato de hora em 24h.

                    Args:
                        strHora (str): Texto com a hora de até quando o jogo ficará gratuito.
                        periodo (str): Se é PM ou AM.

                    Returns:
                        [type]: [description]
                    """
                    if 'pm' in periodo:  return str(int(strHora) + 12)
                    else: return strHora

                def tratarAteQuando(self, ateQuando, hora):
                    """Pega a data de até quando o jogo ficará gratuito e a trata e junta com a hora. Organizando em aaaa/mm/dd/hh.

                    Args:
                        ateQuando (str): Data não tratada, contem '/'.
                        hora (str): A hora de até quando o jogo ficará gratuito.
                    returns:
                        (str): A data junto com a hora em formato aaaa/mm/dd/hh
                    """
                    def salvarDataPSN(self, data):
                        """Salva em um arquivo txt quando novos jogos ficarão gratuitos na PSN.

                        Args:
                            data (str): A data de quando os jogos atuais deixarão de ser gratuitos.
                        """
                        with open('psnData.txt', 'w') as arquivo: arquivo.write(data)

                    ateQuandoLista = ateQuando.split('/')
                    ano = ateQuandoLista[2]
                    mes = ateQuandoLista[1]
                    dia = '0' + ateQuandoLista[0]
                    data = ano + mes + dia + hora
                    salvarDataPSN(self, data)
                    return data

                ateQuandoTexto = self.browser.find_element_by_class_name('price-availability').text.split()
                ateQuando = tratarAteQuando(self, ateQuandoTexto[-3], tratarHora(self, ateQuandoTexto[-2][:2], ateQuandoTexto[-1]))
                return ateQuando

            for url in listaURLSJogos:
                self.browser.get(url)
                sleep(10)
                nome = self.browser.find_element_by_class_name('pdp__title').text
                ateQuando = pegarAteQuando(self)
                dadosJogo = {'nome': nome, 'url': url, 'validoAte': ateQuando, 'gameOuDlc': 'game', 'loja': 'psn', 'lembretePostado': False}
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
        """Fecha o navegador e apaga o arquivo de log gerado por ele.
        """
        self.browser.quit()
        os.remove('geckodriver.log')

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
            if not 'information unavailable' in data.lower(): dataTratada = f'{data[0:4]}-{data[4:6]}-{data[6:8]}'
            else: dataTratada = data
            return dataTratada

        def criarTextoTweet(self):
            """Criará o texto para postar um novo jogo gratuito.

            Returns:
                str: O texto a ser publicado.
            """
            hashtags = f'#freegames #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").replace("™", "").lower()} '
            if 'epicgames' == dadosJogo['loja'].lower().replace(' ', ''): hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']: hashtags += '#steam #pcgaming'
            elif 'psn' in dadosJogo['loja']: hashtags += '#console #playstation #psn'
            string = f'🎮 A NEW {dadosJogo["gameOuDlc"].upper()} IS FOR FREE! 🎮\n\n{dadosJogo["nome"]} is for free on {dadosJogo["loja"].upper()}.\n\n'
            if dadosJogo['loja'].lower() == 'psn': string += f"⚠️ Note: It's required PSN PLUS to grab this game for free.\n\n"
            if dadosJogo['gameOuDlc'] == 'dlc': string += f"⚠️ Note: It's necessary the base game {dadosJogo['gameNecessario']}.\n\n"
            string += f'Valid until: {tratarData(self, dadosJogo["validoAte"])}\n\nFavorite ❤️ and Reply ↩️\n\n{hashtags}\n{dadosJogo["url"]}'
            return string

        def criarTextoTweetLembrete(self):
            """Cria o texto para o lembrete.

            Returns:
                str: O texto a ser publicado.
            """
            hashtags = f'#freegames #{dadosJogo["nome"].replace(" ", "").replace("-", "").replace(":", "").replace("™", "").lower()} '
            if 'epicgamesstore' == dadosJogo['loja'].lower().replace(' ', ''): hashtags += '#epic #epicgames #pcgaming'
            elif 'steam' in dadosJogo['loja']: hashtags += '#steam #pcgaming'
            elif 'psn' in dadosJogo['loja']: hashtags += '#console #playstation #psn'
            string = f"⚠️ REMINDER ⚠️\n\nIt's your last chance to take {dadosJogo['nome']} for free on {dadosJogo['loja'].upper()}. Will expire in the next few hours!\n\n"
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
        # self.api.update_status(textoTweet)

    def mandarMensagem(self):
        """Manda uma mensagem na minha conta principal, mostrando que o bot continua funcionando.
        """
        self.api.send_direct_message(minhaContaPrincipal, 'TESTE BEM SUCEDIDO')

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

    Args:[ty
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
                        if dataGameHora - data.hour <= 5:
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
        if dicionarioJogo['validoAte'].isnumeric():
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
        
        dataPSN = open('psnData.txt').readline()
        if dataPSN.isalpha():
            jogosPSN = buscar.psnStore()
            for jogoPSN in jogosPSN:
                print('JOGO PSN\n', jogoPSN)
                print('TWEET PSN')
                twitterBot.postarTweet(jogoPSN, 'PostarJogo')

        elif str(datetime.now().day) == dataPSN[-3] and datetime.now().strftime('%H') > dataPSN[-2:]:
            jogosPSN = buscar.psnStore()
            for jogoPSN in jogosPSN:
                print('JOGO PSN\n', jogoPSN)
                print('TWEET PSN')
                twitterBot.postarTweet(jogoPSN, 'PostarJogo')

            print('\n===================================================================================================\n')
            
        jogosEpic = buscar.epicGamesStore()
        for jogo in jogosEpic:
            print('JOGO EPIC GAMES\n', jogo)

            print('TWEET EPIC')
            twitterBot.postarTweet(jogo, 'PostarJogo')
        
#         #twitterBot.mandarMensagem()
        buscar.fecharNavegador()
        print('PROCURANDO NOVAMENTE EM 1 HORA...')
        esperar(1)

#estão comentadas as linhas quem postam o tweet e mandam a mensagem
