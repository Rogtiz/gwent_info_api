import httpx
import pycountry
from bs4 import BeautifulSoup
from collections import OrderedDict
import datetime
import time

from app.gwent.dao import PlayersDAO
from app.bot.dao import PropertiesDAO

FACTIONS = {
    'Nilfgaard': '🔆 NG',
    'Scoiatael': '🐿 ST',
    'Syndicate': '💰 SY',
    'Monster': '👹 MO',
    'NorthernKingdom': '⚜️ NR',
    'Skellige': '⚓ SK'
}

# SEASON_ID = await PropertiesDAO.find_one_or_none(name="season_id").value
API_RANK_URL = 'https://gwent-rankings.gog.com/ranked_2_0/seasons/'


def get_country_flag(code: str) -> str:
    return pycountry.countries.get(alpha_2=code).flag


class GwentAPI:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_user_id(self, username: str) -> str | None:
        url = f'https://tournaments.playgwent.com/api/user/search/{username}'
        r = await self.client.get(url)
        if r.status_code == 200:
            data = r.json()
            if data:
                user_id = data[0]['id']
                await PlayersDAO.add_player_if_not_exists(user_id)
                return user_id

        token_resp = await self.client.get('https://auth.gog.com/token', params={
            'grant_type': 'password',
            'username': 'Gwent_Helper',
            'password': 'edwardRA1911',
            'client_id': '48242550540196492',
            'client_secret': 'd9571bba9c10784309a98aa59816696d018c445a0e7b8f979921fba639817392'
        })

        if token_resp.status_code == 200:
            token = token_resp.json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            user_resp = await self.client.get(f'https://users.gog.com/users?username={username}', headers=headers)
            if user_resp.status_code == 200:
                data = user_resp.json()
                PlayersDAO.add_player_if_not_exists(data['id'])
                return data['id']

        return None

    async def get_ranking_info(self, user_id: str, season_id: str) -> dict | None:
        url = f'{API_RANK_URL}{season_id}/users/{user_id}?_version=27'
        resp = await self.client.get(url)
        if resp.status_code == 200:
            return resp.json()
        return None

    async def get_profile_data(self, user_id: str) -> dict | None:
        url = f'https://gwent-profile.gog.com/users/{user_id}/public?_version=27'
        r = await self.client.get(url)
        if r.status_code == 200:
            return r.json()
        return None

    async def get_card_collection(self, user_id: str) -> dict | None:
        url = f'https://gwent-deck.gog.com/users/{user_id}/cards/public'
        params = {
            "_data_version": "111000",
            "_data_version_token": "6542314",
            "_version": "30",
            "build_region": "Global"
        }
        r = await self.client.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        return None

    async def get_profile_page(self, username: str) -> BeautifulSoup | bool:
        url = f"https://www.playgwent.com/en/profile/{username}"
        r = await self.client.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            if soup.find('h2', class_='icon-private'):
                return False
            return soup
        return False

    async def get_ranking_site_info(self) -> list | bool:
        now = datetime.datetime.now()
        month_name = now.strftime("%B").lower()
        year = now.year
        url = f"https://masters.playgwent.com/en/rankings/gwentfinity-1/{month_name}-season-{year}"

        data = []
        r1 = await self.client.get(url)
        if r1.status_code == 200:
            soup = BeautifulSoup(r1.content, 'html.parser')
            rows = soup.select('div.c-ranking-table__body > div.c-ranking-table__tr')
            data.extend(rows)

            r2 = await self.client.get(url + "/1/2")
            if r2.status_code == 200:
                soup2 = BeautifulSoup(r2.content, 'html.parser')
                rows2 = soup2.select('div.c-ranking-table__body > div.c-ranking-table__tr')
                data.extend(rows2)
                return data
        return False


class GwentProfileParser:
    def format_collection(self, username: str, user_data: dict) -> str:
        username = username.replace("_", "\\_")
        info = {
            'Neutral': {},
            '🔆 NG': {}, '🐿 ST': {}, '💰 SY': {},
            '👹 MO': {}, '⚜️ NR': {}, '⚓ SK': {}
        }

        all_current = all_total = 0
        for type_card, factions in user_data['collection']['AllCards'].items():
            for faction, val in factions.items():
                if type_card == 'any':
                    all_current += val
                if faction == 'Neutral':
                    info['Neutral'][type_card] = val
                else:
                    info[FACTIONS[faction]][type_card] = val

        for type_card, factions in user_data['full_collection']['AllCards'].items():
            for faction, val in factions.items():
                if type_card == 'any':
                    all_total += val
                if faction == 'Neutral':
                    info['Neutral'][f"{type_card}_overall"] = val
                else:
                    info[FACTIONS[faction]][f"{type_card}_overall"] = val

        result = f"Nickname: {username}\n```\nFaction - Default - Premium - All\n\n"
        neutral = info['Neutral']
        result += f"Neutral: {neutral['non_premium']}/{neutral['non_premium_overall']} - {neutral['premium']}/{neutral['premium_overall']} - {neutral['any']}/{neutral['any_overall']}\n\n"
        info.pop('Neutral')
        info = OrderedDict(sorted(info.items(), key=lambda x: x[1].get('any', 0), reverse=True))
        for faction, cards in info.items():
            result += f"{faction}: {cards['non_premium']}/{cards['non_premium_overall']} - {cards['premium']}/{cards['premium_overall']} - {cards['any']}/{cards['any_overall']}\n"
        result += f"\nAll: {all_current}/{all_total}\n```"
        return result