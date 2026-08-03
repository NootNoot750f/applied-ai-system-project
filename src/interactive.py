"""
Interactive Adaptive Music Recommender

Use the system yourself: input your preferences, get recommendations,
tell the system which songs you like/skip, and watch it learn.
"""

from recommender import AdaptiveRecommender, load_songs
import os

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.csv')
    songs = load_songs(data_path)
    recommender = AdaptiveRecommender(songs)

    print("\n" + "="*70)
    print("ADAPTIVE MUSIC RECOMMENDER - Interactive Mode")
    print("="*70)
    print("\nWelcome! This recommender learns from your feedback.\n")

    # Get user preferences
    print("Tell me your preferences:")
    genre = input("  Favorite genre (e.g., pop, lofi, rock): ").strip()
    mood = input("  Favorite mood (e.g., happy, chill, intense): ").strip()
    try:
        energy = float(input("  Target energy level (0.0-1.0): ").strip())
        tempo = float(input("  Target tempo in BPM (e.g., 120): ").strip())
    except ValueError:
        print("Invalid input. Using defaults: energy=0.5, tempo=100")
        energy, tempo = 0.5, 100

    user_prefs = {"genre": genre, "mood": mood, "energy": energy, "tempo_bpm": tempo}

    print(f"\nProfile: {genre}, {mood}, energy={energy}, tempo={tempo} BPM")

    # Main loop
    round_num = 0
    while True:
        round_num += 1
        print(f"\n{'='*70}")
        print(f"ROUND {round_num}: Recommendations")
        print(f"{'='*70}\n")

        # Get recommendations
        recommendations = recommender.recommend(user_prefs, k=5)

        # Display them
        for rank, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}/10.00")
            print(f"   {explanation}\n")

        # Get feedback
        print("Which songs did you like? (enter song numbers separated by space, or 'none')")
        liked_input = input("  Liked: ").strip().lower()

        print("Which songs did you skip? (enter song numbers, or 'none')")
        skipped_input = input("  Skipped: ").strip().lower()

        # Parse feedback
        liked_ids = []
        skipped_ids = []

        if liked_input != "none":
            try:
                liked_ranks = [int(x) for x in liked_input.split()]
                liked_ids = [recommendations[i-1][0]['id'] for i in liked_ranks if 0 < i <= len(recommendations)]
            except:
                pass

        if skipped_input != "none":
            try:
                skipped_ranks = [int(x) for x in skipped_input.split()]
                skipped_ids = [recommendations[i-1][0]['id'] for i in skipped_ranks if 0 < i <= len(recommendations)]
            except:
                pass

        # Learn from feedback
        if liked_ids or skipped_ids:
            print(f"\nLearning from your feedback ({len(liked_ids)} liked, {len(skipped_ids)} skipped)...")
            recommender.learn_from_feedback(user_prefs, liked_ids, skipped_ids)

            # Show weight changes
            if round_num > 1:
                prev_weights = recommender.weight_history[-2]
                curr_weights = recommender.weight_history[-1]
                print(f"  Mood:   {prev_weights['mood']:.2f} -> {curr_weights['mood']:.2f}")
                print(f"  Genre:  {prev_weights['genre']:.2f} -> {curr_weights['genre']:.2f}")
                print(f"  Energy: {prev_weights['energy']:.2f} -> {curr_weights['energy']:.2f}")
                print(f"  Tempo:  {prev_weights['tempo']:.2f} -> {curr_weights['tempo']:.2f}")
        else:
            print("No feedback provided. Weights unchanged.")

        # Continue?
        again = input("\nGet more recommendations? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            break

    print("\n" + "="*70)
    print("Thanks for using the Adaptive Recommender!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
