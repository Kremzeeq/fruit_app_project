# Fruit Web App: A Celebration of Fruit
## Flask app which renders facts and images related to fruit. 


![orange](src/static/assets/base_images/orange-3036097_1920_2.jpg "orange")

This web application renders a homepage with a Bootstrap carousel of 5 random fruit 
and related facts.

###There are 2 key modules to this project:

### 1. [src/database_updater.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/database.updater.py)

* When executed, this module reads a CSV from [src/static/data_source/fruit.csv](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/static/data_source/fruit.csv).
* The CSV contains tabular information for fruits and facts.
* This information is split between different pandas dataframes.
* The dataframes are converted to json format as per required by 
the fact and fruit models saved here: [src/models](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/models)
* They are then saved to the database.

**NOTE**: Running this should be a prerequisite to running app.py

### 2. [src/app.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/app.py)

* This module is configured to [src/config.py](https://github.com/Kremzeeq/fruit_app_project/blob/master/src/config.py)
* A FLASK_ENV variable should be exported as 'development' or 'production' e.g.  
`export FLASK_ENV=production`
* This should be prior to executing `flask run` in the command line

## Deploying web application to remote virtual machine e.g. EC2 instance



