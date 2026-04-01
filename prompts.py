def build_opening_prompt(title: str, genre: str, hook: str) -> str:
    return f"""
You are a masterful collaborative storyteller.

Write the opening of a story based on the details below.

Rules:
- Genre must strictly feel like: {genre}
- Keep tone vivid, engaging, and emotionally consistent
- Maintain strong story logic and character consistency
- Write in clear, immersive prose
- Write in third-person narrative unless the setup strongly suggests otherwise
- Generate only the story content, no explanations
- Length: around 150 to 250 words
- Give the story a strong opening that makes the reader want to continue

Story Title:
{title}

Initial Hook / Setting:
{hook}
""".strip()


def build_continue_prompt(title: str, genre: str, story_text: str, user_input: str) -> str:
    return f"""
You are a collaborative storytelling AI.

Continue the story while staying fully consistent with:
- the established genre
- all prior events
- character behavior
- tone and setting

Rules:
- Genre: {genre}
- Continue naturally from the latest events
- Keep continuity strong
- Write 1 to 2 coherent paragraphs
- Do not repeat the user's contribution word-for-word unless absolutely necessary
- Do not repeat earlier story lines
- Push the plot forward meaningfully
- Keep the writing vivid, polished, and immersive
- Output only the story continuation

Story Title:
{title}

Full Story So Far:
{story_text}

Latest User Contribution:
{user_input}
""".strip()


def build_choices_prompt(title: str, genre: str, story_text: str) -> str:
    return f"""
You are a collaborative storytelling AI.

Based on the story below, generate exactly 3 strong next-step choices.

Rules:
- Genre: {genre}
- Each choice must be complete and clear
- Each choice must be meaningfully different
- Each choice should move the plot forward
- Each choice should be 1 to 2 sentences max
- Keep choices consistent with the story so far
- Do not output anything except the 3 choices
- Format exactly like this:

1. ...
2. ...
3. ...

Story Title:
{title}

Full Story So Far:
{story_text}
""".strip()

