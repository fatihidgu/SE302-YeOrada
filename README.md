Running the Application

Clone the repository
$ git clone https://github.com/ro6ley/plaindjango.git

Check into the cloned repository
$ cd plaindjango

Setup the virtual environment and start it as follows:
$ virtualenv --python=python3 env --no-site-packages
$ source env/bin/activate

Install the requirements
$ pip install -r requirements.txt

Start the Django API
$ python manage.py runserver
