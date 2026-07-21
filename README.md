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

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
