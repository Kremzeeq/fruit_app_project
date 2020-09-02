# Fruit Web App: A Celebration of Fruit
## Flask app which renders facts and images related to fruit. 


![orange](src/static/assets/base_images/orange-3036097_1920_2.jpg "orange")

This web application renders a homepage with a Bootstrap carousel of 5 random fruit 
and related facts.

### There are 2 key modules to this project:

### 1. [src/app.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/app.py)

* This main module is configured to [src/config.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/config.py)
* A FLASK_ENV variable should be exported as 'development' or 'production' e.g.  
`export FLASK_ENV=production`
* This should be prior to executing `flask run` in the command line

* The first time you run the app, you will need to update the mongo database 
with fruits and facts to render for the homepage.
* Running the **database updater** module as explained below, will ensure that it is populated

### 2. [src/database_updater.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/database.updater.py)

* This app will automatically run from app.py, so long as `UPDATE_FRUIT_AND_FACTS = True` is so in the config file.
* This can be set to False is updating the database is not required 
* When executed, this module reads a CSV from [src/static/data_source/fruit.csv](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/static/data_source/fruit.csv).
* The CSV contains tabular information for fruits and facts.
* This information is split between different pandas dataframes.
* The dataframes are converted to json format as per required by 
the fact and fruit models saved here: [src/models](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/models)
* They are then saved to the database.


## Deploying web application to remote Ubuntu virtual machine e.g. EC2 instance

1. Once E2 instance is up and running, update the system:

`sudo apt-get update`

2.Next, clone the git hub project:

`git clone https://github.com/Kremzeeq/fruit_app_project.git`

3. Check for python3 version:

`python3 -v`

4. Install pip3:

`sudo apt install python3-pip`

5. Now, modules listed in [requirements.txt](https://github.com/Kremzeeq/fruit_app_project/blob/master/requirements.txt) can be installed
from within ~/fruit_app_project$:

`pip3 install -r requirements.txt`

6. Ensure to install mongo. Official instructions from mongo db can be found [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

7. Credentials should be set up for an admin user in mongo...

8. As the admin user we have just created, we set up another user with readWrite privileges for using the
production version of the celebration_of_fruit database as per the [src/config.py] file. Please provide 
user and password login credentials as per preferences: 

**Please note** The login credentials are not hard-coded within mongo for security purposes. 

9. Next the config file requires that three variables are exported within the command line. 
Please ensure this is done from within the src directory from where app.py will be run...

- Username, password, PRODUCTION_DB_SERVER

10. Next, the app can be run with `flask run`






