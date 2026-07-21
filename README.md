# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

The recommender works by scoring each song against the user's taste profile. For every song, we check four features: does the genre match (40%), does the mood match (35%), is the energy level similar to what they like (20%), and is the tempo close (5%)? Each comparison gets a score from 0-1, and we add them up weighted to get a final score. Then we sort songs by score (highest first) and recommend the best matches, while adding some variety to keep recommendations interesting.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

  In my feature, the songs will use Mood, Genre, Energy and Tempo in that order.

- What information does your `UserProfile` store
  The user profile will store things such as Preferred Genre, Prefered Mood, Prefered Energy Level, Prefered Tempo, and the history: songs they have liked, disliked, skipped, or added to playlists.

- How does your `Recommender` compute a score for each song
  It will have different matches with different weights for each feature of the song

**Mood Match** 3.5 Full points if mood matches; 0 if it doesn't
**Genre Match** 2.5 Full points if genre matches; 0 if it doesn't
**Energy Closeness** | 2.5 | 2.5 pts if within ±0.15 of target energy; 1.5 pts if close; 0 if far
**Tempo Closeness** | 1.5 | 1.5 pts if within ±20 BPM of target; 1.0 pts if close; 0 if far |

Why these weights? Mood is weighted highest (3.5) because it differentiates songs within the same genre—for example, upbeat K-pop vs. metallic K-pop both match the genre but feel very different. Genre and energy are equally weighted (2.5 each) because they're both fundamental to matching taste. Tempo is lowest (1.5) because it's a refinement signal.

- How do you choose which songs to recommend

1. Score all the songs using the system above.
2. Sort by score from highest to lowest; these will be the best matches
3. Add variety: The top 10 identical songs wont be the only ones recomended; there will be songs mixed in from different moods or artists to keep the user interested
4. Boost discovery: Including a few lwer scoring songs that might surprise by giving something they have never heard and might like
5. Return the top recommendations in this order.

### Potential Biases & Limitations

This system has some blind spots:

- Genre-mood coupling: If a user likes pop + happy, they'll miss intense pop songs they might love. Mood dominance (3.5 pts) could mask great genre matches.
- No lyrical understanding: The system only sees genre/mood tags, not actual song content, lyrics, or artist quality.
- No collaborative signals: Unlike Spotify, this system doesn't know "50,000 users like this song"—it only uses content features.
- Popularity bias: Popular songs in the dataset might not be better recommendations, just more common.
- Cold start problem: New songs with no tags won't be recommended until they have mood/genre data.

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running the recommender with default user preferences (pop, happy, energy=0.80, tempo=120 BPM):

```
============================================================
User Profile: pop, happy, energy=0.80
============================================================

TOP 5 RECOMMENDATIONS:

1. Sunrise City by Neon Echo
   Score: 10.00/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Rooftop Lights by Indigo Parade
   Score: 7.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

3. Gym Hero by Max Pulse
   Score: 6.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

4. Night Drive Loop by Neon Echo
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

5. Electric Pulse by Synth Wave Collective
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)
```

**What this shows:**

- The top recommendation "Sunrise City" scores a perfect 10/10 because it matches all four features
- Songs that match mood (happy) score higher even if genre or other features don't match
- The scoring breakdown clearly explains why each song was ranked
- Songs with conflicting moods (intense, moody) rank lower even if other features match

---

## System Evaluation: Multiple User Profiles

### Baseline Profile 1: High-Energy Pop Fan

```
============================================================
User Profile: pop, happy, energy=0.85, tempo=120 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Sunrise City by Neon Echo
   Score: 10.00/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Rooftop Lights by Indigo Parade
   Score: 7.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

3. Gym Hero by Max Pulse
   Score: 6.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

4. Night Drive Loop by Neon Echo
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

5. Electric Pulse by Synth Wave Collective
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)
```

**Analysis:** Perfect match found (10/10). High-energy pop songs dominate. System works as expected.

---

### Baseline Profile 2: Chill Lofi Relaxer

```
============================================================
User Profile: lofi, chill, energy=0.30, tempo=90 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Midnight Coding by LoRoom
   Score: 10.00/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Library Rain by Paper Lanterns
   Score: 10.00/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

3. Spacewalk Thoughts by Orbit Bloom
   Score: 7.00/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy perfect match (+2.5), tempo close (+1.0)

4. Focus Flow by LoRoom
   Score: 6.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

5. Coffee Shop Stories by Slow Stereo
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)
```

**Analysis:** Two perfect matches (10/10 each). Excellent precision for a well-defined niche. Mood + genre + energy alignment creates consistency.

---

### Baseline Profile 3: Intense Rock Fan

```
============================================================
User Profile: rock, intense, energy=0.90, tempo=135 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Storm Runner by Voltline
   Score: 10.00/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Gym Hero by Max Pulse
   Score: 7.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

3. Sunrise City by Neon Echo
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

4. Rooftop Lights by Indigo Parade
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

5. Electric Pulse by Synth Wave Collective
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)
```

**Analysis:** Perfect match found. Note: System prioritizes energy/tempo when genre+mood miss, showing graceful degradation.

---

### Adversarial Profile 1: Conflicted High-Energy Sad (Tests Contradictory Preferences)

```
============================================================
User Profile: metal, sad, energy=0.85, tempo=140 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Thunder Strike by Metal Gods
   Score: 6.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Broken Echoes by Cipher Mind
   Score: 5.00/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy close (+1.5), tempo mismatch (0)

3. Storm Runner by Voltline
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

4. Gym Hero by Max Pulse
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

5. Rooftop Lights by Indigo Parade
   Score: 4.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)
```

**Analysis:** No perfect match found (expected). System splits between genre match + sad mood, showing tension between equally-weighted features. Genre wins (6.5 vs 5.0).

---

### Adversarial Profile 2: Laser-Focused Lofi Relaxer (Tests Niche with Uncommon Mood)

```
============================================================
User Profile: lofi, relaxed, energy=0.20, tempo=85 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Library Rain by Paper Lanterns
   Score: 6.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Coffee Shop Stories by Slow Stereo
   Score: 6.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy close (+1.5), tempo perfect match (+1.5)

3. Midnight Coding by LoRoom
   Score: 5.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy close (+1.5), tempo perfect match (+1.5)

4. Focus Flow by LoRoom
   Score: 5.50/10.00
   Reasons: mood mismatch (0), genre match (+2.5), energy close (+1.5), tempo perfect match (+1.5)

5. Island Breeze by Reggae Vibes
   Score: 5.00/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy mismatch (0), tempo perfect match (+1.5)
```

**Analysis:** No perfect match for "relaxed" mood + lofi (dataset has "chill" but not "relaxed"). System gracefully falls back to genre/energy matches (6.5/10). Shows dataset limitation but doesn't crash.

---

### Adversarial Profile 3: Slow Paradox (Tests Edge Values - Energy 0.0, Extreme Tempo 180)

```
============================================================
User Profile: ambient, chill, energy=0.00, tempo=180 BPM
============================================================

TOP 5 RECOMMENDATIONS:

1. Spacewalk Thoughts by Orbit Bloom
   Score: 7.50/10.00
   Reasons: mood match (+3.5), genre match (+2.5), energy close (+1.5), tempo mismatch (0)

2. Midnight Coding by LoRoom
   Score: 3.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy mismatch (0), tempo mismatch (0)

3. Library Rain by Paper Lanterns
   Score: 3.50/10.00
   Reasons: mood match (+3.5), genre mismatch (0), energy mismatch (0), tempo mismatch (0)

4. Thunder Strike by Metal Gods
   Score: 1.50/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy mismatch (0), tempo perfect match (+1.5)

5. Storm Runner by Voltline
   Score: 1.00/10.00
   Reasons: mood mismatch (0), genre mismatch (0), energy mismatch (0), tempo close (+1.0)
```

**Analysis:** Interesting edge case: user wants 0.0 energy (silent?) and 180 BPM (very fast). No song matches both. System prioritizes mood match (chill) over the paradoxical tempo demand. Top result (7.5) sensibly ignores the extreme tempo in favor of mood/genre/energy alignment. Shows the system makes reasonable tradeoffs.

---

## Key Findings from System Evaluation

1. **Perfect matches (10/10) only occur when all four features align** — very rare in real-world scenarios
2. **Mood has strong influence** — songs with matching mood rank higher even when genre/tempo miss
3. **Graceful degradation works** — system never crashes and always returns recommendations, even for contradictory inputs
4. **Edge cases handled well** — extreme energy (0.0) and tempo (180 BPM) values don't break the algorithm
5. **Dataset limitations exposed** — some mood-genre combinations ("relaxed" + "lofi") don't exist in the 18-song catalog
6. **Weighting priorities clear** — when features conflict, the 10-point system reveals what matters most (mood 3.5 > genre 2.5 > others)

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Bias

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.
The system systematically disadvantages users with extreme energy preferences (0.0 or 1.0) because the ±0.15 tolerance band for perfect energy match is narrow relative to the actual distribution of songs in the dataset. Most songs in the 18-song catalog cluster between 0.35-0.95 energy, leaving users seeking minimal energy (nearly silent) or maximum energy (very loud) unable to find more than 1-2 songs that fit perfectly. While a user preferring mid-range energy (0.5) can find 10+ songs with perfect energy matches and consistently score high, an extreme user loses 1-2 points on nearly every recommendation, effectively creating a filter bubble that excludes outlier preferences from top-ranked results. This reveals a fairness issue: the algorithm is biased toward mainstream taste and penalizes users with statistically rare but valid preferences.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
