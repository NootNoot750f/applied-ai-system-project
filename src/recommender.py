from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_tempo_bpm: float
    likes_acoustic: bool
    liked_song_ids: Optional[List[int]] = None
    skipped_song_ids: Optional[List[int]] = None

    def __post_init__(self):
        if self.liked_song_ids is None:
            self.liked_song_ids = []
        if self.skipped_song_ids is None:
            self.skipped_song_ids = []

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends the top k songs for a user based on preference matching.

        Args:
            user: UserProfile object with user preferences
            k: Number of top recommendations to return (default 5)

        Returns:
            List of top k Song objects sorted by score descending
        """
        # Convert UserProfile to dict format expected by score_song()
        user_prefs = {
            'mood': user.favorite_mood,
            'genre': user.favorite_genre,
            'energy': user.target_energy,
            'tempo_bpm': user.target_tempo_bpm
        }

        # Score all songs and collect (song, score) pairs
        scored_songs = []
        for song in self.songs:
            # Convert Song object to dict
            song_dict = {
                'mood': song.mood,
                'genre': song.genre,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm
            }
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))

        # Sort by score (highest first) and return top k Song objects
        sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        return [song for song, score in sorted_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a particular song is recommended for a user.

        Args:
            user: UserProfile object with user preferences
            song: Song object to explain

        Returns:
            Formatted explanation string with score and reasoning breakdown
        """
        # Convert UserProfile to dict format expected by score_song()
        user_prefs = {
            'mood': user.favorite_mood,
            'genre': user.favorite_genre,
            'energy': user.target_energy,
            'tempo_bpm': user.target_tempo_bpm
        }

        # Convert Song object to dict
        song_dict = {
            'mood': song.mood,
            'genre': song.genre,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm
        }

        # Get score and reasons
        score, reasons = score_song(user_prefs, song_dict)
        explanation_str = ", ".join(reasons)

        # Format and return explanation
        return f"Score: {score}/10.0. Reasons: {explanation_str}"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of song dictionaries with numeric values converted."""
    import csv

    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the 10-point algorithm.

    Scoring Breakdown:
      - Mood Match: 3.5 points (exact match) or 0
      - Genre Match: 2.5 points (exact match) or 0
      - Energy Closeness: 2.5 (within ±0.15), 1.5 (within ±0.30), or 0
      - Tempo Closeness: 1.5 (within ±20 BPM), 1.0 (within ±40 BPM), or 0

    Args:
        user_prefs: Dict with keys 'mood', 'genre', 'energy', 'tempo_bpm'
        song: Dict with song attributes including 'mood', 'genre', 'energy', 'tempo_bpm'

    Returns:
        Tuple of (score, reasons) where score is float (0-10.0) and reasons is list of explanation strings
    """
    score = 0.0
    reasons = []

    # Mood Match: 3.5 points
    if song['mood'] == user_prefs['mood']:
        score += 3.5
        reasons.append("mood match (+3.5)")
    else:
        reasons.append("mood mismatch (0)")

    # Genre Match: 2.5 points
    if song['genre'] == user_prefs['genre']:
        score += 2.5
        reasons.append("genre match (+2.5)")
    else:
        reasons.append("genre mismatch (0)")

    # Energy Closeness: 2.5, 1.5, or 0 points
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    if energy_distance <= 0.15:
        score += 2.5
        reasons.append("energy perfect match (+2.5)")
    elif energy_distance <= 0.30:
        score += 1.5
        reasons.append("energy close (+1.5)")
    else:
        reasons.append("energy mismatch (0)")

    # Tempo Closeness: 1.5, 1.0, or 0 points
    tempo_distance = abs(song['tempo_bpm'] - user_prefs['tempo_bpm'])
    if tempo_distance <= 20:
        score += 1.5
        reasons.append("tempo perfect match (+1.5)")
    elif tempo_distance <= 40:
        score += 1.0
        reasons.append("tempo close (+1.0)")
    else:
        reasons.append("tempo mismatch (0)")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Recommends the top k songs for a user based on preference matching.

    Algorithm:
      1. Score each song using score_song()
      2. Collect results as (song_dict, score, explanation_string)
      3. Sort by score in descending order
      4. Return top k results

    Args:
        user_prefs: Dict with user preferences (mood, genre, energy, tempo_bpm)
        songs: List of song dicts to evaluate
        k: Number of top recommendations to return (default 5)

    Returns:
        List of (song_dict, score, explanation_str) tuples sorted by score descending
    """
    # Score all songs and build result tuples
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    # Sort by score (highest first) using sorted() and return top k
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]

# Example user profiles for testing
def create_example_users() -> Dict[str, UserProfile]:
    """
    Returns a dictionary of example user profiles with different tastes.
    """
    return {
        "upbeat_kpop_fan": UserProfile(
            favorite_genre="kpop",
            favorite_mood="upbeat",
            target_energy=0.75,
            target_tempo_bpm=125,
            likes_acoustic=False
        ),
        "chill_lofi_listener": UserProfile(
            favorite_genre="lofi",
            favorite_mood="chill",
            target_energy=0.35,
            target_tempo_bpm=75,
            likes_acoustic=True
        ),
    }
