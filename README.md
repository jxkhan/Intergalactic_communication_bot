# Intergalactic Communication Bot

The **Intergalactic Communication Bot** is a robust Django-based backend designed to power intelligent chat interfaces. It manages anonymous and authenticated chat sessions, delivers automated responses via keyword matching, and provides a comprehensive admin interface for FAQ management. It is built with Django Rest Framework (DRF) and uses JWT for secure authentication.

## Features

-   **Chat Sessions**: seamless handling of both anonymous and authenticated user sessions.
-   **Automated Intelligence**: Basic keyword-based FAQ matching for instant automated responses.
-   **FAQ Management**: Admin-controlled categories and questions to keep the knowledge base up-to-date.
-   **Secure Authentication**: JWT-based authentication (SimpleJWT) for protecting API endpoints.
-   **Analytics**: Endpoints to track popular and unmatched questions for continuous improvement.

## API Documentation

The API is split into two main modules: `faq` for knowledge base management and `chat` for session handling.


## Setup Instructions

Follow these steps to get the project running locally.

### Prerequisites

-   Python 3.8+
-   pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/jxkhan/Intergalactic_communication_bot_1
    cd Intergalactic_communication_bot_1
    ```

2.  **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migration**
    The project uses SQLite by default for development.
    ```bash
    python manage.py migrate
    ```
    > **Note**: To use PostgreSQL, update `DATABASES` in `settings.py`.

5.  **Create Admin User**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Access the API at `http://127.0.0.1:8000/`.


```