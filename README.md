# Backend Grimosport Project

Preamble: this is an university project for the "Tecnologie Web" (Web Technology) exam. The project is a web application for a sport shop. The project is divided in two parts: the backend and the frontend. This is the backend part. The frontend part is available at this [link](https://github.com/Grimos10/ecommerce-vue).

The course was about learning the basics of web development, so the project is not perfect and it's not complete, it's just a prototype.
Also was about learning Django, so I used Django and Django REST Framework to build the backend.

I decided, just for fun and not beacuse it was necessary, to deploy the project on a server that I manage with a friend of mine, https://grimosport.grimos.dev (API link).

So you can either run the project locally or use the deployed version.
If you want to run the project locally see the [Installation](#installation) and [Usage](#usage) sections.
I raccomend to use the deployed version because it's more complete and it has more data, also this is an API so you can't see the frontend, you can just use the API with a tool like Postman.

## Dependencies and features

This project includes the following features:

- User authentication and authorization
- Product catalog with search and filtering functionality
- Shopping cart and checkout process
- Order management for both customers and administrators

And I used the following dependencies:

- `django`
- `django-rest-framework`
- `django-cors-headers`: (for CORS)
- `djoser`: (for authentication)
- `pillow`: (for image processing)
- `django-environ`: (for environment variables)
- `stripe`: (for payments) see [stripe and payments](#stripe-and-payments) section for more details



## Documentation

### Authentication

I used Djoser to manage authentication. Djoser is a REST implementation of Django authentication system. It provides a set of endpoints to manage users authentication, registration, password reset, etc.

How I handle the authentication process:

1. The user fills the registration form and clicks on the "Register" button
2. The frontend sends a request to the backend with the data of the user
3. The backend creates a new user and sends the data to the frontend
4. The frontend redirects the user to the login page
5. The user fills the login form and clicks on the "Login" button
6. The frontend sends a request to the backend with the data of the user
7. The backend checks if the user exists and sends the data to the frontend
8. The frontend redirects the user to the cart page if he is a customer or to the admin page if he is an admin

### Handling images

I used Pillow to handle images. Pillow is a Python Imaging Library (PIL), it adds image processing capabilities to your Python interpreter.


### Stripe and payments

I used Stripe to manage payments. Stripe is a payment platform that allows you to accept payments online.
I want to specify that I didn't use Stripe because it was necessary, I used it just for fun and to learn something new.
In fact you can use the website without paying, you can just use the test card number `4242 4242 4242 4242` with any CVC, any future expiration date, and any postal code.
This allows you to test the payment process without using a real credit card and create a order so you can see it in your profile.

How I handle the payment process:

1. The user adds items to the cart and goes to the checkout page
2. The user fills the form with his data and clicks on the "Pay" button
3. The frontend sends a request to the backend with the data of the order and the Stripe token
4. The backend creates a new order and sends the data to Stripe
5. Stripe creates a new payment intent and sends the client secret to the backend
6. The backend sends the client secret to the frontend
7. The frontend uses the client secret to confirm the payment
8. Stripe confirms the payment and sends the payment intent to the backend
9. The backend updates the order with the payment intent data
10. The backend sends the order data to the frontend
11. The frontend redirects the user to the order page




## Installation

To install and run the project, follow these steps:

1. Clone the repository: `git clone https://github.com/Grimos10/ecommerce-django.git`
3. Create a new database: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Usage

To use the website, open your web browser and navigate to `http://localhost:8000/`. You can then browse the product catalog, add items to your cart, and complete the checkout process.