# Meeting Room Booking API

A REST API for viewing static meeting-room inventory and managing authenticated
users' room bookings. The application uses FastAPI, SQLAlchemy ORM, and an
embedded H2 database. Room inventory is read from `rooms.json`.

## Setup instructions

### Prerequisites

- Python 3.11 or newer
- Java JDK, required by the H2 JDBC driver
- pip

Set `JAVA_HOME` to the root directory of the installed JDK. For example, in
PowerShell:

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-<version>"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

### Install and configure

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=h2:///./meetingdb
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JAVA_HOME=C:\Program Files\Java\jdk-<version>
```

Replace the example `SECRET_KEY` with a private random value. Do not commit
`.env` or share its secrets.

Initialize the H2 database and seed the demo user:

```powershell
python create_db.py
```

Start the API:

```powershell
python -m uvicorn app:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is
available at `http://127.0.0.1:8000/docs`.

The setup script seeds a demo account:

- Username: `admin`
- Password: `admin123`

This account has no elevated role; the application currently has no role
system. Change or replace these demo credentials before using the application
outside local development.

## Project structure

```text
meeting-room-booking/
├── auth/
│   ├── auth_dependency.py   # JWT authentication dependency
│   ├── jwt_handler.py       # JWT creation
│   └── password_handler.py  # Password hashing and verification
├── libs/
│   └── h2-2.2.224.jar       # H2 JDBC driver
├── model/
│   ├── booking_request.py   # Booking request schema
│   ├── bookings.py         # SQLAlchemy booking model
│   ├── login_request.py    # Login request schema
│   └── user.py             # SQLAlchemy user model
├── repository/
│   ├── booking_repository.py
│   └── user_repository.py
├── routes/
│   ├── auth_routes.py
│   ├── booking_routes.py
│   └── room_routes.py
├── services/
│   ├── auth_services.py
│   ├── booking_service.py
│   └── room_services.py
├── tests/
│   └── test_password_handler.py
├── utils/
│   └── database.py         # SQLAlchemy engine and DB session dependency
├── .env                    # Local environment configuration (not committed)
├── app.py                  # FastAPI application
├── config.py               # Environment-based configuration
├── create_db.py            # Database table creation and demo-user seed
├── meetingdb.mv.db         # Local H2 database, created at runtime
├── requirements.txt
├── rooms.json              # Static room inventory
└── README.md
```

## API documentation

All endpoints require a JWT bearer token except `POST /login`. Get a token
from the login endpoint, then send it on protected requests:

```http
Authorization: Bearer <access_token>
```

### Login

`POST /login` — public.

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Success response (`200`):

```json
{
  "access_token": "<jwt_token>",
  "token_type": "Bearer"
}
```

Invalid credentials return `401`.

### Profile

`GET /profile` — authenticated. Returns the current user's full name and
username.

### List rooms

`GET /rooms` — authenticated. Returns the room objects loaded from
`rooms.json`.

### Get a room

`GET /rooms/{room_id}` — authenticated. Returns the requested room, or `404`
if no room has that ID.

### Create a booking

`POST /book-room` — authenticated. Users can create multiple bookings.

Request:

```json
{
  "room_id": 1,
  "booking_date": "2026-10-22",
  "start_time": "10:00",
  "end_time": "11:00"
}
```

The room must exist, the start time must be earlier than the end time, and
the requested slot must not overlap another active booking for that room and
date. Times use the 24-hour `HH:MM` format. `24:00` may be used as an end
time to indicate midnight, but not as a start time. Successful requests return
a booking ID and confirmation message.

### List the current user's bookings

`GET /my-bookings` — authenticated. Returns bookings for the current user.

### Get booking details

`GET /booking/{booking_id}` — authenticated. Returns the booking with the
requested ID, or `404` if it does not exist.

### Cancel a booking

`DELETE /booking/{booking_id}` — authenticated. The booking owner can cancel
their booking. Cancellation changes its status to `CANCELLED`; it does not
delete the database row.

FastAPI's interactive documentation at `/docs` provides request and response
schemas for each endpoint.

## Assumptions

- No UI or frontend is included; this project provides an API only.
- The application has one standard user type and does not implement user
  roles or role-based permissions. The seeded `admin` account is a demo
  username, not an elevated role.
- Room inventory is static data stored in `rooms.json`. API endpoints may
  read rooms but cannot add, edit, or delete them.
- A user may create multiple bookings.
- Authentication is required for every API endpoint except `POST /login`.
- A booking can be made only for a room present in the JSON inventory.
- A booking's start time must precede its end time.
- Active bookings for the same room and date cannot overlap.
- Users can list their own bookings and cancel only their own bookings.
- Cancellation retains the booking record and sets its status to
  `CANCELLED`.
- User and booking records are stored in the H2 database through SQLAlchemy.
- Java/JDBC is required by the H2 connector; SQLAlchemy is the application's
  ORM interface to the database.
