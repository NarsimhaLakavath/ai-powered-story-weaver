# AI-Powered Story Weaver

An interactive collaborative storytelling app built with **Python + Streamlit** and powered by **Google Gemini**.

The app lets a user define a story, generate an AI-written opening, add their own contributions, request branching choices, select a choice, and continue the story while keeping the full story history in context for consistency.

---

## Features

- Story setup with:
  - Title
  - Genre
  - Initial Hook / Setting
- AI-generated opening paragraph
- Main storytelling view with full story history
- User contribution input
- **Continue with AI**
- **Give Me Choices**
- Clickable branching options
- Creativity / temperature slider
- Genre and story rules display
- **Undo Last AI Turn**
- **Export Story as Markdown**
- Friendly rate-limit error handling

---

## Tech Stack

- **Frontend / App Framework:** Streamlit
- **Language:** Python
- **LLM Provider:** Google Gemini
- **Model Used:** `gemini-2.5-flash`
- **SDK:** `google-genai`

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd myavatar-story-weaver
