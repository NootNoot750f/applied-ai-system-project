"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def display_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Display recommendations for a user profile in a formatted way."""
    print("\n" + "=" * 60)
    print(f"User Profile: {user_prefs['genre']}, {user_prefs['mood']}, energy={user_prefs['energy']:.2f}, tempo={user_prefs['tempo_bpm']} BPM")
    print("=" * 60)
    print("\nTOP 5 RECOMMENDATIONS:\n")

    # Display each recommendation with ranking, formatting, and separators
    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}/10.00")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define multiple user profiles for testing
    profiles = {
        "High-Energy Pop Fan": {"genre": "pop", "mood": "happy", "energy": 0.85, "tempo_bpm": 120},
        "Chill Lofi Relaxer": {"genre": "lofi", "mood": "chill", "energy": 0.30, "tempo_bpm": 90},
        "Intense Rock Fan": {"genre": "rock", "mood": "intense", "energy": 0.90, "tempo_bpm": 135},
        "Conflicted High-Energy Sad": {"genre": "metal", "mood": "sad", "energy": 0.85, "tempo_bpm": 140},
        "Laser-Focused Lofi Relaxer": {"genre": "lofi", "mood": "relaxed", "energy": 0.20, "tempo_bpm": 85},
        "Slow Paradox User": {"genre": "ambient", "mood": "chill", "energy": 0.0, "tempo_bpm": 180},
    }

    # Test each profile
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        display_recommendations(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
