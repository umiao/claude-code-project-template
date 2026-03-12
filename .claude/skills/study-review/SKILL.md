# /study-review -- Spaced Repetition Study Review Session

Run a study review session using the SM-2 spaced repetition queue. Find due posts, generate quiz questions from post content, present them to the user, and record self-ratings to update the review schedule.

## Usage

```
/study-review                    # Start a review session with all due posts
/study-review <slug>             # Review a specific post by slug (filename without .md)
/study-review stats              # Show review queue statistics
```

## Steps

### 1. Check Review Queue Status

1. Run `python tools/review_queue.py show` to find posts due for review.
2. If no posts are due, report:
   ```
   [INFO] No posts due for review today.
   Next step: Run `python tools/review_queue.py stats` to see your review schedule.
   ```
   Then stop.
3. If the queue has not been initialized (state file missing or empty), run:
   ```
   python tools/review_queue.py init
   ```
   Then re-run `show` to get the due list.
4. If a specific slug was provided as argument, verify it appears in the due list. If not due, ask the user if they want to review it anyway (early review).

### 2. Select Post for Review

1. If a specific slug was provided, use that post.
2. If multiple posts are due, show the list and let the user pick:
   ```
   Posts due for review (N):
     1. <slug-1> (due: YYYY-MM-DD, interval: Xd, reps: N)
     2. <slug-2> (due: YYYY-MM-DD, interval: Xd, reps: N)
     ...

   Pick a post number (or "all" for sequential review):
   ```
3. If the user says "all", process posts sequentially (oldest due date first), one at a time.

### 3. Read and Analyze Post

1. Read the full post file from `source/_posts/<slug>.md`.
2. Parse the front matter to extract:
   - `title`, `categories`, `tags`
   - `key_concepts` (if present -- use for targeted questions)
   - `takeaways` (if present -- use as answer reference)
   - `series`, `series_index` (for cross-referencing context)
3. Read the post body content.
4. Identify the major topics, definitions, examples, and conclusions in the post.

### 4. Generate Quiz Questions

Generate **5-7 questions** from the post content, covering at least 3 of these question types:

#### Type A: Definition Recall
Test whether the user can define or explain a key concept from the post.
```
Q: What is <concept>? Explain it in your own words.
```
- Draw from `key_concepts` if available, otherwise from bold terms, headers, and technical vocabulary in the post.

#### Type B: Application / Scenario
Test whether the user can apply a concept to a practical scenario.
```
Q: You're designing a system that needs <requirement>. Based on what you read about <topic>,
   which approach would you choose and why?
```
- Create realistic scenarios related to the post's domain.
- For DDIA posts: system design scenarios.
- For SQL posts: query optimization or schema design scenarios.
- For DS posts: model selection or data pipeline scenarios.

#### Type C: Comparison / Trade-off
Test whether the user understands trade-offs between approaches discussed in the post.
```
Q: Compare <approach A> vs <approach B> discussed in this post.
   What are the trade-offs? When would you choose each?
```
- Draw from any sections that discuss alternatives, pros/cons, or design decisions.

#### Type D: Connection / Synthesis
Test whether the user can connect concepts from this post to broader knowledge.
```
Q: How does <concept from this post> relate to <concept from another post or general knowledge>?
```
- If `series` is set, reference concepts from adjacent posts in the series.
- If `key_concepts` overlap with other posts, create cross-reference questions.

#### Type E: Recall Detail
Test whether the user remembers specific important details.
```
Q: In the context of <topic>, what are the key steps / components / properties of <specific thing>?
```
- Target numbered lists, step-by-step processes, or enumerated properties from the post.

#### Question generation rules:
- Questions must be derived from actual post content, not invented.
- If `key_concepts` and `takeaways` are available, prioritize those for questions.
- Vary difficulty: include 2 easier (definition/recall) and 2-3 harder (application/synthesis).
- Do NOT show the answer immediately -- wait for the user to attempt.

### 5. Present Questions and Conduct Review

Present questions one at a time:

```
## Review: <Post Title>
Post <current>/<total due> | Series: <series name> (if applicable)

---

### Question 1/N (Definition Recall)
<question text>

Take a moment to think, then share your answer (or type "show" to see the reference answer).
```

After the user responds (or asks to see the answer):

1. Show the **reference answer** drawn from the post content:
   ```
   ### Reference Answer
   <concise answer based on post content>

   Source: <relevant section/heading from the post>
   ```

2. Ask the user to self-rate their recall:
   ```
   How well did you recall this? (0-5)
     0 - Complete blackout, no memory at all
     1 - Wrong answer, but recognized the topic when shown
     2 - Wrong answer, but it felt familiar
     3 - Correct answer with significant difficulty
     4 - Correct answer with some hesitation
     5 - Perfect, instant recall
   ```

3. Record the rating (will be used in step 6).
4. Move to the next question.

If the user wants to skip a question, accept "skip" and move on (do not rate skipped questions).

### 6. Record Review Results

After all questions are answered:

1. Calculate the **session rating** as the rounded average of all individual question ratings.
2. Run `python tools/review_queue.py mark <slug> <session_rating>` to update the SM-2 schedule.
3. Show the session summary:

```
## Review Complete: <Post Title>

Questions answered: N/M
Average rating: X.X/5
Session rating (rounded): X/5

Schedule update:
  New interval: X days
  Next review due: YYYY-MM-DD
  Repetitions: N
  Easiness: X.XX
```

### 7. Continue or Finish

If the user selected "all" in step 2, or if there are more due posts:

```
[INFO] Review complete for <slug>. N more posts due today.
Continue to next post? (yes/no)
```

- **yes**: Go back to step 3 with the next due post.
- **no**: Show session summary and stop.

If this was the last (or only) post:

```
[DONE] Review session complete.
  Posts reviewed: N
  Run /study-review again when more posts are due.
```

## Special Commands

During a review session, the user can say:

- **"skip"**: Skip the current question (no rating recorded for it).
- **"show"**: Show the reference answer without attempting.
- **"stop"**: End the session early. Record ratings for completed questions only. Mark the post with the average of completed question ratings.
- **"stats"**: Show current review queue statistics mid-session.

## Important Rules

- **No emoji**: Use text tags like [DONE], [INFO], [WARN].
- **No invented content**: All questions and answers must be derived from the actual post content.
- **One post at a time**: Complete the review cycle for one post before moving to the next.
- **Respect the SM-2 algorithm**: The rating passed to `mark` determines the next review interval. Do not manipulate ratings.
- **Graceful degradation**: If a post has no `key_concepts` or `takeaways`, generate questions from the full post body. The skill works with or without enriched front matter.
- **All subprocess calls use `encoding="utf-8"`** if invoking review_queue.py programmatically.
- **When in doubt, ask**: If the user's answer is ambiguous or the question seems unclear, discuss rather than auto-rating.
