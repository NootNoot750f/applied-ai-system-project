"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "tempo_bpm": 120}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Display user profile
    print("\n" + "=" * 60)
    print(f"User Profile: {user_prefs['genre']}, {user_prefs['mood']}, energy={user_prefs['energy']:.2f}")
    print("=" * 60)
    print("\nTOP 5 RECOMMENDATIONS:\n")

    # Display each recommendation with ranking, formatting, and separators
    for rank, rec in enumerate(recommendations, 1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}/10.00")
        print(f"   Reasons: {explanation}")
        print()  # Blank line between recommendations


if __name__ == "__main__":
    main()
