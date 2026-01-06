# News

News is a high-performance news aggregator that combines the robustness of **Django** for data management with the speed of **Falcon** for serving web requests. It aggregates news from a curated list of RSS feeds, scores them based on popularity/traffic, and presents them in a clean interface.

## Tech Stack

*   **Web Framework**: [Falcon](https://falcon.readthedocs.io/) (for fast HTTP handling)
*   **Data/ORM**: [Django](https://www.djangoproject.com/) (for models, migrations, and management commands)
*   **Database**: PostgreSQL
*   **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
*   **RSS Parsing**: `feedparser`
*   **Task Runner**: Django Management Commands

## Features

*   **RSS Aggregation**: Fetches articles from a wide range of tech, science, and news sources (configured in `project/settings.py`).
*   **Content Extraction**: Automatically fetches and extracts the main content/paragraphs of articles.
*   **Cleanup**: Automatically removes articles older than 48 hours to keep the content fresh.
*   **Hybrid Architecture**: Uses Django models within a Falcon application structure.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd news
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Configuration:**
    Ensure you have PostgreSQL installed and running. The project expects a database named `news`. Update `project/settings.py` with your database credentials if they differ from the defaults (user: `postgres`, password: `postgres`, port: `6432`).

5.  **Run Migrations:**
    Initialize the database schema using Django's migration tool.
    ```bash
    python manage.py migrate
    ```

## Usage

### Running the Web Server

You can run the web server using `gunicorn` (as defined in the `Procfile`):

```bash
gunicorn router:app --reload
```

### Fetching News

To populate the database with the latest news, run the custom management command:

```bash
python manage.py fetch
```

This command will:
1.  Fetch entries from all configured RSS feeds.
2.  Clean up articles older than 48 hours.
3.  Fetch the full content for new articles.

**Note:** In a production environment, this command should be scheduled to run periodically (e.g., via `cron`).
