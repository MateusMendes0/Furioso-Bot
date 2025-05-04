import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

URL_NEWS = "https://gamearena.gg/tudo-sobre/furia/"
URL_GAMES = "https://www.strafe.com/br/team/furia-esports-cs-go-919fb3/"
URL_DIGITALOCEAN = "https://qjn4yrtgsgmgwtbktqsnsx5t.agents.do-ai.run/api/v1/chat/completions"


def requestUtil(url : str):

    headers = {'Accept-Language': 'pt'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    else:
        print(f"Erro ao acessar o site: {response.status_code}")
        return None


def getStats(prompt: str) -> str:
    load_dotenv()

    headers = {
        "Authorization": f"Bearer {os.getenv("DIGITALOCEAN_API")}",
        "Content-Type": "application/json"
    }

    body = {
        "messages": [
            {"role": "user", "content": f"{prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }

    response = requests.post(URL_DIGITALOCEAN, headers=headers, json=body)

    print(response)

    return response.json()["choices"][0]["message"]["content"]


def getNews() -> list[dict[str, str]]:

    newsArray = []

    soup = requestUtil(URL_NEWS)
    if soup:
        elementos = soup.find_all("div", class_="Grid__Row-sc-1g6aojd-1 liZFbE")
        for elemento in elementos:
            if elemento.text.startswith("CS2"):
                newsArray.append({
                    "title": elemento.text,
                    "link": elemento.find("a").get("href")
                })
    return newsArray


def getGames() -> dict[str, str] | None:
    soup = requestUtil(URL_GAMES)

    if soup:
        evento = soup.find( 'div', class_='text-sm lg:text-base')
        if evento:
            partida = {}

            partida["evento"] = evento.text

            partida["data"] = soup.find('span', class_="text-xs font-bold uppercase").text
            hora = soup.find('div', class_='flex items-start').text
            partida["hora"] = f"{hora[:2]}:{hora[2:]}"

            teams = soup.find_all('span', class_='truncatedText_container__fD0SA')
            teams = [teams[0].text, teams[1].text]

            partida["times"] = teams

            return partida

        else:
            print("Nenhum evento encontrado.")
            return None
    return None


def getLastGames() -> list[dict[str, str]]:

    gamesArray = []

    soup = requestUtil(URL_GAMES)

    if soup:
        games = soup.find( 'div', class_='competitorForm_form__6btFX relative flex flex-wrap space-x-[1px] border border-gray-500 bg-gray-500')
        if games:
            for game in games:

                gameDict = {
                    "evento": None,
                    "adversario": None,
                    "resultado": None,
                    "data": None
                }

                gameDict["evento"] = game.find('div', class_='whitespace-nowrap text-xs text-white').text
                adversario = game.find('img', class_='h-full w-full object-contain')
                if adversario:
                    adversario = adversario['alt']
                    gameDict["adversario"] = adversario
                else:
                    gameDict["adversario"] = None


                resultado = game.find("div", class_="mt-1 text-center text-xs font-bold")
                gameDict["resultado"] = resultado.text.replace("\xa0-\xa0", " x ")

                gameDict["data"] = game.find("div", class_="mt-3 mb-0.5 text-xs font-semibold group-hover:text-gray-100").text

                gamesArray.append(gameDict)

    return gamesArray




if __name__ == "__main__":
    # getNews()
    print(getGames())
    #print(getLastGames())