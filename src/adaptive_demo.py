"""
Agentic Demo: Music Recommender That Learns from Feedback

This script demonstrates the AdaptiveRecommender learning and improving
its recommendations over multiple user interactions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import AdaptiveRecommender, load_songs
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def display_recommendations(title: str, recommendations, iteration: int):
    """Display recommendations in a readable format."""
    print(f"\n{'='*70}")
    print(f"{title} (Iteration {iteration})")
    print(f"{'='*70}\n")
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}/10.00")
        print(f"   {explanation}\n")

def main():
    """Run adaptive recommender demo."""
    print("\n" + "="*70)
    print("ADAPTIVE MUSIC RECOMMENDER DEMO")
    print("Demonstrates agentic workflow: Plan -> Act -> Check -> Adapt")
    print("="*70)

    # Load songs
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.csv')
    songs = load_songs(data_path)
    print(f"\nLoaded {len(songs)} songs from database.")

    # Create adaptive recommender
    recommender = AdaptiveRecommender(songs)
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.80, "tempo_bpm": 120}

    print(f"\nUser Profile: {user_prefs['genre']}, {user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, tempo={user_prefs['tempo_bpm']} BPM")

    # ITERATION 1: Initial recommendations
    print(f"\n[ITERATION 1] PLAN >> Generate initial recommendations")
    recommendations_1 = recommender.recommend(user_prefs, k=5)
    display_recommendations("INITIAL RECOMMENDATIONS", recommendations_1, 1)

    # ITERATION 1: User feedback
    print("[ITERATION 1] CHECK >> User provides feedback")
    liked = [recommendations_1[0][0]['id'], recommendations_1[1][0]['id']]  # Liked top 2
    skipped = [recommendations_1[4][0]['id']]  # Skipped last one
    print(f"[LIKED] User enjoyed songs: {[recommendations_1[i][0]['title'] for i in [0,1]]}")
    print(f"[SKIPPED] User passed on: {recommendations_1[4][0]['title']}")

    # ITERATION 1: Adapt weights
    print("\n[ITERATION 1] ADAPT >> System adjusts weights based on feedback")
    recommender.learn_from_feedback(user_prefs, liked, skipped)

    # ITERATION 2: Improved recommendations
    print(f"\n[ITERATION 2] PLAN >> Generate improved recommendations with new weights")
    recommendations_2 = recommender.recommend(user_prefs, k=5)
    display_recommendations("RECOMMENDATIONS (After Learning Round 1)", recommendations_2, 2)

    # ITERATION 2: More feedback
    print("[ITERATION 2] CHECK >> User provides more feedback")
    liked_2 = [recommendations_2[0][0]['id']]
    skipped_2 = [recommendations_2[3][0]['id'], recommendations_2[4][0]['id']]
    print(f"[LIKED] User enjoyed: {recommendations_2[0][0]['title']}")
    print(f"[SKIPPED] User passed on: {recommendations_2[3][0]['title']}, {recommendations_2[4][0]['title']}")

    # ITERATION 2: Adapt again
    print("\n[ITERATION 2] ADAPT >> System adjusts weights again")
    recommender.learn_from_feedback(user_prefs, liked_2, skipped_2)

    # ITERATION 3: Final recommendations
    print(f"\n[ITERATION 3] PLAN >> Generate final recommendations with refined weights")
    recommendations_3 = recommender.recommend(user_prefs, k=5)
    display_recommendations("RECOMMENDATIONS (After Learning Round 2)", recommendations_3, 3)

    # Summary
    print("\n" + "="*70)
    print("LEARNING SUMMARY")
    print("="*70)
    print(f"\nWeight Evolution:")
    for i, weights in enumerate(recommender.weight_history):
        print(f"  Round {i}: mood={weights['mood']:.2f}, genre={weights['genre']:.2f}, "
              f"energy={weights['energy']:.2f}, tempo={weights['tempo']:.2f}")

    print(f"\nFeedback History:")
    for i, feedback in enumerate(recommender.feedback_history, 1):
        print(f"  Round {i}: {feedback['liked']} liked, {feedback['skipped']} skipped")
        print(f"    >> Weights adjusted: {feedback['weights_before']} >> {feedback['weights_after']}")

    print("\n" + "="*70)
    print("DEMO COMPLETE: System successfully learned and improved recommendations!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
