# Booki - Library Book Reservation System

A web application that enables users to borrow books from local libraries, write reviews, and discover nearby libraries through location-based services.

## About

**Booki** is a full-featured library management and book reservation platform built with Django. It connects book enthusiasts with local libraries, allowing users to search for books, make reservations, and share their reading experiences through reviews and ratings. The application supports multiple user roles including regular users, librarians, and administrators, each with tailored functionality. Users can locate nearby libraries within a 10km radius, make book reservations, and track their pickup status. Librarians manage their library's inventory, handle reservation requests, and support users throughout the borrowing process.

## Features

- **Book Search & Discovery** - Search for books by title, author, category, or tags with detailed book information and user reviews
- **Location-Based Library Search** - Find nearby libraries within 10km using OpenStreetMap API integration and geographic coordinates
- **Book Reservation System** - Reserve books from libraries with 7-day automatic expiration, cancel requests, or update pickup status
- **User Reviews & Ratings** - Share reading experiences through detailed reviews and rate books to help other readers
- **Role-Based Access Control** - Multi-role system with users, librarians, and administrators, each with tailored permissions and dashboard features

## Tech Stack

- **Backend**: Django 5.1.3
- **Frontend**: Bootstrap 5.3, Bootstrap Icons 1.11, Google Font Roboto
- **Database**: SQLite (Django ORM)
- **APIs**: OpenStreetMap API for location services
- **Tools**: Pylint, autopep8 for code quality

## Project Structure

```
booki/
├── models/                 # Application data models
│   ├── author.py          # Author model
│   ├── book.py            # Book model with relationships
│   ├── category.py        # Book categories
│   ├── library.py         # Library with geographic points
│   ├── library_book.py    # Many-to-many library inventory
│   ├── reserve.py         # Book reservations
│   ├── review.py          # User reviews and ratings
│   ├── tag.py             # Book tags
│   └── user_profile.py    # User address and location data
├── templates/             # HTML templates
│   ├── pages/            # Full page templates
│   ├── components/       # Reusable template components
│   └── ajax/             # AJAX response templates
├── static/               # CSS, JavaScript, images
│   ├── css/              # Stylesheets
│   ├── js/               # Client-side scripts
│   └── img/              # Project images
├── templatetags/         # Custom Django template tags
├── utils/                # Helper functions
│   ├── geo.py            # OpenStreetMap geolocation
│   └── helper.py         # Utility functions
├── views.py              # View logic
├── forms.py              # Django forms
├── urls.py               # URL routing
├── admin.py              # Django admin customization
├── decorators.py         # Custom decorators
└── context_processors.py # Template context processors
```

## Getting Started

### Prerequisites

- Python 3.x
- pip package manager

### Installation

1. **Clone the repository and navigate to the project directory**

   ```bash
   cd booki
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account**

   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data (optional)**
   Create the following in Django admin:
   - A user group named `librarian`
   - Authors, categories, tags, and books
   - Libraries with valid addresses and geographic coordinates
   - Assign books to libraries with shelf information

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Web app: http://127.0.0.1:8000
   - Admin dashboard: http://127.0.0.1:8000/admin
