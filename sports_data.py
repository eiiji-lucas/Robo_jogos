import datetime
import requests
from typing import List, Dict, Any

SPORTS_FILTER = {
    "Soccer": [
        "English Premier League",
        "La Liga",
        "Serie A",
        "Bundesliga",
        "Ligue 1",
        "Brasileirão Série A",
        "MLS",
    ],
    "Basketball": [
        "NBA",
        "EuroLeague",
        "NCAA Men's Basketball",
        "Liga ACB",
        "NBB",
    ],
    "Esports": [
        "VCT",
        "VCT Americas",
        "VCT EMEA",
        "VCT Pacific",
        "Valorant Champions",
    ],
}

BROADCAST_LOGOS = {
    "Disney": "https://upload.wikimedia.org/wikipedia/commons/3/3a/The_Walt_Disney_Company_Logo.svg",
    "HBO": "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_logo.svg",
    "TNT": "https://upload.wikimedia.org/wikipedia/commons/5/5a/TNT_2016_logo.svg",
    "YouTube": "https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg",
}

DEFAULT_LEAGUE_IMAGES = {
    "English Premier League": "https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg",
    "La Liga": "https://upload.wikimedia.org/wikipedia/en/5/56/La_Liga.svg",
    "Serie A": "https://upload.wikimedia.org/wikipedia/en/e/e1/Serie_A_logo_%282019%29.svg",
    "Bundesliga": "https://upload.wikimedia.org/wikipedia/en/d/df/Bundesliga_logo_%282017%29.svg",
    "Ligue 1": "https://upload.wikimedia.org/wikipedia/en/0/04/Ligue1.svg",
    "Brasileirão Série A": "https://upload.wikimedia.org/wikipedia/en/1/18/Campeonato_Brasileiro_S%C3%A9rie_A_logo.svg",
    "MLS": "https://upload.wikimedia.org/wikipedia/en/d/d3/MLS_crest_2014.svg",
    "NBA": "https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg",
    "EuroLeague": "https://upload.wikimedia.org/wikipedia/en/c/cd/Euroleague_Basketball_logo.svg",
    "Liga ACB": "https://upload.wikimedia.org/wikipedia/en/8/8d/ACB_logo.svg",
    "NBB": "https://upload.wikimedia.org/wikipedia/en/0/0c/NBB_logo.svg",
    "VCT": "https://upload.wikimedia.org/wikipedia/en/8/8f/Valorant_Championship_Tour_logo.svg",
    "Valorant Champions": "https://upload.wikimedia.org/wikipedia/en/8/8f/Valorant_Championship_Tour_logo.svg",
}

DEFAULT_BROADCAST = [
    "Disney+",
    "HBO Max",
    "TNT Sports",
    "YouTube",
]


def parse_time(utc_time: str, utc_date: str) -> str:
    try:
        if utc_time and utc_date:
            dt = datetime.datetime.fromisoformat(f"{utc_date} {utc_time}")
            return dt.strftime("%H:%M")
    except ValueError:
        pass
    return utc_time or "--:--"


def build_game_entry(event: Dict[str, Any]) -> Dict[str, Any]:
    sport = event.get("strSport") or "Unknown"
    league = event.get("strLeague") or "Liga desconhecida"
    date_event = event.get("dateEvent") or event.get("dateEventLocal") or ""
    time_event = event.get("strTime") or event.get("strTimeLocal") or ""
    home = event.get("strHomeTeam") or event.get("strTeamHome") or "Time A"
    away = event.get("strAwayTeam") or event.get("strTeamAway") or "Time B"
    description = event.get("strTVStation") or event.get("strChannel") or "Canal não informado"

    return {
        "sport": sport,
        "league": league,
        "time": parse_time(time_event, date_event),
        "home": home,
        "away": away,
        "broadcast": description,
        "image": DEFAULT_LEAGUE_IMAGES.get(league, DEFAULT_LEAGUE_IMAGES.get(sport, "https://upload.wikimedia.org/wikipedia/commons/5/5f/Generic_sports_logo.svg")),
    }


def get_todays_games(api_key: str) -> List[Dict[str, Any]]:
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsday.php?d={date}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        events = data.get("events") or []
    except Exception:
        events = []

    games = []
    for event in events:
        sport = event.get("strSport")
        league = event.get("strLeague")
        if not sport or not league:
            continue

        if sport == "Soccer" and league in SPORTS_FILTER["Soccer"]:
            games.append(build_game_entry(event))
        elif sport == "Basketball" and league in SPORTS_FILTER["Basketball"]:
            games.append(build_game_entry(event))
        elif sport == "Esports" and league in SPORTS_FILTER["Esports"]:
            games.append(build_game_entry(event))

    soccer_games = [game for game in games if game["sport"] == "Soccer"]
    basketball_games = [game for game in games if game["sport"] == "Basketball"]
    esports_games = [game for game in games if game["sport"] == "Esports"]

    if not games:
        games.extend(
            get_sample_soccer_games()
            + get_sample_basketball_games()
            + get_sample_valorant_games()
        )
    else:
        if not soccer_games:
            games.extend(get_sample_soccer_games())
        if not basketball_games:
            games.extend(get_sample_basketball_games())
        if not esports_games:
            games.extend(get_sample_valorant_games())

    games.sort(key=lambda item: item["time"])
    return games


def get_sample_soccer_games() -> List[Dict[str, Any]]:
    return [
        {
            "sport": "Soccer",
            "league": "English Premier League",
            "time": "14:30",
            "home": "Manchester United",
            "away": "Liverpool",
            "broadcast": "Disney+",
            "image": DEFAULT_LEAGUE_IMAGES["English Premier League"],
        },
        {
            "sport": "Soccer",
            "league": "Brasileirão Série A",
            "time": "19:00",
            "home": "Flamengo",
            "away": "Palmeiras",
            "broadcast": "TNT Sports",
            "image": DEFAULT_LEAGUE_IMAGES["Brasileirão Série A"],
        },
    ]


def get_sample_basketball_games() -> List[Dict[str, Any]]:
    return [
        {
            "sport": "Basketball",
            "league": "NBA",
            "time": "21:00",
            "home": "Los Angeles Lakers",
            "away": "Golden State Warriors",
            "broadcast": "HBO Max",
            "image": DEFAULT_LEAGUE_IMAGES["NBA"],
        },
        {
            "sport": "Basketball",
            "league": "EuroLeague",
            "time": "17:45",
            "home": "Real Madrid",
            "away": "FC Barcelona",
            "broadcast": "YouTube",
            "image": DEFAULT_LEAGUE_IMAGES["EuroLeague"],
        },
    ]


def get_sample_valorant_games() -> List[Dict[str, Any]]:
    return [
        {
            "sport": "Esports",
            "league": "VCT EMEA",
            "time": "15:00",
            "home": "Team Falcons",
            "away": "Team Phoenix",
            "broadcast": "YouTube",
            "image": DEFAULT_LEAGUE_IMAGES["VCT"],
        },
        {
            "sport": "Esports",
            "league": "Valorant Champions",
            "time": "20:30",
            "home": "Valor Gaming",
            "away": "Knight Squad",
            "broadcast": "Twitch",
            "image": DEFAULT_LEAGUE_IMAGES["Valorant Champions"],
        },
    ]


def get_broadcast_logo(source: str) -> str:
    for key, logo in BROADCAST_LOGOS.items():
        if key.lower() in source.lower():
            return logo
    return "https://upload.wikimedia.org/wikipedia/commons/5/5f/Generic_sports_logo.svg"
