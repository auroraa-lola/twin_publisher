## Digital Twin: AI Assistant 

This digital twin chatbot is a commercial AI Assistant to a Sample Autobiography Publishing Company 

 Using SQLite3 for Q&A, the Assistant: 
* Records only relevant questions that aren’t already in the database. 
* Sends contact details or unanswered questions to Pushover.
* Marks relevant Q&A not in the database for human review. A small terminal tool (uv run review.py) is used by a human to approve or delete entries.

## Getting Started

### Prerequisites

- Python 3.12+
- OpenAI API key
- Pushover API User and Token for notiofications
- Required Python packages:
  - `openai`
  - `gradio`
  - `python-dotenv`
  - `sqlite3` (included in Python standard library)

### Installation

1. Sign up for a free account and API Keys at https://pushover.net/
2. Get a free API Key at https://platform.openai.com/api-keys
3. Set up your environment variables:
   - Create a `.env` file in the project directory
   - Add your API keys:
    OPENAI_API_KEY=sk-proj-....
    PUSHOVER_USER=your_pushover_user 
    PUSHOVER_TOKEN=your_pushover_token

## Database Setup

Before running the chatbot, you need to set up the database:

Run the `init_db.ipynb` notebook to:
- Rereate the database schema (question, answer, category, reviewed)
- Insert sample data
- Expect AI to give the same answers to these questions

## Usage

1. From Cursor or VS Code, open split terminal, ensure you are on twin_publishing
2. Start our AI Assistant
   ```sh
      twin_publishing $ uv run app.py
   ```
3. Click or type a question,
   * Expect AI to have the same answer to questions from the database
   * If the question is unrelated to autobiography publishing, expect AI to steer the
   conversation back 
   * Expect AI to push the contact details or unanswered question to Pushover
   * If a related question is not already in the database , expect AI to send the Q&A for Human review
4. Human Review
   ```sh
      twin_publishing $ uv run review.py
         (a)pprove, (d)elete, (s)kip, (q)uit:
   ```
   * Run the Query on `init_db.ipynb` notebook to see the approved entries
