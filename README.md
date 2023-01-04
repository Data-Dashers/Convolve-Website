# Convolve-Website

## Project Description:

- This is python project to forecast sales of different products.
- Technologies used - Django, ChartJS, Django-Rest_Framework
- This project was done for the second round of Convolve Competition organized by Cisco.


## Installation and Testing:

- Clone the repository using

    ```
    git clone https://github.com/Data-Dashers/Convolve-Website.git
    ```
- Install Python
- Install virtualenv packages using 

    ```
    pip install virtualenv
    ```
- Create a virtual environment with

    ```
    virtualenv <env_name>
    ```
- Activate the virtual environment using :

    For Windows

    ```
    .env_name/Scripts/activate
    ``` 
    For Linux
    
    ```
    source env_name/bin/activate
    ```
- Change directory to the project folder
- Install the required packages using 
    
    ```
    pip install -r requirements.txt
    ```
- Migrate the changes inside the project

    ```
    python manage.py migrate
    ```
- Run the server
    ```
    python manage.py runserver
    ```
- Open localhost:8000 in browser to use the UI
