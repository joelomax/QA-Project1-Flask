# start.sh

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py

export FLASK_ENV=development

export SQLALCHEMY_DATABASE_URI=mysql+pymysql://songbox:songbox@localhost/songbox_db
#export SQLALCHEMY_DATABASE_URI=sqlite:////home/joelomax/flasktutorial/database/songbox.db
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export SECRET_KEY=sldlknlgaowiur09q08308


flask run --host=0.0.0.0 --port=5000
