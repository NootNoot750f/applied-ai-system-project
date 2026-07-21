# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch v1.0** — A content-based music recommendation engine that scores songs using a 10-point weighted algorithm combining mood, genre, energy, and tempo.

---

## 2. Intended Use

MoodMatch recommends songs based on explicit user mood/genre preferences and acoustic properties (energy, tempo). It is designed for educational exploration of how recommendation algorithms work, not for real-world deployment.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The system asks users for four preferences: favorite genre, favorite mood, preferred energy level (0-1), and preferred tempo (BPM). It then scores each song by awarding points: 3.5 for mood match, 2.5 for genre match, 2.5 for energy closeness (±0.15 range), and 1.5 for tempo closeness (±20 BPM). Mood and genre are all-or-nothing matches, while energy and tempo reward "close enough" songs. The system sorts songs by total score (out of 10) and returns the top recommendations with explanations of why they matched.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

## The catalog contains 18 songs across 15 genres (pop, rock, lofi, ambient, jazz, synthwave, indie pop, hip-hop, classical, electronic, reggae, country, metal, soul, indie) and 12 moods (happy, chill, intense, relaxed, focused, moody, energetic, sad, aggressive, romantic, nostalgic, melancholic). We expanded the starter dataset from 10 to 18 songs by adding hip-hop, classical, electronic, reggae, country, metal, soul, and indie tracks to increase genre diversity. However, the dataset lacks many real-world genre-mood combinations—for example, there's "chill lofi" but no "relaxed lofi," and some genres like classical and rock are represented by only one song each, limiting recommendations for fans of those styles.

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition  
  The system excels for users with well-represented preferences: a pop + happy listener found "Sunrise City" with a perfect 10/10 match, and chill lofi listeners found two perfect 10/10 songs, demonstrating that the scoring algorithm correctly prioritizes mood and genre when both align. The weighting scheme (3.5 for mood, 2.5 for genre, 2.5 for energy) captures a key insight—users care most about emotional vibe and category—and this shows in the test results where mood-matched songs consistently ranked higher even when other features didn't match. The system also gracefully handles mid-range preferences: users seeking moderate energy (0.4-0.7) and standard tempos (90-130 BPM) find abundant options with high scores, showing the algorithm works well for "mainstream" taste profiles.

---

## 6. Limitations and Bias

The 18-song dataset is the single largest limitation. Some genres have only 1 song (rock has "Storm Runner" only), and mood combinations like "relaxed lofi" don't exist at all. This forces the algorithm into fallback behavior where it recommends genre-mismatched songs when mood preferences are rare, creating artificial filter bubbles.

The energy scoring algorithm (±0.15 tolerance for perfect match) systematically disadvantages users at extremes. A user with energy=0.0 (minimalist/ambient preference) or energy=1.0 (maximum energy) gets few perfect matches because most songs cluster in the 0.3-0.9 range.

The weighting (mood 3.5 + genre 2.5 = 60% of total points) means similarity (what the song is labeled as) dominates over acoustic properties (how it feels). The "Conflicted High-Energy Sad" user shows this: they got "Thunder Strike" (metal/aggressive, genre match) ranked higher than "Broken Echoes" (hip-hop/sad, mood match), even though mood alignment should matter more for playlist coherence.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

---

I tested 6 user profiles: 3 baseline profiles (High-Energy Pop Fan, Chill Lofi Relaxer, Intense Rock Fan) that should find perfect matches, and 3 adversarial profiles (Conflicted High-Energy Sad, Laser-Focused Lofi Relaxer, Slow Paradox with extreme energy=0.0) designed to expose weaknesses. I looked for whether the top-ranked songs matched our intuition—e.g., does a rock fan get rock songs first, and does a pop+happy listener find "Sunrise City" (which matches all four features)? I was surprised by how stable the algorithm was: when I experimentally doubled the energy weight and halved the genre weight, the top-ranked songs didn't change order, only their absolute scores. The biggest surprise was that the 18-song dataset, not the algorithm, was the limiting factor—users with rare mood-genre combos (e.g., "relaxed lofi") couldn't find perfect matches because the songs didn't exist, forcing the system into fallback mode.

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

## Expand the dataset to at least 100 songs to represent rare genre-mood combinations and reduce fallback matching behavior. Add features like lyrics, artist similarity, explicit content warnings, and instrumentation (vocal vs. instrumental), which would let users specify preferences beyond the current four dimensions. Improve explanations by showing not just why a song matched, but also which songs almost matched and why they fell short, helping users understand the tradeoffs the algorithm made.

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

I learned that recomender systems use more math and logic than originally thought, which was unexpected but makes sense. I understood that there was some logic underneath, but there was more going on than I thought. I learned that the dataset really makes a difference, and that the algorithm is not as important as the dataset, since the logic could be solid, but if there is not much info, then it wont do that well, but if you have a large dataset, the logic could be ok, but you would end up with more successes through sheer numbers and info.

Something unexpected was that songs are weighed differently in their different features, like mood and genre, and that some are more important than others, and that this is important to think about when making a recommender.

This changed the way I look at recommenders and it makes me appreciate the work that went into them more, since now that I have this experience, I can look at it and know how it works, and if I could get the recommender of a platform im using, then I could skew how I wanted it to present me songs or videos. Its useful to know, so I could build a for you page more accurately to what I wanna watch or listen to.

I think that in the future, I would wanna try to make this into an actual recommender, perhaps turning this into an API style project, or you could like import your youtube history or music history and it would be able to find a song that you would want to listen to. Of course I would need to expand the dataset, but this would be a nice thing to do.
