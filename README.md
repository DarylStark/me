# Me

This project will be te continued development of the project me-dstark-nl. This project was started a while ago to create a personal assistant called 'me-dstark-nl' in Python 2. After creating a fine project, I found out a lot of things could be done better, so I satrted a new one in Python 3. This one was fine, but created in a monolithic way. I decided to recreate this one in Python 3 with microservices. A lot of the code of the Python3 version of 'me-dstark-nl' will be reused though.

# Microservices

As stated, this application will be created using microservices. The source code will be divided in a few parts:

- Google App Engine application
- A Python 3 package to interact with the Google App Engine application

## Google App Engine application

This will be the hart of the Personal Assistant and will run on Google App Engine (hence the name). This application is an REST API and web front-end. The services that run in this application are:

- `default-v1`: this is the default service that gets called when a unknown resource gets called
- `rest-api-v1`: the first version of the REST API that controlls the complete application
- `web-gui-v1`: a web interface to interact with the application

## Python 3 package

The Python 3 package will contain a package that can be imported to interact with the API of the Google App Engine application. It will also contain a CLI tool to interact with the Google App Engine application.

# API flow to authenticate

The application uses multiple ways to authenticate a user. A client (like the web interface or the CLI client) should have a client token. This token should be generated in the application itself by a authenticated user. The client then uses this client key to request a user key from the system (if the application is allowed to). The user key is used to authenticate as a specific user so the client can do things on behalf of the user.

The user key should be saved in a secure place by the client since it can be used by anyone to imitate the client and use the application on the users behalf. That means that a web-application, for instance, should never reviel te key from a user to other users.