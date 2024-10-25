def format_anime_message(anime_data):
    msg = f"🔸Title: {anime_data['russian']} \n"
    msg += f"🇯🇵Original Title: {anime_data['name']} \n"
    msg += f"🌟 Score: {anime_data['score']} \n"
    msg += f"📊Status: {anime_data['status']}  \n"
    msg += f"📺episodes: {anime_data['episodes']} \n"
    msg += f"📜genres: {', '.join([x.get('russian') for x in anime_data.get('genres')])} \n"
    msg += f"📆Realese: {anime_data['releasedOn']['year']} \n"
    poster = f"{anime_data['poster']['originalUrl']}"

    return msg, poster
