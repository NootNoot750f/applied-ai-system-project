from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class RecommenderConfig:
    """Adjustable weights for the recommendation algorithm."""
    mood_weight: float = 3.5
    genre_weight: float = 2.5
    energy_weight: float = 2.5
    tempo_weight: float = 1.5

    def clamp(self) -> None:
        """Prevent weights from drifting outside reasonable bounds (0.1 to 5.0)."""
        self.mood_weight = max(0.1, min(5.0, self.mood_weight))
        self.genre_weight = max(0.1, min(5.0, self.genre_weight))
        self.energy_weight = max(0.1, min(5.0, self.energy_weight))
        self.tempo_weight = max(0.1, min(5.0, self.tempo_weight))

    def total_weight(self) -> float:
        """Get the sum of all weights."""
        return self.mood_weight + self.genre_weight + self.energy_weight + self.tempo_weight

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

def score_song_with_config(user_prefs: Dict, song: Dict, config: RecommenderConfig) -> Tuple[float, List[str]]:
    """
    Scores a song with adjustable weights (used by AdaptiveRecommender).

    Args:
        user_prefs: Dict with keys 'mood', 'genre', 'energy', 'tempo_bpm'
        song: Dict with song attributes
        config: RecommenderConfig with adjustable weights

    Returns:
        Tuple of (score, reasons)
    """
    score = 0.0
    reasons = []

    # Mood Match
    if song['mood'] == user_prefs['mood']:
        score += config.mood_weight
        reasons.append(f"mood match (+{config.mood_weight})")
    else:
        reasons.append("mood mismatch (0)")

    # Genre Match
    if song['genre'] == user_prefs['genre']:
        score += config.genre_weight
        reasons.append(f"genre match (+{config.genre_weight})")
    else:
        reasons.append("genre mismatch (0)")

    # Energy Closeness
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    if energy_distance <= 0.15:
        score += config.energy_weight
        reasons.append(f"energy perfect match (+{config.energy_weight})")
    elif energy_distance <= 0.30:
        score += config.energy_weight * 0.6
        reasons.append(f"energy close (+{config.energy_weight * 0.6:.1f})")
    else:
        reasons.append("energy mismatch (0)")

    # Tempo Closeness
    tempo_distance = abs(song['tempo_bpm'] - user_prefs['tempo_bpm'])
    if tempo_distance <= 20:
        score += config.tempo_weight
        reasons.append(f"tempo perfect match (+{config.tempo_weight})")
    elif tempo_distance <= 40:
        score += config.tempo_weight * 0.67
        reasons.append(f"tempo close (+{config.tempo_weight * 0.67:.1f})")
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

class AdaptiveRecommender:
    """
    Agentic recommender that learns from user feedback and adapts weights.

    Workflow:
    1. PLAN: Start with default weights
    2. ACT: Generate recommendations using current weights
    3. CHECK: User provides feedback (likes/skips)
    4. ADAPT: Analyze feedback and adjust weights
    5. REPEAT: Next round uses improved weights
    """
    def __init__(self, songs: List[Dict], initial_config: Optional[RecommenderConfig] = None):
        self.songs = songs
        self.config = initial_config or RecommenderConfig()
        self.feedback_history = []
        self.weight_history = [self._config_snapshot()]
        logger.info(f"AdaptiveRecommender initialized with weights: {self.weight_history[0]}")

    def _config_snapshot(self) -> Dict[str, float]:
        """Return current config as dict."""
        return {
            'mood': self.config.mood_weight,
            'genre': self.config.genre_weight,
            'energy': self.config.energy_weight,
            'tempo': self.config.tempo_weight
        }

    def recommend(self, user_prefs: Dict, k: int = 5) -> List[Tuple[Dict, float, str]]:
        """Generate recommendations using current weights."""
        scored_songs = []
        for song in self.songs:
            score, reasons = score_song_with_config(user_prefs, song, self.config)
            explanation = ", ".join(reasons)
            scored_songs.append((song, score, explanation))

        recommendations = sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
        logger.info(f"Generated {len(recommendations)} recommendations for user (genre={user_prefs['genre']}, mood={user_prefs['mood']})")
        return recommendations

    def learn_from_feedback(self, user_prefs: Dict, liked_song_ids: List[int], skipped_song_ids: List[int]) -> None:
        """
        Learn from user feedback and adjust weights.

        Strategy:
        - For liked songs: increase weight of features they had
        - For skipped songs: decrease weight of features they had
        - Clamp weights to reasonable bounds
        """
        logger.info(f"Processing feedback: {len(liked_song_ids)} liked, {len(skipped_song_ids)} skipped")

        if not liked_song_ids and not skipped_song_ids:
            logger.info("No feedback to process")
            return

        # Find songs by ID
        liked_songs = [s for s in self.songs if s['id'] in liked_song_ids]
        skipped_songs = [s for s in self.songs if s['id'] in skipped_song_ids]

        # Adjust weights based on liked songs
        mood_boost = 0.0
        genre_boost = 0.0
        energy_boost = 0.0
        tempo_boost = 0.0

        for song in liked_songs:
            if song['mood'] == user_prefs['mood']:
                mood_boost += 0.2
            if song['genre'] == user_prefs['genre']:
                genre_boost += 0.2
            energy_distance = abs(song['energy'] - user_prefs['energy'])
            if energy_distance <= 0.30:
                energy_boost += 0.2
            tempo_distance = abs(song['tempo_bpm'] - user_prefs['tempo_bpm'])
            if tempo_distance <= 40:
                tempo_boost += 0.2

        # Penalize based on skipped songs
        for song in skipped_songs:
            if song['mood'] == user_prefs['mood']:
                mood_boost -= 0.1
            if song['genre'] == user_prefs['genre']:
                genre_boost -= 0.1
            energy_distance = abs(song['energy'] - user_prefs['energy'])
            if energy_distance <= 0.30:
                energy_boost -= 0.1
            tempo_distance = abs(song['tempo_bpm'] - user_prefs['tempo_bpm'])
            if tempo_distance <= 40:
                tempo_boost -= 0.1

        # Apply adjustments
        old_config = self._config_snapshot()
        self.config.mood_weight += mood_boost
        self.config.genre_weight += genre_boost
        self.config.energy_weight += energy_boost
        self.config.tempo_weight += tempo_boost
        self.config.clamp()

        new_config = self._config_snapshot()
        self.weight_history.append(new_config)

        logger.info(f"Weight adjustment: mood {old_config['mood']:.2f}→{new_config['mood']:.2f}, "
                   f"genre {old_config['genre']:.2f}→{new_config['genre']:.2f}, "
                   f"energy {old_config['energy']:.2f}→{new_config['energy']:.2f}, "
                   f"tempo {old_config['tempo']:.2f}→{new_config['tempo']:.2f}")

        self.feedback_history.append({
            'liked': len(liked_song_ids),
            'skipped': len(skipped_song_ids),
            'weights_before': old_config,
            'weights_after': new_config
        })

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
