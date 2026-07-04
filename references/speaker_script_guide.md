# Speaker script guide

Use this reference when producing `paper2slide_speaker_script.docx`.

## Default requirement

The default speaker script must be in English and must be returned as a Word document for every full paper-to-slide package.

If the user requests another presentation language, still produce the default English script unless they explicitly ask for a non-English-only script. Additional translated or bilingual scripts can be returned as extra files.

## Timing

Default total duration: approximately 10 minutes.

Spoken English pace:

- 60 seconds: 100-150 words.
- 45 seconds: 75-110 words.
- 30 seconds: 45-75 words.
- 90 seconds: 150-210 words.

Leave slight breathing room. A 10-minute script should usually be around 1,200-1,450 words.

## Structure per slide

For each slide, include:

- Slide number.
- Slide title.
- Target time.
- Speaker script.
- Optional transition sentence.

Example:

```text
Slide 5 — Architecture Overview
Target time: 80 seconds

The central idea of our method is to ...

Transition: Now that the overall architecture is clear, I will zoom into the first module.
```

## Style

- Use natural spoken English, not paper prose.
- Explain the visual before discussing details.
- Avoid reading every bullet verbatim.
- When introducing equations, describe the role first, then the formula.
- When discussing tables, state the comparison, then the key number.
- Use signposting: “The key point here is...”, “This is important because...”.

## Technical wording

For model architecture slides:

- Start with the input-output flow.
- Name each core module once.
- Explain why the module is needed.
- End with the consequence for performance, efficiency, or robustness.

For result slides:

- State the dataset/protocol.
- State the strongest result.
- Mention one or two important baselines.
- Interpret the gain, not just the number.

For limitations:

- Be honest and concise.
- Frame limitations as future research directions.

## Avoid

- Overly promotional language.
- Claiming “state of the art” unless the paper supports it.
- Mentioning results not present in the paper.
- Long sentences with multiple clauses.
- Dense lists of metric values.
