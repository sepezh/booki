# Booki (Final-Project: Capstone)

powered by: Django v5.1.3, Bootstrap v5.3, Bootstrap icons v1.11, Google font Roboto

Video demo : [https://youtu.be/2Qy7TzS0qRY
](https://youtu.be/2Qy7TzS0qRY)

# Table of Contents
- [Introduction](#introduction)
    - [Features](#features)
    - [Key Learning point](#key-learning-points)
    - [Installation](#installation)
    - [How Booki works](#how-booki-works)
        - [Preparing Data](#preparing-data)
        - [Web application](#web-application)
- [Distinctiveness and complexity](#distinctiveness-and-complexity)
- [Code and organization](#code-and-organization)
   - [Folder Structure : booki](#folder-structure--booki)
   - [Some others](#some-others)


# Introduction
**Booki** is a web application built on Django and styled with Bootstrap, aimed at enabling users to borrow books from local libraries, share their thoughts, and rate their reading experiences. Librarians have the ability to oversee reservations and provide assistance to users.

## Features
- **Users**: Make reservations, write reviews, rate books, and search for titles.
- **Librarians**: Handle reservation requests and support users.
- **Location Integration**: Utilizes the OpenStreetMap API to locate nearby libraries.

---
## Key Learning Points
- **API Integration**: Implemented OpenStreetMap API for location functionalities.
- **Code Quality**: Enhanced using Pylint and autopep8 tools.
- **Customizations**: Included context processors, custom template tags, decorators, and modal forms.
- **Admin Enhancements**: Introduced group-based filtering and user permissions.
---

## Installation and Setup
1. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate 
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Up Database**
```bash
python manage.py migrate
```

5. **Run the Server**
```bash
python manage.py runserver
```


6. **Create Superuser**
```bash
python manage.py createsuperuser
```

## How Booki works

### Preparing Data
before start we need to do some data entry.

1. we need to create a Group call `librarian`
2. define some Author, Category, Tags, Books by superadmin
3. Create some librarian user it means we will create user with and assign group librarian to them.
4. now we need to define some library please be sure the address and geo point are valid because our project will rely on Geographic point of Libraries to find nearest to user and help them.
5. now it times to assign how many book which library have.

### Web application
from `http://127.0.0.1:8000` each client can get some info about each book and author and also can search for book by title, author, tag and category

each user can **register** and **login** with their email/username and password.

for making a **reservation user** need to update or fulfill his address (valid address) then he can find nearest library in 10Km. after he book the client the request will be send as a reservation for library. now it's time to pickup for book from that library or if the user couldn't picked it up. he is able to cancel or the request will be rejected in 7 days.

**librarian** also can login by same way as normal user can by their username and password and then they can manage their library's requests. and set a pickup and return or decline requests.

# Distinctiveness and complexity
Booki is highly distinct from other projects covered in the course and among typical final projects. Unlike general-purpose applications, Booki specifically targets library users and librarians, combining book reservation, review, and location-based services into one cohesive platform. To date, no similar project focusing on a library reservation system with these features has been identified in the course material or student projects.  
- Locate and interact with nearby libraries using OpenStreetMap API integration.  
- Manage different user roles, permissions, and experiences effectively.  
- Offer book reviews and ratings as a value-added service to enhance user engagement.  

Booki demonstrates significant complexity by incorporating multiple advanced features and customizations, including:  
- **Multi-role System**: Seamless interaction between users, librarians, and admins through role-based access control using Django's user groups and permissions.  
- **API Integration**: Integration with the OpenStreetMap API to enable location-based services for finding nearby libraries.  
- **Custom Backend Functionality**: Creation of reusable components such as decorators, custom template tags, and context processors for efficient backend management.  
- **Interactive Frontend**: Implementation of modal-based forms and responsive design using Bootstrap to enhance the user experience.  
- **Enhanced Admin Features**: Customizing the Django admin panel for group filtering and managing permissions, going beyond default capabilities.  
- **Database Management**: Use of advanced database relationships and queries to support book reservations, reviews, and ratings.  
- **Scalability and Maintainability**: A modular folder structure with separated models, views, and templates ensures the project is organized and future-proof.  


# Code and organization
## File and Folder Structure : booki
 - `booki/migrations` :  keep the migrations versions
 - `booki/models` : all models as individual files
    - `__init__.py` will load all models and the models has been listed and imported in it.
    - `author.py` Author's model
    - `book.py` Book's model which has relation with author category and tags
    - `category.py` Category's model
    - `library_book.py` pivot relation many to many table for keeping each library has how many books and in which shelf is it
    - `library.py` Library's model have geo point latitude and longitude
    - `reserve.py` a model for making reservation for books from library by user
    - `review.py` will keep user's reviews for books
    - `tag.py` Tag's model
    - `user_profile.py` for keeping user address and latitude and longitude for making a reservation
 - `booki/static` : all css and javascripts and project images like as booki logo and default user , book image.
    - `css/` all css file will be keep in this directory
    - `img/` will keep all project images
    - `js/` all js has been written in this path
 - `booki/templates` : all Front-end templates
    - `ajax/` all we will return by ajax call has been stored in this directory like as  reservation and message for update profile address
    - `components/` for creating reuseable component and use them in different places we have some components like as paginations , small profile, list of anything and reviews
    - `pages/` will keep each page templates
    - `layout.html` basic layout which will already loaded some css and js and also please consider that _we need to be connected to internet because it will use CDN's of bootstrap and etc._ 
 - `booki/templatetags` : keep extra tags and custom tags which we need in template has been defined in this folder
    - `booki_extras.py` have some tags for templates [How define a custome template tag](https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/)
 - `booki/utils`: some utils like as geo finder and helpers are here
    - `geo.py` will send a request to OpenStreetMap for getting Geo point of address
    - `helper.py` some helpers which will help us to avoid repeat ourself and accessible from different places like as update reservation if has been expired
 - `admin.py` to register models and what we need to superadmin dashboard. we have customized LibraryAdmin for Library which just select user's with group librarian and has not been assigned to another library
 - `apps.py` default config of app
 - `context_processors.py` to preload what we need like as Search form for all request we have
 - `decorators.py` to keep and be able to write some decorator for view functions like as redirect login users when they want to access directly again to login, check ajax call, librarians just can call function
 - `forms.py` contains 
    - Home search field
    - Login form
    - Register form
    - User Profile Form
    - Review Form
- `urls.py` will keep urls
- `views.py` contains with function we need in project

## Some others
- `mysite/settings.py` : 
    - added booki to INSTALLED_APPS
    - define MEDIA_URL
    - added `booki.context_processors.search_field`  TEMPLATES.options.context_processors
    - added messages middleware, tags and context_processors [The messages framework Django Document](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)
- `mysite/urls.py`
    - define url pattern for debug env for access to `/uploads`
    ```python
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.BASE_DIR)
    ```