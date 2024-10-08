# bulletin_board

This backend part is intended for an ad posting site. 
The aim of the project is to provide functionality for managing ads and interacting with users.

## Main Functionality 

1. User authorization and authentication.
2. Role distribution among users (user and admin).
3. Password recovery via email.
4. CRUD for ads on the site (admin can delete or edit all ads, users – only their own).
5. Ability to leave reviews under ads.
6. Search for ads by title in the site header.

## Setup
Follow the steps below to setup and run the project locally:

1. Clone the Repository.
2. Setup a Virtual Environment.
Navigate to your project directory and create a virtual environment using the command:
python3 -m venv venv
3. Activate the Virtual Environment.
Activate the virtual environment using the following command:
source venv/bin/activate
4. Install Dependencies.
Install all the required dependencies from the 'requirements.txt' file using the command:
pip install -r requirements.txt
5. Setup Environment Variables.
Create an .env file in the root directory of your project and define the variables 
that are in the .env.sample file
6. Initialize the Database.
python manage.py migrate
7. Start the Server
Run the command below to start Django's development server:
python manage.py runserver
The server should now be accessible on http://localhost:8000/

## Installation

As Postman is used for result visualization, the project setup will include its usage. 

1. Install Postman if you don't have it yet. It can be downloaded [here](https://www.postman.com/downloads/).
2. Clone the repository: git@github.com:glebskotnikov/bulletin_board.git
3. Install project dependencies (this command assumes that you are in the root directory of the project): pip install -r requirements.txt 
4. Run the server: python3 manage.py runserver

## Usage 

Use Postman to test the web application.

1. When your server is running, open Postman.
2. Create a new request (e.g., GET, POST, etc.).
3. Insert the server URL, for example, `http://localhost:8000/`.
4. If required, add the request body in JSON format or enter necessary parameters.
5. Press the "Send" button to send the request.
6. The server's response will be displayed at the bottom of the window.

This project provides several API endpoints for interacting with the application:

- `POST /users/register`: Register a new user.
- `POST /users/login`: Log in an existing user.
- `POST /users/reset_password/`: POST route that triggers a password reset process.
- `POST /users/reset_password_confirm/`: POST route that confirms the user's password reset request.


- `GET /api/ads/`: Getting a list of all advertisements.
- `POST /api/ads/`: Creating a new ad.
- `GET /api/ads/<int:pk>/`: Detailed information about the advertisement.
- `PUT /api/ads/<int:pk>/`: Modifying an existing ad.
- `PATCH /api/ads/<int:pk>/`: Partially updates the details of a particular ad.
- `DELETE /api/ads/<int:pk>/`: This operation deletes a particular ad.


- `GET /api/reviews/`: Getting a list of all reviews.
- `POST /api/reviews/`: Creating a new review.
- `GET /api/reviews/<int:pk>/`: Detailed information about the review.
- `PUT /api/reviews/<int:pk>/`: Modifying an existing review.
- `PATCH /api/reviews/<int:pk>/`: Partially updates the details of a particular review.
- `DELETE /api/reviews/<int:pk>/`: This operation deletes a particular review.


## Docker-compose

1. Install Docker if you don't already have it. You can download it [here](https://docs.docker.com/).
2. Type the command in the terminal: docker-compose up -d --build
