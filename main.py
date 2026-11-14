import requests

# Базовый URL для всех запросов к Jikan API v4
BASE_URL = "https://api.jikan.moe/v4"


def get_genre_id(genre_name):
    """Запрашивает список всех жанров и возвращает ID для искомого названия."""
    try:
        response = requests.get(f"{BASE_URL}/genres/anime", timeout=10)
        response.raise_for_status()
        genres_data = response.json()["data"]
    except requests.RequestException as e:
        print(f"Ошибка при получении списка жанров: {e}")
        return None

    # Ищем жанр без учёта регистра и лишних пробелов
    search_name = genre_name.strip().lower()
    for genre in genres_data:
        if genre["name"].lower() == search_name:
            return genre["mal_id"]

    return None


def find_anime_by_genre(genre_id, limit=5):
    """Ищет аниме по ID жанра и выводит названия и оценки."""
    params = {
        "genres": genre_id,
        "limit": limit,
        "order_by": "score",   # Сортируем по рейтингу
        "sort": "desc",
        "sfw": True,           # Исключаем взрослый контент
    }

    try:
        response = requests.get(f"{BASE_URL}/anime", params=params, timeout=10)
        response.raise_for_status()
        anime_list = response.json()["data"]
    except requests.RequestException as e:
        print(f"Ошибка при поиске аниме: {e}")
        return

    if not anime_list:
        print("По этому жанру ничего не найдено.")
        return

    print(f"\n--- Топ-{len(anime_list)} аниме в этом жанре ---")
    for anime in anime_list:
        title = anime.get("title") or "Без названия"
        score = anime.get("score") or "Н/Д"
        year = anime.get("year") or "—"
        episodes = anime.get("episodes") or "—"
        print(f"{title} | {year} | эп.: {episodes} | рейтинг: {score}")


def main():
    user_genre = input("Введите жанр аниме (например, Action, Comedy, Romance): ")

    genre_id = get_genre_id(user_genre)
    if genre_id is None:
        print(f"Жанр '{user_genre}' не найден. Попробуйте другое название (на английском).")
        return

    print(f"Жанр найден (ID: {genre_id}). Ищу аниме...")
    find_anime_by_genre(genre_id)


if __name__ == "__main__":
    main()