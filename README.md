# Penn Labs Backend Challenge 2020 spring - Penn Clubs Review Lite

This project is structured with the standard Django project setup.

## Installation
1. run `py manage.py makemigrations pennclubslite`
2. run `py manage.py migrate`
3. run `py manage.py runserver` to start the server

You should now be able to access the server at [http://127.0.0.1:8000/].

## Populating db with club data and creating user *jen* (this should only happen once)
1. run `py manage.py shell` to enter python shell
In python shell...
2. run `from pennclubslite.scraper import store_clubs`
3. run `store_clubs()` to pull club data from Online Clubs With Penn and store them in database
4. run `from pennclubslite.models import CustomUser, Club, Category, Comment`
5. run `CustomUser(username='jen', email='jen@upenn.edu', password='jenpw', first_name='Jennifer', last_name='Jenln').save()` to create user jen

## Testing
### Model Instances
To access models from the python shell, run `from pennclubslite.models import CustomUser, Club, Category, Comment`. 
You can view the clubs stored by running `Club.objects.all()` or querying for specific clubs by club_name. You can check the existence of jen by running `CustomUser.objects.get(username='jen')`. You can also access/create model instances from the admin site, but for mysterious reasons many-to-many fields don't show up for both models on the admin site and occasionally updates made to fields aren't reflected, so it's best to directly check by querying the db.

### Accessing the admin site
1. run `py manage.py createsuperuser`
2. set the username, password, email as prompted
3. the admin site can be accessed at [http://127.0.0.1:8000/admin]

### Testing POST requests with Postman
It's assumed that POST request data will be submitted through a form. In Postman, test by sending key-value pairs 
by selecting **Body** - **form-data**. Remember to append a slash at the end of the URL. 

## Design Documentation
### Models (see `models.py`):
Using a database allows us to store large amounts of data and model the relationship between data efficiently. Clubs, users, comments and categories (tags) are all stored in the sqlite db. The fields of each model are detailed below (an id is automatically generated and hence not listed):

1. CustomUser:
    Extended Django's AbstractUser to make implementing login/logout/signup/authentication in the future. Required fields 'username', 'email', 'password', 'first_name', 'last_name'. 'username' is used as the unique identifier.

2. Club:
    - club_name: the club's name; character field of max-length 200
    - description: the description of the club; text field
    - likers: CustomUser instances who like this club; many-to-many field linking Club and CustomUsers

3. Comment:
    - club: foreign key linking to the Club that this Comment is related to
    - posted_by: the author of the comment; users have the freedom to post anonymously or leave whatever name they want
    - comment: text field containing the actual comment
    - date: date-time field recording the date of the comment

4. Category:
    club: Club instances in this category; many-to-many field linking Category and Club
    tag: the category name; character field of max-length 100

### API (see `urls.py` & `view.py`):

<table>
    <tr>
        <th>URL</th>
        <th>Http method</th>
        <th>Parameters</th>
        <th>Response upon success</th>
    </tr>
    <tr>
        <td><code>'/'</code></td>
        <td><code>'GET'</code></td>
        <td>NA</td>
        <td>Render html page</td>
    </tr>
    <tr>
        <td><code>'/api/clubs/'</code></td>
        <td><code>'GET'</code></td>
        <td>NA</td>
        <td>JSON containing club information</td> 
    </tr>
    <tr>
        <td><code>'/api/clubs'</code></td>
        <td><code>'POST'</code></td>
        <td>
            <ul>
                <li><code>club_name</code>: name of club to create/edit</li>
                <li><code>description</code>: description of club</li>
                <li><code>tag1</code><code>tag2</code><code>tag3</code>: categories the club belongs to (optional)</li>
            </ul>
        </td>
        <td>HttpRedirect to homepage</td> 
    </tr>
    <tr>
        <td><code>'/api/user/:username/'</code></td>
        <td><code>'GET'</code></td>
        <td>NA</td>
        <td>JSON containing username and registered email</td> 
    </tr>
    <tr>
        <td><code>'/api/favorite/'</code></td>
        <td><code>'POST'</code></td>
        <td>
            <ul>
                <li><code>username</code>: username of User instance favoriting this Club instance</li>
                <li><code>club_name</code>: club_name of Club instance to favorite</li>
            </ul>
        </td>
        <td>HttpRedirect to homepage</td> 
    </tr>
    <tr>
        <td><code>'/api/comment/'</code></td>
        <td><code>'POST'</code></td>
        <td>
            <ul>
                <li><code>club_name</code>: club_name of Club instance to comment on</li>
                <li><code>author</code>: author commenting (default to anonymous)</li>
                <li><code>comment</code>: comments left by user</li>
                <li><code>date</code>: date the comment was made</li>
            </ul>
        </td>
        <td>HttpRedirect to homepage</td> 
    </tr>
</table>


### Bonus:
1. Updating of existing club is allowed by modifying fields of existing club instance
2. Information is stored in database as documented above
