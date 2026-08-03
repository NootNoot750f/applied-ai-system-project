# 🎵 Adaptive Music Recommender: An Applied AI System

## Original Project Summary

**Base Project**: Music Recommender Simulation (from Module 2)

The original recommender system scores songs against a user's taste profile using a weighted algorithm across four features: genre match (2.5 pts), mood match (3.5 pts), energy closeness (2.5 pts), and tempo closeness (1.5 pts). Songs are ranked by score and the top matches are returned as recommendations.

## What's New: Agentic Workflow

This extended system adds **agentic learning** — the recommender now observes user feedback (liked/skipped songs) and adapts its weights automatically. Instead of static weights, the system:

1. **PLAN**: Initialize with default weights
2. **ACT**: Generate recommendations using current weights
3. **CHECK**: Receive feedback on which songs users liked/skipped
4. **ADAPT**: Analyze feedback and adjust weights upward for features that matched liked songs, downward for skipped songs
5. **REPEAT**: Use improved weights in the next recommendation cycle

This demonstrates how AI systems can learn from behavior rather than relying on hand-tuned parameters. The system includes guardrails (weight clamping), comprehensive logging, and tracks all weight evolution.

## System Architecture

![Architecture Diagram](diagrams/architecture.mmd)

See `diagrams/architecture.mmd` for the detailed data flow showing the Plan-Act-Check-Adapt cycle.

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/applied-ai-system-final.git
cd applied-ai-system-final
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Adaptive Recommender

**Option 1: Interactive Mode** (try it yourself)
```bash
cd src
python interactive.py
```
Enter your music preferences (genre, mood, energy, tempo), get personalized recommendations, tell the system which songs you like/skip, and watch it learn and re-rank songs in real-time.

**Option 2: Demo Mode** (see pre-scripted example)
```bash
cd src
python adaptive_demo.py
```

This runs a complete 3-iteration demo where:
- Iteration 1: System makes initial recommendations, user gives feedback
- Iteration 2: System adjusts weights and re-recommends, user gives more feedback  
- Iteration 3: System refines weights again and generates final recommendations

### Running Tests

```bash
pytest tests/
pytest test_profiles.py
```

---

## Sample Interaction: System Learning Over Time

Here's what happens when you run `python adaptive_demo.py`:

**Iteration 1: Initial Recommendations**
```
User Profile: pop, happy, energy=0.8, tempo=120 BPM

Initial Weights: mood=3.5, genre=2.5, energy=2.5, tempo=1.5

1. Sunrise City by Neon Echo
   Score: 10.00/10.00
   mood match (+3.5), genre match (+2.5), energy perfect match (+2.5), tempo perfect match (+1.5)

2. Rooftop Lights by Indigo Parade
   Score: 7.50/10.00
   mood match (+3.5), genre mismatch (0), energy perfect match (+2.5), tempo perfect match (+1.5)

User Feedback: Liked top 2 songs, skipped the last one (Electric Pulse)
```

**After Learning Round 1: Weights Adapt**
```
Weight Changes:
  mood: 3.5 -> 3.9 (boosted because liked songs had mood match)
  genre: 2.5 -> 2.7 (boosted)
  energy: 2.5 -> 2.8 (boosted)
  tempo: 1.5 -> 1.8 (boosted)
```

**Iteration 2: Improved Recommendations**
```
Updated Weights: mood=3.9, genre=2.7, energy=2.8, tempo=1.8

1. Sunrise City by Neon Echo
   Score: 11.20/10.00  [IMPROVED - score went up]
   mood match (+3.9), genre match (+2.7), energy perfect match (+2.8), tempo perfect match (+1.8)

2. Rooftop Lights by Indigo Parade
   Score: 8.50/10.00  [IMPROVED - score went up]
   mood match (+3.9), genre mismatch (0), energy perfect match (+2.8), tempo perfect match (+1.8)

User Feedback: Liked Sunrise City again, skipped Night Drive Loop and Electric Pulse
```

**After Learning Round 2: Further Refinement**
```
Weight Changes:
  mood: 3.9 -> 4.1 (further boosted - mood was critical for liked songs)
  genre: 2.7 -> 2.9 (continued boost)
  energy: 2.8 -> 2.8 (stable)
  tempo: 1.8 -> 1.8 (stable)
```

**Iteration 3: Final Recommendations**
```
Updated Weights: mood=4.1, genre=2.9, energy=2.8, tempo=1.8

1. Sunrise City by Neon Echo
   Score: 11.60/10.00  [FURTHER IMPROVED]
   mood match (+4.1), genre match (+2.9), energy perfect match (+2.8), tempo perfect match (+1.8)

2. Rooftop Lights by Indigo Parade
   Score: 8.70/10.00  [FURTHER IMPROVED]
   mood match (+4.1), genre mismatch (0), energy perfect match (+2.8), tempo perfect match (+1.8)
```

**Key Observation**: Over 2 learning rounds, the system increased the score of songs the user liked (Sunrise City went from 10.00 -> 11.20 -> 11.60) by boosting the weights of features those songs had.

---

## Design Decisions

### 1. Weight Adjustment Strategy
- **Positive feedback**: +0.2 per liked song with matching feature
- **Negative feedback**: -0.1 per skipped song with matching feature
- **Rationale**: Users' actions reveal what matters. Liked songs with mood matches tell us mood is valuable; skipped songs with genre matches tell us genre alone isn't enough.

### 2. Guardrails: Weight Clamping
- Weights are clamped to [0.1, 5.0] to prevent drift
- Prevents mood from becoming negligible (< 0.1) or overwhelming (> 5.0)
- **Rationale**: Without bounds, repeated feedback could push weights toward extremes, making the system brittle.

### 3. Logging and Tracking
- Every recommendation and weight adjustment is logged with timestamp
- Weight history is preserved for analysis
- Feedback history is recorded with before/after weights
- **Rationale**: Transparency is critical for trustworthy AI. Users and developers need to see why recommendations changed.

### 4. Incremental Learning
- System learns from each interaction rather than batching feedback
- Allows near-real-time adaptation
- **Rationale**: Realistic recommenders respond quickly to user preferences, not once per week.

---

## Testing and Reliability

### What Works
- ✓ System correctly identifies which features mattered for liked songs
- ✓ Weight adjustments always move in the correct direction (increase for good features, decrease for bad)
- ✓ Guardrails prevent weights from drifting out of bounds
- ✓ Recommendations improve over iterations (top-liked song scores increase)
- ✓ Logging captures all decisions for audit trail

### Edge Cases Handled
- Empty feedback (no likes/skips) -> no adjustment made
- Single feedback round -> proportional weight changes
- Contradictory feedback (same song in likes and skips) -> balanced by penalty system

### Known Limitations
- Linear adjustment model: assumes more feedback = proportionally better learning
- No forgetting: old feedback weights equally with recent feedback
- Small dataset: 18 songs may not show all learning patterns

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
