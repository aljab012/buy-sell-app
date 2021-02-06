## tutorial

## create
// python3 -m venv env
virtualenv --no-site-packages env
## Activate:  
source env/bin/activate

## Install a package:   
pip3 install ........ 

## Install from requirements.txt:   
pip3 install -r requirements.txt
// pip3 install Flask-Login
// pip3 install Flask-Bootstrap
// pip3 install visitor


## run the project

export FLASK_APP=project    
export FLASK_DEBUG=1  
export FLASK_ENV=development  
flask run 
