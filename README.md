# Chat Room using Django Channels
Web based chat room where users can create groups, add people to group and chat in those groups. This is similar to whats app chat, messanger chat, etc. 
Purpose of this repository is to learn how Asynchronous web communication works(Socket duplex connection). And implement simple web based chat application using Django channels and Angular client framework.

## Software Requirements
1. Python 3.7+
2. Angular 15.2.0

Application uses Django Channels for Asynchronous communication, Sqlite database for storing transactional data and Angular framework for user interface. 

## Run Backend Service

1. Navigate to folder ```./src/core```
2. Create a virtual environment
   ```
   python -m venv venv
   ```
3. Activate the virtual environment
   ```
   venv\Scripts\activate
   ```
4. Install packages
   ```
   pip install -r requirements.txt
   ```
5. Migrate DB changes
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Run the service
   ```
   py manage.py runserver
   ```

## Run Frontend Service

1. Navigate to folder ```./src/Clientapp```
2. Install Node packages
    ```
    npm install
    ```
3. Start the server
    ```
    ng serve --ssl
    ```
