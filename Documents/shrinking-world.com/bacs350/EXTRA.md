EXTRA.md


 


Follow this recipe to create a photo gallery app with list and details views.


### Step 1 - Add Images to List View

Start with the Gallery Project you just built

Modify view code to show all images in directory

    from pathlib import Path
    photos = Path('static/images').iterdir()

Change Template to use name of images from directory listing

templates/photos.html

    <h1>Photo Gallery</h1>
   
    {% for photo in photos %}
        <img src="{{ photo }}" alt="Chapter {{ photo }}">
    {% endfor %}


### Step 2 - Create a Detail View  

templates/photos.html

    <p>
        <img src="{{ photo.file }}" alt="Chapter {{ photo.id }}">
    </p>
    <p>
        FILE PATH: {{ photo.caption }}
    </p>

photos/views.py

    def photo_details(i, filename):
        return dict(id=i, file=f, caption=f)


Data for view

    {
        'id': "4",
        'file': "static/images/chapter-4.jpg",
        'caption': "Caption for Chapter 4",
    }

photos/views.py

    class PhotoDetailView(TemplateView):
        template_name = 'photo.html'

        def get_context_data(self, **kwargs):
            i = kwargs['id']
            filename = 'static/images/chapter-4.jpg'
            return photo_details(i, filename)


### Step 3 - Configure URL Route
   
urls.py

    from django.urls import path
    from photos.views import PhotosView
    
    urlpatterns = [
        path('', PhotosView.as_view()),
    ]
 
sample URLs

    http://localhost:8000/4


### Step 4 - Improve View Code

#### For loop in Template

templates/photos.html

    {% for photo in photos %}
        <img src="{{ photo.file }}" alt="Chapter {{ photo.id }}" width="200">
    {% endfor %}


#### If statement in Template

templates/photos.html

    {% if photo.caption %}
        {{ photo.caption }}
    {% else %}
        No caption
    {% endif%}


#### List the Directory as Dictionary

List the images in the directory and create a dictionary for the view.

photos/views.py

    def photo_list():
        photos = Path('static/images').iterdir()
        photos = [photo_details(i, f) for i, f in enumerate(photos)]
        return photos


#### Add Links for Details

templates/photos.html

    {% for photo in photos %}
        <a href="{{ photo.id }}">
            <img src="{{ photo.file }}">
        </a>
    {% endfor %}


### Step 5 - Test/Commit/Push

Test Locally

    $ python manage.py runserver

Browse to web page at http://localhost:8000

Commit changes to Git

    $ git add .
    $ git commit -m 'Create Photos app' 
    $ git push


### Step 6 - Digital Ocean Server

Prep for App Platform

runtime.txt

    python-3.10.4

requirements.txt

    Django
    gunicorn
    psycopg2-binary

Run Command

    python manage.py migrate --no-input
    cd week3/Gallery
    gunicorn --worker-tmp-dir /dev/shm config.wsgi
    
Browse to web page





### Step 6 - Digital Ocean Server
    
Prep for App Platform by creating files to specify the Python and package versions
to use.
Edit your App Platform config to try out this new code.

runtime.txt

    python-3.10.4

requirements.txt

    Django
    gunicorn

Run Command

    python manage.py migrate --no-input
    gunicorn --worker-tmp-dir /dev/shm config.wsgi
    
Once you have created your initial web app at Digital Ocean you can upload a new 
**app.yaml** file to replace the existing one. This will change all of the App
Platform settings at once.
 
Go to the Digital Ocean App Platform page. Select App Settings and upload the **app.yaml**
to App Platform.

Wait while it is built (this may take 10-15 minutes)

Here is a configuration that you can use as a starting point for your deployment.
Be sure and customize this file to point to your source code.

config/app.yaml

    envs:
    - key: DEBUG
      scope: RUN_AND_BUILD_TIME
      value: "True"
    - key: DISABLE_COLLECTSTATIC
      scope: RUN_AND_BUILD_TIME
      value: "1"
    name: bacs350-demo
    region: nyc
    services:
    - environment_slug: python
      github:
        branch: main
        deploy_on_push: true
        repo: Mark-Seaman/PythonWebApps
      http_port: 8080
      instance_count: 1
      instance_size_slug: basic-xxs
      name: bacs350-demo-app
      routes:
      - path: /
      run_command: |
        python manage.py migrate --no-input
        gunicorn --worker-tmp-dir /dev/shm config.wsgi
      source_dir: Photos
    static_sites:
    - environment_slug: html
      github:
        branch: main
        deploy_on_push: true
        repo: Mark-Seaman/PythonWebApps
      name: bacs350-demo-static
      routes:
      - path: /static
      source_dir: Photos/static

After setting a new **app.yaml** an automatic build and deploy will be done on App Platform.
If it is successful you will have a running server. If it is not successful then the code will 
be automatically rolled back to the last good version of code that was properly deployed.
This ensures that if you push bad code your customers will see the older version that was working.


### Step 7 - Test Your Server

Browse to web page at the default route of your server. This will be at a URL that Digital
Ocean assigned to you.  You can also configure a custom URL if you have a registered domain
name to point at your application.

Browse to the web page at the top of your domain.  For example, 

    https://hammerhead-app-i8swz.ondigitalocean.app/

This will load the default URL at your website. You should always define this URL to do 
something useful for your users. Additional URLs may point to other pages.

    https://hammerhead-app-i8swz.ondigitalocean.app/hulk




### Step 5 - Digital Ocean Server
    
Once you have created your initial web app at Digital Ocean you can upload a new 
**app.yaml** file to replace the existing one. This will change all of the App
Platform settings at once.

Here is a configuration that you can use as a starting point for your deployment.
Be sure and customize this file to point to your source code.

After setting a new **app.yaml** an automatic build and deploy will be done on App Platform.
If it is successful you will have a running server. If it is not successful then the code will 
be automatically rolled back to the last good version of code that was properly deployed.
This ensures that if you push bad code your customers will see the older version that was working.



### Step 6 - Test Your Server

Browse to the web page at the default route of your server. This will be at an URL that Digital
Ocean assigned to you. You can also configure a custom URL if you have a registered domain
name to point at your application.

Browse to the web page at the top of your domain. For example, 

    https://hammerhead-app-i8swz.ondigitalocean.app/

This will load the default URL at your website. You should always define this URL to do 
something useful for your users. Additional URLs may point to other pages.

    https://hammerhead-app-i8swz.ondigitalocean.app/hulk


