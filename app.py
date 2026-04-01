import streamlit as st
from llm import generate_opening_story, continue_story_with_ai, generate_story_choices
from prompts import build_opening_prompt, build_continue_prompt, build_choices_prompt

st.set_page_config(page_title="AI Story Weaver", page_icon="📖", layout="wide")

defaults = {
    "story_started": False,
    "title": "",
    "genre": "Fantasy",
    "hook": "",
    "story_text": "",
    "user_input": "",
    "choices_text": "",
    "choices_list": [],
    "selected_choice": "",
    "temperature": 0.8,
    "previous_story_text": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def parse_choices(choices_text: str):
    lines = [line.strip() for line in choices_text.splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        if line and line[0].isdigit() and "." in line:
            cleaned.append(line.split(".", 1)[1].strip())
        elif line.lower().startswith("option"):
            cleaned.append(line.split(":", 1)[1].strip() if ":" in line else line)
    return cleaned[:3]


def show_friendly_error(e: Exception):
    error_message = str(e)
    if "429" in error_message or "rate" in error_message.lower() or "quota" in error_message.lower():
        st.error("Rate limit reached. Please wait a moment and try again.")
    else:
        st.error(f"Error: {error_message}")


st.title("📖 AI-Powered Story Weaver")
st.caption("Build stories collaboratively with AI.")

# ---------- Story Setup ----------
st.subheader("1. Story Setup")

title = st.text_input(
    "Story Title",
    value=st.session_state.title,
    placeholder="Enter your story title..."
)

genre_options = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Comedy"]

genre = st.selectbox(
    "Genre",
    genre_options,
    index=genre_options.index(st.session_state.genre)
)

hook = st.text_area(
    "Initial Hook / Setting",
    value=st.session_state.hook,
    placeholder="Describe the opening scene, setting, characters, or idea...",
    height=160
)

if st.button("Start the Story", use_container_width=True):
    if not title.strip():
        st.warning("Please enter a story title.")
    elif not hook.strip():
        st.warning("Please enter the initial hook / setting.")
    else:
        st.session_state.title = title
        st.session_state.genre = genre
        st.session_state.hook = hook

        prompt = build_opening_prompt(title=title, genre=genre, hook=hook)

        try:
            with st.spinner("Generating your story opening..."):
                opening = generate_opening_story(
                    prompt,
                    temperature=st.session_state.temperature
                )

            st.session_state.story_text = opening
            st.session_state.story_started = True
            st.session_state.choices_text = ""
            st.session_state.choices_list = []
            st.session_state.previous_story_text = ""
            st.success("Story created successfully.")

        except Exception as e:
            show_friendly_error(e)

# ---------- Main Storytelling View ----------
if st.session_state.story_started:
    st.divider()
    st.subheader("2. Main Storytelling View")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Full Story So Far")
        st.text_area(
            "Story",
            value=st.session_state.story_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )

        user_input = st.text_area(
            "Add your next line / idea",
            value=st.session_state.user_input,
            placeholder="Write the next sentence, twist, dialogue, or event...",
            height=120
        )

        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("Continue with AI", use_container_width=True):
                if not user_input.strip():
                    st.warning("Please add your contribution before continuing.")
                else:
                    clean_input = user_input.strip()

                    if clean_input.lower() in st.session_state.story_text.lower():
                        st.warning("That line already appears in the story. Please add a new contribution.")
                    else:
                        st.session_state.user_input = clean_input
                        updated_story = st.session_state.story_text + "\n\n" + clean_input

                        prompt = build_continue_prompt(
                            title=st.session_state.title,
                            genre=st.session_state.genre,
                            story_text=updated_story,
                            user_input=clean_input
                        )

                        try:
                            st.session_state.previous_story_text = st.session_state.story_text

                            with st.spinner("AI is continuing the story..."):
                                ai_continuation = continue_story_with_ai(
                                    prompt,
                                    temperature=st.session_state.temperature
                                )

                            st.session_state.story_text = updated_story + "\n\n" + ai_continuation
                            st.session_state.user_input = ""
                            st.session_state.choices_text = ""
                            st.session_state.choices_list = []
                            st.success("Story continued successfully.")
                            st.rerun()

                        except Exception as e:
                            show_friendly_error(e)

        with button_col2:
            if st.button("Give Me Choices", use_container_width=True):
                prompt = build_choices_prompt(
                    title=st.session_state.title,
                    genre=st.session_state.genre,
                    story_text=st.session_state.story_text
                )

                try:
                    with st.spinner("Generating branching choices..."):
                        choices = generate_story_choices(
                            prompt,
                            temperature=st.session_state.temperature
                        )

                    st.session_state.choices_text = choices
                    st.session_state.choices_list = parse_choices(choices)

                except Exception as e:
                    show_friendly_error(e)

        if st.session_state.choices_list:
            st.markdown("### AI Choices")
            st.caption("Select one option to continue the story.")

            for idx, choice in enumerate(st.session_state.choices_list, start=1):
                if st.button(f"Option {idx}: {choice}", key=f"choice_{idx}", use_container_width=True):
                    st.session_state.selected_choice = choice

                    updated_story = st.session_state.story_text + "\n\n" + choice

                    prompt = build_continue_prompt(
                        title=st.session_state.title,
                        genre=st.session_state.genre,
                        story_text=updated_story,
                        user_input=choice
                    )

                    try:
                        st.session_state.previous_story_text = st.session_state.story_text

                        with st.spinner("Continuing story from selected choice..."):
                            ai_continuation = continue_story_with_ai(
                                prompt,
                                temperature=st.session_state.temperature
                            )

                        st.session_state.story_text = updated_story + "\n\n" + ai_continuation
                        st.session_state.choices_text = ""
                        st.session_state.choices_list = []
                        st.success("Story continued from selected choice.")
                        st.rerun()

                    except Exception as e:
                        show_friendly_error(e)

    with col2:
        st.markdown("### Story Controls")
        st.slider(
            "Creativity / Temperature",
            min_value=0.0,
            max_value=1.5,
            value=float(st.session_state.temperature),
            step=0.1,
            key="temperature"
        )

        st.markdown("### Current Genre")
        st.info(st.session_state.genre)

        st.markdown("### Story Rules")
        st.write(
            """
- Keep the story consistent
- Respect the chosen genre
- Build naturally from prior events
- Keep tone and characters coherent
            """
        )

        st.markdown("### Bonus Features")

        if st.button("Undo Last AI Turn", use_container_width=True):
            if st.session_state.previous_story_text:
                st.session_state.story_text = st.session_state.previous_story_text
                st.session_state.previous_story_text = ""
                st.session_state.choices_text = ""
                st.session_state.choices_list = []
                st.success("Last AI turn was undone.")
                st.rerun()
            else:
                st.warning("No AI turn available to undo.")

        markdown_story = f"""# {st.session_state.title}

**Genre:** {st.session_state.genre}

## Initial Hook / Setting
{st.session_state.hook}

## Full Story
{st.session_state.story_text}
"""

        safe_title = st.session_state.title.strip().replace(" ", "_").lower() or "story"

        st.download_button(
            label="Export Story as Markdown",
            data=markdown_story,
            file_name=f"{safe_title}.md",
            mime="text/markdown",
            use_container_width=True
        )
              