# MirMachine Webapp
This is a webapp built for serving an easy-to-use UI 
for the MirMachine lookup/annotation tool 
(see [MirMachine](https://github.com/sinanugur/MirMachine)) 

## Running Django
### Setting up `pipenv`
Firstly make sure you have the correct Python version installed.\
This project requires that you have Python 3.8 installed.\
You also need `pipenv` installed. This is done by using `pip install pipenv`. 

To install the project simply run `pipenv install` in the root folder.\
Then run `pipenv shell` to spawn the virtual environment.\
Now you are ready to start Django.\
P.S. if you want to exit the environment type `exit`

### Running the Django server
In the virtual environment you can run the following:
#### `python manage.py migrate` 
Run this script in the root folder of the project.\
This refreshes Django with potential changes that may be present in the backend.
This should be done after the initial download, and after there are changes made
in the backend.
#### `python manage.py runserver`
Use this script to run the server.\
Make sure you build the frontend before running the server.


## Building the frontend 
Navigate to `lookupService/frontend`
before using the following scripts.\
If you require hot reloading we recommend using a separate 
shell to build the frontend. 

### `npm run dev`
Runs the app in the development mode.\
Enables hot reloading, making it the best choice when making changes to the frontend.\
Run the Django server and open [http://localhost:8000](http://localhost:8000) to view it in the browser.

The page will update if you make edits. Simply reload to display changes. 

### `npm run build`
Builds the app for production to the `lookupService/static/frontend` folder.\
Webpack bundles the project and optimizes it for production.



