# Restaurants API Project

## Overview

The **Restaurants API** is a FastAPI-based backend application designed to manage restaurants, menus, user accounts, and likes. It provides a RESTful API for user authentication, restaurant management, and menu operations, with support for PostgreSQL as the primary database and SQLite for testing purposes. The project is containerized using Docker and includes tools for database migrations (Alembic) and API documentation via Swagger UI.

### Key Features

- **User Authentication**:
  - Register and log in users via `/auth/register/` and `/auth/login/` endpoints.
  - Refresh tokens using `/auth/refresh/`.
  - JWT-based authentication with access and refresh tokens.

- **Restaurant Management**:
  - Create restaurants via `/restaurants/` (POST).
  - Retrieve all restaurants via `/restaurants/` (GET).

- **Menu Management**:
  - Retrieve today's menus sorted by likes via `/menus/today/` (GET).

- **Likes System**:
  - Like a menu via `/likes/` (POST).

### Versioning in API Endpoints

The `GET /restaurants/` endpoint includes a stub implementation to demonstrate how versioning for mobile applications can be handled, ensuring backward compatibility and smooth updates. Here's the current approach:

- **Version Detection**: The endpoint is designed to detect the client version (e.g., via a custom header like `X-App-Version` or a query parameter like `?version=1.0`) and adjust the response format or behavior accordingly.
- **Stub Implementation**: Currently, this versioning is implemented as a placeholder (stub). While the endpoint is prepared to handle different versions (e.g., by returning different fields like `rating` for newer versions), the actual response does not yet vary based on the version provided. For example:
  - **Version 1.0**: Returns `[{"id": 1, "name": "Test Restaurant"}]`.
  - **Version 2.0**: Also returns `[{"id": 1, "name": "Test Restaurant"}]`, despite the intention to include additional fields like `rating`.
- **Future Development**: The stub serves as a foundation for future implementation, where responses can be tailored to specific app versions (e.g., adding new fields like `rating` or `last_updated` for newer versions).

This approach allows developers to see a potential versioning strategy while the actual logic for response differentiation is yet to be implemented.

### API Endpoints

The API documentation is available via Swagger UI at `/docs` after running the application. Key endpoints include:

- **POST `/auth/register/`**: Register a new user.
  - **Request Body**: `{"email": "user@example.com", "password": "password123"}`
  - **Response**: `201 Created` with user details or `409 Conflict` if the email already exists.

- **POST `/auth/login/`**: Log in a user and receive access/refresh tokens.
  - **Request Body**: `{"email": "user@example.com", "password": "password123"}`
  - **Response**: `200 OK` with tokens or `401 Unauthorized` if credentials are invalid.

- **POST `/auth/refresh/`**: Refresh access token using a refresh token.
  - **Request Body**: `{"refresh_token": "your_refresh_token"}`
  - **Response**: `200 OK` with new tokens or `401 Unauthorized` if the token is invalid.

- **POST `/restaurants/`**: Create a new restaurant.
  - **Request Body**: `{"name": "New Restaurant"}`
  - **Response**: `201 Created` with restaurant details or `404 Not Found` if validation fails.

- **GET `/restaurants/`**: Retrieve all restaurants.
  - **Response**: `200 OK` with a list of restaurants or `404 Not Found` if none exist. Includes a stub for versioning (e.g., via `X-App-Version` header), but responses are currently the same across versions.
  - **Example Response (v1.0 and v2.0)**: `[{"id": 1, "name": "Test Restaurant"}]`

- **GET `/menus/today/`**: Retrieve today's menus, sorted by the number of likes.
  - **Response**: `200 OK` with a list of menus or `404 Not Found` if none exist.

- **POST `/likes/`**: Like a menu.
  - **Request Body**: `{"menu_id": 1}`
  - **Query Parameter**: `user_id=1`
  - **Response**: `200 OK` with like details or `404 Not Found` if the menu doesn't exist.

### Project Structure

- **src/**: Main source code directory.
  - **config/**: Configuration files for settings
