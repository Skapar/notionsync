
# NotionSync API

This project is a simple API built with FastAPI that supports:

1. **User Registration and Authentication** (JWT with OAuth 2.0)
2. **Notion Page Management**:
    - Adding pages
    - Editing pages
    - Deleting pages
    - Retrieving pages with pagination

The database is managed using SQLite via SQLAlchemy, and the integration with Notion's API allows managing Notion pages as part of the admin tasks.

## Features

- **User Registration and Login**:
  - Users can register using a `username` and `password`.
  - Authentication is handled using **OAuth2.0 with JWT** access and refresh tokens for secure authorization.

- **Page Management in Notion**:
  - **Create**: Add new pages to a Notion database.
  - **Update**: Modify existing Notion pages.
  - **Delete**: Move Notion pages to trash.
  - **List with Pagination**: Retrieve pages with pagination support.

- **Security**:
  - Implemented using **OAuth2.0 with JWT tokens**.
  - Users must authenticate with a valid token to access the Notion page management API.

## Project Structure

```bash
.
├── app
│   ├── __init__.py
│   ├── main.py                # FastAPI entry point
│   ├── auth                   # Handles user registration, login, and security
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models for user authentication
│   │   ├── routes.py           # Routes for registration and login
│   │   ├── security.py         # JWT and OAuth2.0 logic
│   │   ├── schemas.py          # Pydantic schemas for user inputs
│   ├── notion                 # Handles Notion API integration
│   │   ├── __init__.py
│   │   ├── client.py           # Initializes Notion client
│   │   ├── routes.py           # CRUD routes for page management
│   │   ├── schemas.py          # Pydantic models for Notion data
│   ├── config.py               # App configuration settings
│   └── db.py                   # Database connection and session management
├── alembic                     # Database migrations
├── .env                        # Environment variables
├── README.md
└── requirements.txt            # Project dependencies
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/notion-sync-api.git
cd notion-sync-api
```

1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Set up environment variables:

Create a `.env` file in the project root with the following content:

```bash
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id
```

1. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

## Running with Docker

To run the application with Docker:

1. Build the Docker image:

    ```bash
    docker build -t notion-sync-api .
    ```

2. Run the Docker container:

    ```bash
    docker-compose up
    ```

This will start the application in a Docker container and automatically set up the required services. Make sure to modify the `.env` file to suit your configuration.

## Linter with Black

1. Code formatting with `black`:

    This project uses `black` for consistent code formatting. To format the code, run the following command:

    ```bash
    black .
    ```

    You can install `black` if you don't have it yet:

    ```bash
    pip install black
    ```

Make sure to run `black` before submitting or deploying your code to maintain consistency.

## API Endpoints

### Authentication

- **Register**: `POST /auth/register`
  - Request body: `{"username": "your_username", "password": "your_password"}`
  - Response: `{"msg": "User successfully registered"}`

- **Login**: `POST /auth/login`
  - Request body: `{"username": "your_username", "password": "your_password"}`
  - Response: JWT tokens: `{"access_token": "your_token", "token_type": "bearer"}`

### Notion Pages (Requires Authentication)

- **Create a page**: `POST /notion/pages`
  - Request body: `{"title": "Page title", "content": "Page content"}`
  - Response: Created Notion page data.

- **Update a page**: `PUT /notion/pages/{page_id}`
  - Request body: `{"title": "Updated title", "content": "Updated content"}`
  - Response: Updated Notion page data.

- **Delete a page**: `DELETE /notion/pages/{page_id}`
  - Response: `{"msg": "Page moved to trash"}`

- **List pages**: `GET /notion/pages?start_cursor=""&page_size=10`

    Retrieves a paginated list of pages from the connected Notion database. You can control the pagination by providing a `start_cursor` and a `page_size`.

    **Query Parameters**:
    `start_cursor` (optional): A string used to retrieve the next set of results. Defaults to an empty string if not provided.
    `page_size` (optional): The number of pages to return. Defaults to 10 if not provided.

    **Response**:
    Returns a JSON object containing a list of pages with the following structure:

    ```json
    {
      "results": [
        {
          "id": "129ec433-71fd-8190-89a4-e3c9d5cf625a",
          "title": "Example Title",
          "content": "Page content here"
        },
        ...
      ]
    }
    ```

### Security

- **JWT Authentication**:
  - JWT tokens are issued during login and must be included in the `Authorization` header as a Bearer token for all subsequent requests to the Notion API endpoints.

  Example:

  ```bash
  Authorization: Bearer your_jwt_token
  ```

## Notion Integration

- **Notion Client**: The application interacts with the Notion API using the official Notion SDK (`notion-client`).
- **Pages Management**: The API supports basic CRUD operations on pages in your Notion workspace, based on the specified Notion database ID.

## How JWT Authentication Works

The application uses **OAuth2.0** with **JWT tokens** to secure the API. The flow involves issuing both **access** and **refresh** tokens. The access token is used to authenticate requests to secure endpoints, while the refresh token can be used to obtain a new access token when the old one expires.

- **Access Token**: Short-lived and passed with every request to authenticated endpoints.
- **Refresh Token**: Longer-lived and used to obtain new access tokens without re-authenticating the user.

## Contributing

Feel free to submit issues, feature requests, or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
