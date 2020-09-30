import requests
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

if __name__ == '__main__':
    from datetime import datetime
    while True:
        print(f'Procurando... | {datetime.now().strftime("%d-%m-%y_%Hh%Mm%Ss")}')
        searchGame = SearchFreeSteamKeys()
        esperar()