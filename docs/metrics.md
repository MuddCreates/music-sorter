# Metrics to track

1. tempo (easy-medium?) for reference, tempo is the "speed" of a song;
   the frequency of "beats"

    1. find the downbeats--should be pressure spikes at regular
       intervals.

    2. track the frequency and extremity of tempo modulations.
       Possibly try to quantify how "jarring" the changes are too.

2. chord related things (medium-hard?) for reference, a chord is a
   harmonic (i.e., composed of multiple sumperimposed pitches) set of
   pitches consisting of some number of notes. Sometimes, the chord
   will be decomposed into individual notes (arpeggiation), or into
   groups of notes, played by different voices. A chord progression is
   some list of chords that, when played sequentially, transitions
   through some sort of "distance" away from the tonic (root note),
   returning (at least usually) to the tonic to give a sense of
   "resolution."

   In an 8-note scale, we use the following terms to describe notes.
   This table is a 12-semitone scale thing, so notes congruent mod 12
   are the "same" note shifted up. In terms of physics, this means
   that the frequency of one is 2^n times the frequency of the other,
   where $n\in \mathbb{Z}, n\neq 0$. Or, that you can fit an even
   number of wavelengths of one inside one wavelength of the other.
   The following table is adapted from wikipedia. Can re-index

   | Note #    |    Name     | e.g.(Mj)  | Meaning....
   | --------- | ----------- | --------- | ---------------------
   | 0+\*/12   | Tone        |    C      | Tonal center, note of final resolution
   |    11     | Leading     |    B      | Melodically strong affinity for and leads to tonic/One half step below tonic in Major scale and whole step in Natural minor.
   |    10     |             | A#/B♭     | Sorta same as the other ones that're same
   |    9      | Submediant  |    A      | Lower mediant, midway between tonic and subdominant, (in major key) root of relative minor key
   |    8      |             |    G#     | Same as F#/G♭
   |    7      | Dominant    |    G      | 2nd in importance to the tonic.  Sounds very resolved
   |    6      |             | F#/G♭     | Doesn't sound "harmonic" with the tonic but not super dissonant either.
   |    5      | Subdominant |    F      | Lower dominant, same interval below tonic as dominant is above tonic.  Creates a bit of tension when played with tonic.
   |    4      | Mediant     |    E      | Midway between tonic and dominant, (in minor key) root of relative major key. Sounds v harmonic when played with tonic.
   |    3      |             | D#/E♭     | Sounds "minor" when played with tonic?
   |    2      | Supertonic  |    D      | One whole step (two semitones) above the tonic.  Somewhat dissonant.
   |    1      |             | C#/D♭     | Dissonant
   |    0      | Tonic       |    C      | Tonal center, note of final resolution

   \* the + indicates that this note is up an octave, but in the same
   equivalence class mod 12 as whatever number precedes it. This
   notation is my own, so so don't count on seeing it around too
   often? Also, usually I believe indexing starts at 1, but I thought
   this would help avoid off-by-one errors, and also make the modular
   relationships more apparent.

   Chords can be (partially) classified by the number of notes they
   contain. A 3-note chord is called a triad. Here is some info about
   the diatonic functions (certain types of triads) that can be formed
   with the degrees (the named notes above; i.e. none of 2,4,7,9,11)
   as roots. The capitalization is both intentional and important!

   | Chord#(Mj.) |    Name                     | Notes    | Character
   | ----------- | --------------------------- | -------- | ---------
   |    I        | Tone                        | 0+,4+,7+ |
   |    vii      | Leading tone/Subtonic\**    | 11,2+,5+ |
   |    vi       | Submediant/Tonic parallel   | 9,12,4+  |
   |    V        | Dominant                    | 8,11,2+  |
   |    IV       | Subdominant                 | 5,9,12   |
   |    iii      | Mediant/Dominant parallel\* | 4,7,11   |
   |    ii       | Supertonic/Subdominant par. | 2,5,9    | \***
   |    I        | Tonic                       | 0,4,7    |

   \* also called Tonic counter parallel

   \** OFTEN referred to as incomplete Dominant seventh

   \*** Distinguish chord V as a "goal" of motion (music "feels"
   tugged towards dominant). This is because ii lies a fifth above the
   dominant, and descending fifth's sounds very "strong" and natural.
   In fact, ii is one of the strongest ways to get to V. Adding a
   chordal seventh (i.e., the root of the chord plus 7, e.g. if tonic
   is 1, we'd add an 8) makes this feel more intense, and makes us
   feel tugged towards resolution more. More on wiki- pedia about why
   this is

   Ok I haven't finished this but the point is that chord progressions
   will be super helpful in quantifying the character of a piece.  In
   that light, some paths of inquiry:

   1. Finding out what key (i.e., what scale the song resolves around)
      our mp3 is in. A Crappy starting-point approximation--look at
      the first note of the song, and see if it makes sense that that
      note is the tonic

   2. Identify chords within the mp3

   3. Look at distributions between the chords, and transitions from
      chord to chord. Possibly use a Markov model? structure here
      would be a little more long-term than just first order.

   4. And/or, look at how long it takes for chords to be resolved,
      and/or the average distance between chords on the circle of
      fifths. (maybe this is its own R^n walk problem?)

   5. On a related note, we could also look at how strong cadences
      (rhythmic/harmonic endings to phrases) are

   6. Track number of accidentals (modulations to a different key),
      and how they are distributed.

   7. Carefully track the degree of musical "tension" in the
      progression, and attempt to quantify it. Some progressions might
      avoid resolving for a while, but still not create a lot of
      tension in the meantime.

3. frequency distributions and/or overtones (easy)

   1. looking at the frequency / overtone distributions would help us
      to determine what the notes "sound like" in this song. E.g., a
      violin playing an A is different sounding than a piano doing the
      same thing. Overtones play a significant role in that.
   2. Could possibly try to track the number of distinct voices
      (probably hard) and track how much each of them moves around.
      Might be hard to separate out the voices without fourier
      analysis?

4. Dynamics (how loud or quiet something is)

    1. Similar to tempo. Find how _much_ the dynamics change (on
       average), and over what kinds of time intervals. Could also try
       to do some curve fitting with pressure as a function of time
       then track residuals in other pieces.

5. _possibly_ the length of the song, but I think that should be
   avoided.

6. How self-similar parts of the song are--this seems like it could be
   computationally unfeasible, but perhaps we could try to look for
   short-term repeating subunits of chords/themes throughout the
   piece.
