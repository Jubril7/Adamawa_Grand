# eProject Report
# Hotel Room Booking System
### Adamawa Grand Hotel & Suites — Yola, Adamawa State, Nigeria
### Developed with Django (Python Web Framework)

---

## Table of Contents

1. Acknowledgements
2. eProject Synopsis
3. eProject Analysis
4. eProject Design
   - Data Flow Diagrams (DFDs)
   - Flowcharts
   - Process Diagrams
   - Database Design / Structure
5. Screen Descriptions
6. Source Code Structure with Comments Guide
7. User Guide (User Manual)
8. Developer's Guide
   - Module Descriptions

---

## 1. Acknowledgements

This project, **Adamawa Grand Hotel & Suites — Hotel Room Booking System**, was developed as an eProject submission for Aptech Computer Education.

The system was built using industry-standard tools and best practices, including the Django web framework, SQLite database, Bootstrap 5 for the front-end, and Python-Decouple for secure environment management.

Special acknowledgement is given to:
- The Aptech eProjects Team for providing the project specification and learning framework.
- The Django Software Foundation for the excellent open-source framework.
- The Bootstrap Team for the responsive UI toolkit.
- Nigeria's Adamawa State — the rich cultural heritage of which inspired the design and theme of this application.

---

## 2. eProject Synopsis

### Project Title
Hotel Room Booking System — Adamawa Grand Hotel & Suites

### Technology Stack
| Layer       | Technology                         |
|-------------|-------------------------------------|
| Language    | Python 3.x                         |
| Framework   | Django 4.2 (LTS)                   |
| Database    | SQLite (development) / PostgreSQL ready |
| Front-End   | Bootstrap 5, HTML5, CSS3, JavaScript |
| Auth        | Django Custom User Model (AbstractUser) |
| Form Rendering | django-crispy-forms + crispy-bootstrap5 |
| Static Files | WhiteNoise                         |
| Environment | python-decouple (.env)             |

### Summary
The Hotel Room Booking System is a full-stack web application that enables guests to search, view and book hotel rooms online. Administrators manage rooms, bookings and customer data through a dedicated admin dashboard.

The application is themed around **Adamawa Grand Hotel & Suites**, located in Yola, the capital of Adamawa State, Nigeria — a state known for the Kiri Dam, Sukur Cultural Landscape (UNESCO World Heritage Site), and the Mandara Mountains.

### Problem Being Solved
Hotels traditionally rely on walk-in or phone bookings, causing:
- Long queues and poor guest experience
- No real-time room availability visibility
- Manual, error-prone booking management

This system resolves all three by providing a 24/7 online booking platform.

---

## 3. eProject Analysis

### User Roles

#### 3.1 Guest User (Unauthenticated)
- View the hotel home page with hero images and featured rooms
- Browse all available rooms with filters (type, capacity, price)
- View detailed room information and amenities
- Submit a contact/enquiry form
- View hotel information and nearby Adamawa attractions
- Register for an account

#### 3.2 Registered User (Authenticated)
- All guest features
- Book available rooms (select dates, guests, special requests)
- View all their bookings with status tracking
- View individual booking details
- Cancel pending or approved bookings
- Update personal profile (name, phone, photo, etc.)

#### 3.3 Admin (Superuser)
- Full Django Admin panel access
- Add, update, delete room types and rooms
- Manage room availability and pricing
- View and manage all customer bookings
- Approve or reject bookings (change status)
- Manage registered customers
- Read and manage contact form messages
- Manage hero slider images on the home page

### Functional Requirements
| ID  | Requirement                                              | Priority |
|-----|----------------------------------------------------------|----------|
| FR1 | Users can register and log in securely                   | High     |
| FR2 | Users can search and filter available rooms              | High     |
| FR3 | Users can book rooms with date selection                 | High     |
| FR4 | Users can view and cancel their bookings                 | High     |
| FR5 | Admin can approve/reject bookings                        | High     |
| FR6 | Admin can manage rooms and room types                    | High     |
| FR7 | Guests can submit contact enquiries                      | Medium   |
| FR8 | Total booking price is auto-calculated                   | Medium   |
| FR9 | User profiles can be updated                             | Medium   |
| FR10| Hero slider manageable by admin                         | Low      |

### Non-Functional Requirements
- **Security**: CSRF protection on all forms, secure password hashing, login required for booking
- **Performance**: WhiteNoise static file serving, `select_related` on DB queries
- **Scalability**: Settings structured for easy PostgreSQL migration
- **Usability**: Responsive Bootstrap 5 UI, works on mobile and desktop
- **Maintainability**: Django app-based architecture, each concern in its own app

---

## 4. eProject Design

### 4.1 Data Flow Diagrams (DFDs)

#### Level 0 — Context Diagram
```
                    ┌───────────────┐
    Guest User ────>│               │
                    │               │────> Room Listings
  Registered  ────>│  HOTEL ROOM   │
     User           │  BOOKING      │────> Booking Confirmation
                    │  SYSTEM       │
     Admin    ────>│               │────> Admin Reports
                    └───────────────┘
```

#### Level 1 — Main Processes
```
Guest User
    │
    ├──> [1.0 Browse Rooms] ──────────────────> Room Catalogue
    │         │
    │         └──> Filtered Room List
    │
    ├──> [2.0 User Registration/Login] ──────> User Store
    │
    └──> [3.0 Contact Enquiry] ─────────────> Messages Store

Registered User
    │
    ├──> [4.0 Book Room] ────────────────────> Booking Store
    │         │
    │         └──> Total Price Calculation
    │
    ├──> [5.0 View/Cancel Bookings] ─────────> Booking Store
    │
    └──> [6.0 Update Profile] ───────────────> User Store

Admin
    │
    ├──> [7.0 Manage Rooms] ─────────────────> Room Store
    ├──> [8.0 Manage Bookings] ──────────────> Booking Store
    └──> [9.0 View Messages] ────────────────> Messages Store
```

### 4.2 Flowcharts

#### Room Booking Flowchart
```
START
  │
  ▼
User visits /rooms/
  │
  ▼
Browse & filter rooms
  │
  ▼
Click "View Details" on a room
  │
  ▼
Is user logged in?
  │
  ├── NO ──> Redirect to Login ──> After login, back to booking
  │
  └── YES
        │
        ▼
      Fill Booking Form (check-in, check-out, guests, requests)
        │
        ▼
      Is form valid?
        │
        ├── NO ──> Show validation errors ──> (loop back)
        │
        └── YES
              │
              ▼
            Is num_guests <= room.capacity?
              │
              ├── NO ──> Show error message ──> (loop back)
              │
              └── YES
                    │
                    ▼
                  Save Booking (status = PENDING)
                  Calculate total price
                    │
                    ▼
                  Show success message
                    │
                    ▼
                  Redirect to My Bookings
                    │
                    ▼
                  END
```

#### Admin Booking Approval Flowchart
```
START
  │
  ▼
Admin logs into /admin/
  │
  ▼
Goes to Bookings section
  │
  ▼
Views pending bookings list
  │
  ▼
Selects a booking
  │
  ▼
Decision: Approve or Cancel?
  │
  ├── APPROVE ──> Status = "approved" ──> Save ──> Guest notified
  │
  └── CANCEL  ──> Status = "cancelled" ──> Save ──> END
```

#### User Registration Flowchart
```
START
  │
  ▼
Visit /accounts/register/
  │
  ▼
Fill registration form
  │
  ▼
Form valid?
  │
  ├── NO ──> Show field errors ──> (loop)
  │
  └── YES
        │
        ▼
      Username/email unique?
        │
        ├── NO ──> Show uniqueness error ──> (loop)
        │
        └── YES
              │
              ▼
            Create user account (hashed password)
              │
              ▼
            Auto-login
              │
              ▼
            Redirect to Home with welcome message
              │
              ▼
            END
```

### 4.3 Process Diagrams

#### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT BROWSER                       │
│              (HTML + Bootstrap 5 + JS)                   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   DJANGO WSGI SERVER                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  URL Router                       │   │
│  │  /          → pages.views.home                   │   │
│  │  /rooms/    → rooms.views.room_list              │   │
│  │  /bookings/ → bookings.views.*                   │   │
│  │  /accounts/ → accounts.views.*                   │   │
│  │  /admin/    → Django Admin                       │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │               DJANGO APPS                        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │   │
│  │  │ accounts │ │  rooms   │ │     bookings      │ │   │
│  │  │ ──────── │ │ ──────── │ │     ─────────     │ │   │
│  │  │ models   │ │ models   │ │     models        │ │   │
│  │  │ views    │ │ views    │ │     views         │ │   │
│  │  │ forms    │ │ admin    │ │     forms         │ │   │
│  │  │ admin    │ │ urls     │ │     admin, urls   │ │   │
│  │  └──────────┘ └──────────┘ └──────────────────┘ │   │
│  │  ┌──────────────────────────────────────────────┐│   │
│  │  │                  pages                       ││   │
│  │  │  models (HeroSlide, ContactMessage)          ││   │
│  │  │  views (home, about, contact)                ││   │
│  │  └──────────────────────────────────────────────┘│   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │             DJANGO ORM → SQLite DB               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 4.4 Database Design / Structure

#### Entity Relationship Overview

```
CustomUser ─────────────< Booking >─────────────── Room
                                                     │
                                                     │
                                               RoomType

pages: HeroSlide (standalone)
       ContactMessage (standalone)
```

#### Table: accounts_customuser
| Column           | Type         | Constraints      | Description                  |
|------------------|--------------|------------------|------------------------------|
| id               | BigInt       | PK, Auto         | Primary key                  |
| username         | Varchar(150) | Unique, NOT NULL | Login username               |
| first_name       | Varchar(150) | Optional         | First name                   |
| last_name        | Varchar(150) | Optional         | Last name                    |
| email            | Varchar(254) | Optional         | Email address                |
| password         | Varchar(128) | NOT NULL         | Hashed password (PBKDF2)     |
| phone_number     | Varchar(15)  | Optional         | Nigerian mobile number       |
| address          | Text         | Optional         | Home address                 |
| profile_picture  | ImageField   | Optional         | Uploaded profile photo       |
| date_of_birth    | Date         | Optional         | Date of birth                |
| is_active        | Boolean      | Default: True    | Account active status        |
| is_staff         | Boolean      | Default: False   | Admin access flag            |
| date_joined      | DateTime     | Auto             | Account creation timestamp   |

#### Table: rooms_roomtype
| Column      | Type         | Constraints   | Description          |
|-------------|--------------|---------------|----------------------|
| id          | BigInt       | PK, Auto      | Primary key          |
| name        | Varchar(50)  | Unique        | e.g. Standard, Suite |
| description | Text         | Optional      | Type description     |

#### Table: rooms_room
| Column          | Type           | Constraints         | Description               |
|-----------------|----------------|---------------------|---------------------------|
| id              | BigInt         | PK, Auto            | Primary key               |
| room_number     | Varchar(10)    | Unique, NOT NULL    | e.g. "101", "401"         |
| room_type_id    | BigInt         | FK → RoomType       | Room classification       |
| price_per_night | Decimal(10,2)  | NOT NULL            | Price in Nigerian Naira   |
| capacity        | SmallInt       | Default: 2          | Max number of guests      |
| description     | Text           | NOT NULL            | Room description          |
| amenities       | Text           | Optional            | Comma-separated amenities |
| image           | ImageField     | Optional            | Room photo                |
| is_available    | Boolean        | Default: True       | Booking availability flag |
| floor           | SmallInt       | Default: 1          | Floor number              |
| created_at      | DateTime       | Auto                | Creation timestamp        |

#### Table: bookings_booking
| Column           | Type          | Constraints        | Description                    |
|------------------|---------------|--------------------|--------------------------------|
| id               | BigInt        | PK, Auto           | Primary key (booking number)   |
| user_id          | BigInt        | FK → CustomUser    | Guest who made the booking     |
| room_id          | BigInt        | FK → Room          | Room being booked              |
| check_in_date    | Date          | NOT NULL           | Arrival date                   |
| check_out_date   | Date          | NOT NULL           | Departure date                 |
| num_guests       | SmallInt      | Default: 1         | Number of guests               |
| total_price      | Decimal(12,2) | Auto-calculated    | price_per_night × num_nights   |
| status           | Varchar(20)   | Default: 'pending' | pending/approved/cancelled/completed |
| special_requests | Text          | Optional           | Guest special requirements     |
| created_at       | DateTime      | Auto               | Booking creation time          |
| updated_at       | DateTime      | Auto               | Last modification time         |

#### Table: pages_heroslide
| Column    | Type        | Constraints  | Description               |
|-----------|-------------|--------------|---------------------------|
| id        | BigInt      | PK, Auto     | Primary key               |
| title     | Varchar(100)| NOT NULL     | Slide heading             |
| subtitle  | Varchar(200)| Optional     | Slide subheading          |
| image     | ImageField  | NOT NULL     | Slide background image    |
| is_active | Boolean     | Default: True| Toggle visibility         |
| order     | SmallInt    | Default: 0   | Display order             |

#### Table: pages_contactmessage
| Column     | Type         | Constraints | Description              |
|------------|--------------|-------------|--------------------------|
| id         | BigInt       | PK, Auto    | Primary key              |
| name       | Varchar(100) | NOT NULL    | Sender's name            |
| email      | EmailField   | NOT NULL    | Sender's email           |
| phone      | Varchar(15)  | Optional    | Sender's phone           |
| subject    | Varchar(200) | NOT NULL    | Message subject          |
| message    | Text         | NOT NULL    | Message body             |
| created_at | DateTime     | Auto        | Submission time          |
| is_read    | Boolean      | Default: False | Admin read status     |

---

## 5. Screen Descriptions

| Screen                     | URL                         | Access       | Description                                      |
|----------------------------|-----------------------------|--------------|--------------------------------------------------|
| Home Page                  | /                           | Public       | Hero section, featured rooms, attractions        |
| Rooms List                 | /rooms/                     | Public       | Filterable grid of available rooms               |
| Room Detail                | /rooms/<id>/                | Public       | Full room info with amenities and booking button |
| About Us                   | /about/                     | Public       | Hotel info, services, statistics                 |
| Contact Us                 | /contact/                   | Public       | Enquiry form with hotel contact details          |
| Register                   | /accounts/register/         | Guest only   | New user registration form                       |
| Login                      | /accounts/login/            | Guest only   | Username/password login                          |
| Profile                    | /accounts/profile/          | Logged in    | View and edit personal profile                   |
| Book Room                  | /bookings/book/<room_id>/   | Logged in    | Booking form with date pickers                   |
| My Bookings                | /bookings/my/               | Logged in    | List of user's bookings with status              |
| Booking Detail             | /bookings/<id>/             | Logged in    | Full booking details and cancellation option     |
| Cancel Booking             | /bookings/<id>/cancel/      | Logged in    | Confirmation page before cancellation            |
| Admin Dashboard            | /admin/                     | Admin only   | Full Django admin for managing all data          |

---

## 6. Source Code Structure with Comments Guide

### Project Structure
```
HotelRoomBooking/
│
├── config/                  # Django project configuration
│   ├── settings.py          # All project settings (DB, apps, auth, etc.)
│   ├── urls.py              # Root URL configuration — routes to all apps
│   └── wsgi.py              # WSGI entry point for deployment
│
├── accounts/                # User authentication & profile management
│   ├── models.py            # CustomUser extends AbstractUser (adds phone, address, etc.)
│   ├── forms.py             # RegisterForm (UserCreationForm), ProfileUpdateForm
│   ├── views.py             # register_view, login_view, logout_view, profile_view
│   ├── admin.py             # CustomUserAdmin with extended fieldsets
│   └── urls.py              # /register/, /login/, /logout/, /profile/
│
├── rooms/                   # Room catalogue management
│   ├── models.py            # RoomType, Room (with get_amenities_list method)
│   ├── views.py             # room_list (with filters), room_detail
│   ├── admin.py             # RoomAdmin with list_editable for quick price/availability changes
│   └── urls.py              # /rooms/, /rooms/<pk>/
│
├── bookings/                # Booking engine
│   ├── models.py            # Booking model — auto-calculates total_price on save
│   ├── forms.py             # BookingForm with date validation (no past dates, checkout > checkin)
│   ├── views.py             # book_room, my_bookings, booking_detail, cancel_booking
│   ├── admin.py             # BookingAdmin with status management
│   └── urls.py              # /bookings/book/<pk>/, /bookings/my/, etc.
│
├── pages/                   # Static-ish pages (home, about, contact)
│   ├── models.py            # HeroSlide (carousel management), ContactMessage
│   ├── forms.py             # ContactForm (ModelForm)
│   ├── views.py             # home, about, contact
│   ├── admin.py             # HeroSlideAdmin, ContactMessageAdmin
│   └── urls.py              # /, /about/, /contact/
│
├── templates/               # All HTML templates (Django template language)
│   ├── base.html            # Master layout — navbar + footer + messages
│   ├── partials/
│   │   ├── navbar.html      # Responsive Bootstrap 5 navbar with auth-aware links
│   │   └── footer.html      # Footer with hotel contact info & Adamawa attractions
│   ├── pages/               # home.html, about.html, contact.html
│   ├── rooms/               # list.html, detail.html
│   ├── bookings/            # book.html, my_bookings.html, booking_detail.html, cancel_confirm.html
│   └── accounts/            # register.html, login.html, profile.html
│
├── static/
│   ├── css/style.css        # Custom CSS — gold/navy Adamawa colour theme, all component styles
│   └── js/main.js           # Navbar scroll effect, alert auto-dismiss, booking price preview
│
├── media/                   # User-uploaded files (profile pictures, room images, slides)
│
├── .env                     # Environment variables (SECRET_KEY, DEBUG) — NOT committed to git
├── .env.example             # Template for .env — committed to git
├── .gitignore               # Excludes .env, __pycache__, db.sqlite3, media/, staticfiles/
├── requirements.txt         # Python package dependencies
└── manage.py                # Django management CLI entrypoint
```

### Key Code Patterns Used

**Custom User Model** (`accounts/models.py`):
The project uses `AUTH_USER_MODEL = 'accounts.CustomUser'` — set before any migrations are created. This is the recommended Django best practice.

**Auto Price Calculation** (`bookings/models.py`):
The `Booking.save()` method automatically calls `calculate_total()` which multiplies `room.price_per_night × num_nights` before saving to the database.

**Form Validation** (`bookings/forms.py`):
The `BookingForm.clean()` method validates that check-in is not in the past and check-out is strictly after check-in, giving user-friendly error messages.

**Query Optimization** (`bookings/views.py`):
`select_related('room', 'room__room_type')` is used on booking queries to avoid N+1 database queries.

---

## 7. User Guide (User Manual)

### 7.1 Getting Started

**Accessing the System:**
Open your web browser and go to: `http://127.0.0.1:8000/` (or the deployed URL)

---

### 7.2 Guest User Guide

#### Viewing Rooms
1. From the **Home page**, click **"Explore Rooms"** or **"View All Rooms"**
2. You will see the rooms listing page at `/rooms/`
3. Use the filter bar at the top to narrow results by:
   - **Room Type** — Standard, Deluxe, Suite, Presidential Suite
   - **Min. Capacity** — minimum number of guests the room must accommodate
   - **Max Price (₦/night)** — your maximum budget per night
4. Click **"Details"** on any room card to see full information

#### Submitting a Contact Enquiry
1. Click **"Contact"** in the navigation bar
2. Fill in your name, email, phone (optional), subject and message
3. Click **"Send Message"**
4. A confirmation message will appear on screen

---

### 7.3 Registered User Guide

#### Creating an Account
1. Click **"Register"** in the top-right navigation bar
2. Fill in the form:
   - **Username** — your unique login name
   - **First Name** and **Last Name**
   - **Email** — valid email address
   - **Phone Number** (optional)
   - **Password** — minimum 8 characters, not too common
   - **Confirm Password** — must match
3. Click **"Create Account"**
4. You will be automatically logged in and taken to the home page

#### Logging In
1. Click **"Login"** in the navigation bar
2. Enter your **Username** and **Password**
3. Click **"Login"**
4. A welcome message will appear and you'll be redirected

#### Booking a Room
1. Browse rooms and click **"View Details"** on the room you want
2. Click **"Book This Room"** (you must be logged in)
3. Fill in the booking form:
   - **Check-in Date** — select your arrival date (cannot be in the past)
   - **Check-out Date** — must be after check-in date
   - **Number of Guests** — cannot exceed the room's stated capacity
   - **Special Requests** — optional (e.g. early check-in, extra pillows)
4. Click **"Confirm Booking"**
5. A success message shows your booking number and status: **Pending**

> **Note:** All bookings start as "Pending" and must be approved by hotel admin before they become "Approved".

#### Viewing Your Bookings
1. Click your name in the top navigation bar
2. Select **"My Bookings"** from the dropdown
3. You will see a list of all your bookings with their status:
   - 🟡 **Pending** — awaiting admin approval
   - 🟢 **Approved** — confirmed by the hotel
   - 🔴 **Cancelled** — cancelled by you or the hotel
   - 🔵 **Completed** — stay has been completed

#### Cancelling a Booking
1. Go to **My Bookings**
2. Find the booking you want to cancel (must be Pending or Approved)
3. Click **"Cancel"** then confirm on the next screen
4. The booking status will change to **Cancelled**

> **Important:** Completed bookings cannot be cancelled.

#### Updating Your Profile
1. Click your name in the top navigation bar
2. Select **"Profile"**
3. Update any of: First/Last Name, Email, Phone, Address, Profile Picture, Date of Birth
4. Click **"Save Changes"**

#### Logging Out
1. Click your name in the top navigation bar
2. Click **"Logout"**
3. You will be redirected to the home page

---

### 7.4 Admin User Guide

#### Accessing the Admin Panel
1. Go to `/admin/` in your browser
2. Log in with your administrator credentials
   - Default: username `admin`, password `Admin@1234` *(change this immediately in production)*

#### Managing Rooms
1. In the admin panel, click **"Rooms"**
2. Click **"Add Room"** to create a new room — fill in room number, type, price, capacity, floor, description, amenities and upload an image
3. Click any existing room to edit it
4. Toggle **"Is available"** to quickly mark a room as unavailable for booking

#### Managing Bookings
1. Click **"Bookings"** in the admin panel
2. You will see all bookings with status, dates and total price
3. To approve a booking: click on it and change **Status** to **"Approved"**, then save
4. To cancel: change **Status** to **"Cancelled"**
5. You can also change status in the list view using the **inline editable Status column**

#### Managing Contact Messages
1. Click **"Contact messages"** in the admin panel
2. View messages from guests
3. Mark messages as read using the **"Is read"** checkbox

#### Managing Hero Slides
1. Click **"Hero slides"** in the admin panel
2. Add slides with a title, subtitle and upload an image
3. Set the **order** to control which slide appears first
4. Toggle **"Is active"** to show/hide slides

---

## 8. Developer's Guide

### 8.1 Setup Instructions

**Prerequisites:**
- Python 3.10+
- pip3

**Installation:**
```bash
# Clone or download the project
cd HotelRoomBooking

# Install dependencies
pip3 install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Edit .env and set a new SECRET_KEY

# Apply database migrations
python3 manage.py migrate

# Create admin superuser
python3 manage.py createsuperuser

# Load seed data (optional — adds sample rooms)
python3 manage.py shell < seed.py  # if seed script is provided

# Run development server
python3 manage.py runserver
```

Access the app at: http://127.0.0.1:8000/

---

### 8.2 Module Descriptions

#### Module: `accounts`
**Purpose:** Handles all user authentication, registration and profile management.

| Component             | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `CustomUser` model    | Extends Django's `AbstractUser`. Adds `phone_number`, `address`, `profile_picture`, `date_of_birth`. Set as `AUTH_USER_MODEL` in settings. |
| `RegisterForm`        | Inherits `UserCreationForm`. Adds `email`, `first_name`, `last_name`, `phone_number`. Auto-saves all extra fields. |
| `ProfileUpdateForm`   | `ModelForm` for `CustomUser`. Allows editing of personal info and uploading a profile picture. |
| `register_view`       | Creates a new user, logs them in immediately, redirects to home.            |
| `login_view`          | Uses Django's built-in `AuthenticationForm`. Handles `?next=` redirect.    |
| `logout_view`         | POST-only logout (CSRF protected). Redirects to home.                       |
| `profile_view`        | Requires login. Handles GET (display form) and POST (save changes).        |

---

#### Module: `rooms`
**Purpose:** Manages the room catalogue — types, details and availability.

| Component             | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `RoomType` model      | Simple lookup table. Examples: Standard, Deluxe, Suite, Presidential Suite. |
| `Room` model          | Core room entity. Linked to `RoomType` via FK. `get_amenities_list()` splits the comma-separated amenities string into a Python list for template rendering. |
| `room_list` view      | Fetches `is_available=True` rooms. Supports GET query filters: `type`, `capacity`, `max_price`. Uses `select_related` for query efficiency. |
| `room_detail` view    | Fetches a single room by PK using `get_object_or_404`.                     |

---

#### Module: `bookings`
**Purpose:** The booking engine — creating, viewing and cancelling bookings.

| Component             | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `Booking` model       | Links `CustomUser` to `Room`. Status choices: pending, approved, cancelled, completed. The `save()` override calls `calculate_total()` to set `total_price = price_per_night × num_nights`. The `can_cancel()` method returns True only for pending/approved bookings. |
| `BookingForm`         | Date pickers via `type="date"`. `clean()` validates: no past dates, check-out > check-in. |
| `book_room` view      | Login-required. Validates guest count against room capacity. Creates booking with `status=pending`. |
| `my_bookings` view    | Login-required. Lists all bookings for `request.user`, ordered by most recent. |
| `booking_detail` view | Login-required. Shows full booking info. Only accessible by the booking owner. |
| `cancel_booking` view | Login-required. GET shows confirmation page. POST changes status to cancelled. |

---

#### Module: `pages`
**Purpose:** Public-facing informational pages — home, about, contact.

| Component               | Description                                                               |
|-------------------------|---------------------------------------------------------------------------|
| `HeroSlide` model       | Stores carousel images for the home page hero section. Managed via admin. |
| `ContactMessage` model  | Stores contact form submissions. Admin can mark as read.                  |
| `ContactForm`           | Simple `ModelForm` for `ContactMessage`.                                  |
| `home` view             | Fetches active `HeroSlide` objects and up to 6 featured rooms.            |
| `about` view            | Static view — renders the about page template.                            |
| `contact` view          | Handles contact form GET (show form) and POST (save + redirect).         |

---

#### Module: `config` (Project Settings)
| Setting               | Value / Purpose                                                            |
|-----------------------|----------------------------------------------------------------------------|
| `AUTH_USER_MODEL`     | `'accounts.CustomUser'` — custom user model                               |
| `TIME_ZONE`           | `'Africa/Lagos'` — West Africa Time (WAT, UTC+1)                          |
| `CRISPY_TEMPLATE_PACK`| `'bootstrap5'` — Bootstrap 5 form rendering                               |
| `STATICFILES_STORAGE` | `WhiteNoise` — efficient static file serving                               |
| `EMAIL_BACKEND`       | Console backend for development; swap for SMTP in production              |
| `LOGIN_URL`           | `'accounts:login'`                                                         |
| `LOGIN_REDIRECT_URL`  | `'pages:home'`                                                             |

---

### 8.3 Adding a New Room Type
1. In admin panel → Room Types → Add Room Type
2. Or via Django shell:
```python
from rooms.models import RoomType
RoomType.objects.create(name='Family Suite', description='Two-bedroom family suite')
```

### 8.4 Environment Variables (.env)
| Variable       | Description                                 |
|----------------|---------------------------------------------|
| `SECRET_KEY`   | Django secret key (never share/commit this) |
| `DEBUG`        | `True` in development, `False` in production|
| `ALLOWED_HOSTS`| Comma-separated allowed hostnames           |

### 8.5 Switching to PostgreSQL (Production)
Replace the `DATABASES` setting in `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```
Then run `pip3 install psycopg2-binary` and re-run migrations.

---

*End of eProject Report*
*Adamawa Grand Hotel & Suites — Hotel Room Booking System*
*Developed with Django, Bootstrap 5 | Yola, Adamawa State, Nigeria*
