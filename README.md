Installing
----------

First, install Python (any version less than 3 should work, but you can go with 2.6 to be super safe).

Then, install [setuptools](http://pypi.python.org/pypi/setuptools) (`sudo apt-get install python-setuptools` on debian-ish systems). Setuptools gives you the command line program easy_install, which is a Python package manager.

However, you want the newer and cooler package system, so run `easy_install pip` and never use easy_install again. On Windows, easy_install might not get put on your PATH, in which case it should be somewhere like C:\Python*xx*\Tools\Scripts. I recommend adding that whole directory to your system PATH.

Here's why you wanted pip, the cool new package manager. Now, just get in the csc450-website/ directory and run `pip install -r requirements.txt`. I made that requirements file, and it should go ahead and install all the Python packages needed for this project (Django, etc.). If, later on, you pull updates and something breaks, there's a good chance there's a new dependency present, so just run that last command again (for this project, there probably won't be any more dependencies unless I want to get clever).

In the main project directory, there's a manage.py script. That's Django's utility for doing crap. There's a couple of one-time-only things to run here (Windows users omit the dot-slash):

    ./manage.py syncdb

 This creates tables in SQL. In settings.py I have it just using an SQLite database that gets created in the project folder. If needed, we can change that later to any of Django's supported databases. This command will ask you to create a local superuser. You might as well do that; it's just a dummy account to use locally so feel free to do user:admin password:password. You can add more later with `./manage.py createsuperuser`.

 At the end of the output for the above command it will say that our project isn't synced and to use migrations instead. To do this, run:

     ./manage.py migrate cars

 That will *actually* create the rest of our tables. In the future, I will probably make commits with messages starting with "(MIGRATION)". Every time I do that, it means I modified the database scema, so you'll have to run the above command again.

 Now you should be ready to run the local dev server:

     ./manage.py runserver

 It will start running [on port 8000](http://127.0.0.1:8000/). Go to it in your browser and log in with your superuser account, or register a new account. You can add cars, blah-dee-blah.

Basics
------

 The main folder is what's called the Django project. It's mostly just settings. Our actual application is in the cars/ folder. You'll spend most your time in this directory.

 Templates are under the templates/ directory. They are basically HTML, but the stuff between `{% %}` and `{{ }}` is Django template code, which Django will process and replace with text or actual HTML code. The main template is base.html. It's the only one that contains the actual opening and closing html and body tags. I like to keep everything neatly indented so hopefully it's easy to read. Near the bottom you'll see this:

    {% block content-area %}
    {% endblock %}

All the other templates will *extend* base.html, which means that everything contained within them will get put inside that block. Think of it like a Java ClassB extending ClassA and overriding one of ClassA's methods.

All the static media (CSS, images, and JavaScript) is in the site_media/ directory in the root directory of our project. In base.html I've already imported a cars.css and cars.js file, so feel free to mess with those if needed.

**That's all I've got for now.**