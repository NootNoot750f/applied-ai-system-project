"""
Adversarial and Edge-Case User Profiles for Music Recommendation System Testing

These profiles are designed to stress-test the 10-point weighted scoring algorithm:
- Mood match: 3.5 points (exact match only)
- Genre match: 2.5 points (exact match only)
- Energy closeness: 2.5 points (±0.15), 1.5 (±0.30), 0 (else)
- Tempo closeness: 1.5 points (±20 BPM), 1.0 (±40 BPM), 0 (else)

Total max score: 10.0 points
"""

from src.recommender import UserProfile

# ==============================================================================
# ADVERSARIAL PROFILES (5-7)
# ==============================================================================

# 1. CONTRADICTORY PREFERENCES: High-Energy + Sad Mood
CONFLICTED_HIGH_ENERGY_SAD = UserProfile(
    favorite_genre="metal",
    favorite_mood="sad",
    target_energy=0.85,
    target_tempo_bpm=140,
    likes_acoustic=False
)
"""
WHY IT'S ADVERSARIAL:
- Tests conflicting emotional states: sad mood typically pairs with low energy,
  but this user wants high energy.
- Exposes whether the system can find songs that satisfy contradictory dimensions.
- In real data, sad + high-energy songs are rare; tests handling of mismatches.
- Mood and Genre are worth 6 points total; energy/tempo worth 4. When mood conflicts
  with energy, the system must choose which to prioritize or find rare hybrids.
- Metal + Sad is a reasonable combo, so genre + mood can both match if we find
  the right high-energy sad metal track.
"""

# 2. EXTREMELY NARROW: Only Lofi + Relaxed (laser-focused preferences)
LASER_FOCUSED_LOFI_RELAXER = UserProfile(
    favorite_genre="lofi",
    favorite_mood="relaxed",
    target_energy=0.20,
    target_tempo_bpm=85,
    likes_acoustic=True
)
"""
WHY IT'S ADVERSARIAL:
- Tests whether the system can find recommendations for an extremely specific niche.
- If the dataset has few lofi-relaxed songs, recommendations will be poor.
- Exposes potential overfitting: system must balance exact matches with fallbacks.
- Low energy (0.20) with 85 BPM is realistic for lofi, but reduces song pool.
- Likes_acoustic=True adds another constraint; tests multi-dimensional filtering.
"""

# 3. EDGE CASE: Minimum Energy + Maximum Tempo (Contradictory Extremes)
SLOW_PARADOX_USER = UserProfile(
    favorite_genre="ambient",
    favorite_mood="chill",
    target_energy=0.0,
    target_tempo_bpm=180,
    likes_acoustic=False
)
"""
WHY IT'S ADVERSARIAL:
- Energy=0.0 is an extreme edge value (minimum possible).
- Tempo=180 is an extreme edge value (fast, typically rock/metal territory).
- This is physically contradictory: can't be both chill (0.0 energy) AND 180 BPM.
- Tests how scoring handles edge values and unrealistic combinations.
- Energy scoring will fail (distance > 0.30, 0 points) unless a rare ambient-180BPM song exists.
- Ambient genre is slow; system must choose between genre match or tempo match.
"""

# 4. EDGE CASE: Maximum Energy + Minimum Tempo (Another Contradiction)
ENERGETIC_BALLAD_LOVER = UserProfile(
    favorite_genre="soul",
    favorite_mood="energetic",
    target_energy=1.0,
    target_tempo_bpm=40,
    likes_acoustic=True
)
"""
WHY IT'S ADVERSARIAL:
- Energy=1.0 is maximum possible (hyperactive/extreme intensity).
- Tempo=40 is very slow (ballad territory, jazz, ambient).
- Contradictory: high-energy + slow tempo is uncommon in real music.
- Tests scoring of impossible-to-satisfy preference combinations.
- Soul genre can work with either energy or tempo, but usually mid-range.
- Energy closeness will fail (distance > 0.30) for most normal songs.
- Exposes whether system penalizes users fairly for unrealistic preferences.
"""

# 5. RARE MOOD-GENRE PAIRING: Aggressive + Ambient (Oxymoronic)
AGGRESSIVE_AMBIENT_SEEKER = UserProfile(
    favorite_genre="ambient",
    favorite_mood="aggressive",
    target_energy=0.75,
    target_tempo_bpm=110,
    likes_acoustic=False
)
"""
WHY IT'S ADVERSARIAL:
- Aggressive mood in ambient genre is extremely rare/oxymoronic.
- Ambient music is typically relaxing; aggressive ambient is niche experimental.
- Tests whether system can handle non-standard combinations that rarely exist in data.
- Genre + Mood matching will likely get 0 points (mismatch on both or just mood).
- Energy (0.75) and tempo (110) are moderate; system must compensate with these.
- Exposes potential bias: does system assume mood+genre correlation exists?
- Real use case: experimental/industrial ambient fans.
"""

# 6. UNDERREPRESENTED MOOD: Nostalgic + Metal (Genre-Mood Mismatch)
NOSTALGIC_METAL_FAN = UserProfile(
    favorite_genre="metal",
    favorite_mood="nostalgic",
    target_energy=0.8,
    target_tempo_bpm=135,
    likes_acoustic=False
)
"""
WHY IT'S ADVERSARIAL:
- Nostalgic mood is typically paired with softer genres (indie pop, soul, lofi).
- Metal + nostalgic is unconventional (thrash metal nostalgia? 80s cover bands?).
- Tests system's ability to find songs in underrepresented mood categories.
- If nostalgic songs are rare in dataset, system will score poorly.
- Genre match possible (metal), but mood match unlikely (0 points).
- Energy and tempo are realistic for metal, so system relies on these 4 points.
- Exposes mood distribution bias: does the algorithm fail for rare mood+genre pairs?
"""

# 7. MULTI-CONFLICTING: Romantic + Intense + High-Energy + Fast
INTENSE_ROMANTIC_SPRINTER = UserProfile(
    favorite_genre="electronic",
    favorite_mood="romantic",
    target_energy=0.90,
    target_tempo_bpm=160,
    likes_acoustic=False
)
"""
WHY IT'S ADVERSARIAL:
- Romantic mood typically expects lower energy and slower tempo (soft, intimate).
- Target energy 0.90 is very high; tempo 160 is fast/energetic.
- Tests contradictory emotional dimensions: romance ≠ intense + high-energy.
- Electronic genre CAN support this (EDM, synth-pop), but rare to find true match.
- All 4 elements (mood, genre, energy, tempo) are in tension.
- Forces the algorithm to choose: satisfy mood OR energy/tempo dimensions.
- Exposes whether weighting (3.5 mood + 2.5 genre = 6 points) overwhelms energy/tempo.
"""

# ==============================================================================
# BASELINE PROFILES (2-3 "Normal" Cases)
# ==============================================================================

# Baseline 1: High-Energy Pop (Classic Happy Listener)
HIGH_ENERGY_POP_FAN = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.85,
    target_tempo_bpm=120,
    likes_acoustic=False
)
"""
WHY IT'S A BASELINE:
- Pop + happy is a standard, well-represented combination.
- High energy (0.85) and tempo (120) are typical for pop music.
- System should easily find 5+ perfect matches (3.5+2.5+2.5+1.5 = 10 points possible).
- Represents the "happy path" - normal user with conventional taste.
- Good control for verifying basic recommendation quality.
"""

# Baseline 2: Chill Lofi Listener (Classic Relaxation)
CHILL_LOFI_RELAXER = UserProfile(
    favorite_genre="lofi",
    favorite_mood="chill",
    target_energy=0.30,
    target_tempo_bpm=90,
    likes_acoustic=True
)
"""
WHY IT'S A BASELINE:
- Lofi + chill is extremely common and well-represented in modern datasets.
- Low energy (0.30) and moderate tempo (90) match lofi characteristics perfectly.
- Should achieve near-perfect scores for many songs in dataset.
- Represents "relaxation" listening; straightforward preference matching.
- Easy baseline to verify correct scoring algorithm implementation.
"""

# Baseline 3: Intense Rock Fan (Classic High-Intensity)
INTENSE_ROCK_FAN = UserProfile(
    favorite_genre="rock",
    favorite_mood="intense",
    target_energy=0.90,
    target_tempo_bpm=135,
    likes_acoustic=False
)
"""
WHY IT'S A BASELINE:
- Rock + intense is standard and very well-represented in music datasets.
- High energy (0.90) and fast tempo (135) are typical rock characteristics.
- Should easily find perfect or near-perfect matches.
- Represents "energetic" listening; validates energy/tempo scoring.
- Good baseline for verifying the system works for different mood types.
"""

# ==============================================================================
# SUMMARY & TESTING STRATEGY
# ==============================================================================

ADVERSARIAL_PROFILES = {
    "conflicted_high_energy_sad": CONFLICTED_HIGH_ENERGY_SAD,
    "laser_focused_lofi_relaxer": LASER_FOCUSED_LOFI_RELAXER,
    "slow_paradox_user": SLOW_PARADOX_USER,
    "energetic_ballad_lover": ENERGETIC_BALLAD_LOVER,
    "aggressive_ambient_seeker": AGGRESSIVE_AMBIENT_SEEKER,
    "nostalgic_metal_fan": NOSTALGIC_METAL_FAN,
    "intense_romantic_sprinter": INTENSE_ROMANTIC_SPRINTER,
}

BASELINE_PROFILES = {
    "high_energy_pop_fan": HIGH_ENERGY_POP_FAN,
    "chill_lofi_relaxer": CHILL_LOFI_RELAXER,
    "intense_rock_fan": INTENSE_ROCK_FAN,
}

"""
TESTING STRATEGY:

1. Run each adversarial profile through the recommender.
2. Check if recommendations make sense (or gracefully fail).
3. Compare scores: adversarial profiles should score LOWER on average than baselines.
4. Validate edge cases:
   - Zero energy/tempo recommendations exist?
   - System handles contradictory preferences by picking "best compromise"?
   - Rare mood+genre combos don't crash or return empty results?

5. Scoring algorithm validation:
   - Check if mood matching (3.5 points) overshadows energy/tempo (4 points total).
   - Verify energy closeness thresholds (±0.15 vs ±0.30) are enforced.
   - Verify tempo closeness thresholds (±20 vs ±40 BPM) are enforced.

6. Bias detection:
   - Do baselines consistently score 8-10 points?
   - Do adversarial profiles score 4-6 points (partial matches)?
   - Are underrepresented moods (nostalgic) penalized unfairly?

7. Edge case handling:
   - What happens when NO song exists for a user's preferences?
   - Does the system return empty list or partial matches?
   - Are there ties (multiple songs with same score)?
"""

if __name__ == "__main__":
    print("Adversarial Profiles:")
    for name, profile in ADVERSARIAL_PROFILES.items():
        print(f"  {name}: {profile}")
    print("\nBaseline Profiles:")
    for name, profile in BASELINE_PROFILES.items():
        print(f"  {name}: {profile}")