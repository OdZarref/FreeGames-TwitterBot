import requests
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
from time import sleep

def esperar():
    sleep(60 * 60 * 2)

class SearchFreeSteamKeys():
    def __init__(self):
        def logProjeto(self, textLog):
            with open('bot_log.txt', 'a') as log:
                log.write(textLog)

        def retrieveLastSeenFreeSteamKeys(self):
            with open('last_seen_freesteamkeys.txt') as file:
                return file.read()

        def updateLastSeenFreeSteamKeys(self, lastSeen):
            with open('last_seen_freesteamkeys.txt', 'w') as file:
                file.write(lastSeen)

        def accessGamePage(url):
            gamePage = requests.get(url)
            gamePageSoup = BeautifulSoup(gamePage.text, 'html.parser')
            ancora = gamePageSoup.find('a', class_='zf-edit-button')
            gameButton = gamePageSoup.find('a', class_='item-url custom_link_button')

            if ancora.get('href')[7:] in gameButton.get('onclick'):
                logProjeto(self, f'JOGO STEAM! + {ancora.get("href")}' + '\n')

        self.page = requests.get('https://www.freesteamkeys.com/')
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        self.articles = self.soup.find(id='post-items')

        for count, article in enumerate(self.articles, start=0):
            divPostThumbnail = article.find(class_='post-thumbnail')
            try:
                if article.get('id') == retrieveLastSeenFreeSteamKeys(self):
                    break

                if not divPostThumbnail.find('div', class_='expire_stamp'):
                    print(divPostThumbnail.find('a').get('href'))
                    accessGamePage(divPostThumbnail.find('a').get('href'))
            except: 
                pass

            if count == 1:
                print('ISTO OCORREU')
                updateLastSeenFreeSteamKeys(self, article.get('id'))

class SeleniumBusca:
    def __init__(self):
        self.browser = Firefox()

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
                ateQuando = self.browser.find_element_by_class_name('css-etnin6').text
                nomeJogo = self.browser.title
                jogosGratis.append([nomeJogo, self.browser.current_url, ateQuando])
                print(nomeJogo + ' | ' + self.browser.current_url + ' | ' + 'Jogo Grátis!')
            except:
                pass
            sleep(2)

        return jogosGratis
    
    def fecharNavegador(self):
        self.browser.quit()

if __name__ == '__main__':
    while True:
        print('BUSCANDO!')
        buscar = SeleniumBusca()
        print(buscar.epicGamesStore())
        buscar.fecharNavegador()
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-') 