# Distinctiveness and Complexity
I have named my capstone project as Mathango (_**Math**_ + _Dj**ango**_) because it is based on a Mathematic (arithmetic) game and Django is this project's Backend Backbone. 
Mathango is a small website-based game where during a gaming session a player has to answer as many possible simple arithmetic calculations correctly and accurately within a stipulated time which they can select at the beginning.
Right and exact answers are only accepted, otherwise the players have to answer again. Questions involve addition and substraction of 1-3 digit numbers, and multiplication and addition of 3 digit numbers by 1 digit numbers. 
Blank answers are regarded as incorrect. Each users have their own statistics of games played, total questions they have answered correctly,
and their average response time which is the average time taken by the user to answer one question **correctly**. 
There is a leaderboard tab which on opening shows the list of all users ranked on the basis of their statistics. 
New users who haven't answered a single question correctly are not ranked. Each User's are allocated a separate User profile which they can view on aa webpage.
Users have the ability to post some messages which only them and their followers can see. 
Similarly Users can follow other users and hence have followers.
This social feature is just a tiny portion of the complete Capstone Project.


Evidently this type of math game has not been included in any projects in the CS50W course. Although chances are almost negligible but if any other person's any project have any type of resemblence with the central idea of my 
project, the project as whole will definitely be different as I have included several new and exclusive Bootstrap CSS features for enhancing the User interface and aesthetics which, therefore, will be hugely different from any other project (if any exists).
And such a resemblence shall be purely coincidental.

The project as a whole is absolutely and definitely different from any other projects or assignments which we have / have been done in the CS50W Course. 

_Features which constitute the website and make it stand out in complexity are discussed_ :

## Mathangoapp
Mathangoapp is the single Django application in the Mathango Django project, where the entire functionality of the website is based. The back end utilises Python Programming using Django Libraries. The front end utilises HTML for the overall structure of the webpage, CSS for the aesthetics, Django templates for server-client functionality and Javascript for server-client communication, aesthetics as well as other essential functionality.

## Layout and Mobile Responsiveness
Each webpage has the same characteristic header and footer. The header is a navigation bar with many link tabs. There is a search bar where user can search other users by their username and view their profile. Mathango Logo is present on the extreme left which on clicking redirects the user to the home page. Users who haven't signed in or registered will see two tabs : ```Log in```, ```Register```. Log in webpage is opened on clicking the ```Log in``` tab and the user can register by entering his name, email and password under the ```Register``` tab. Users who have signed in will see four tabs : ```Profile``` (with a profile icon), ```Play```, ```Leaderboard``` and ```Log out```. The ```log out``` tab logs out the user and redirects him to log in webpage. The ```Play``` tab does the task of redirecting the user to the home page. The ```Leaderboard``` tab opens the leaderboard. Each webpage have a characteristic footnote containing a link to mine(the creator's) email address which preserves it's identity. The main content of the webpages are contained in a division which is between the header and footer. The division is named ```main``` which takes up the entire width of the window. The header, footer, ```main``` and the contents inside ```main``` are extremely mobile responsive such that everything fits into the screen quite well. When the screen width turns into that of a standard mobile, the header turnes into a collapsable navigation tab with the same links. Clicking on the three striped button opens the drops the navbar with all the tab links, and again clicking on it collapses it back.

## Models
5 Django Models have been utilised throughout the application.
- ### User
  Inherits the AbstractUser Model
- ### UserStats
  Is used for storing the user statistics for each user. Fields : user (Foreign - User), total_right, avg_response_time. 
- ### Game
 Is used for storing the information about each game played by users. Fields : player (Foreign - User), right, totalresponsetime, avgresponsetime.
- ### Follow
 Is used for establishing user to user follow relations defining how an user follows other users. Fields : user (Foreign - user), following (Foreign - User)
- ### Message
 Is used for storing a table of messages written by various users on the site. Fields : creator (Foreign - User), content, date

## Index page
url : ```/index```

This is the homepage of Mathango website. 
Some rules are posted on the top, then there are some preset game-times and then there is a custom game-time setting.

## Game page
url : ```/game?time=<time selected by user in index page>```

This is the main game page of the website. On selecting a game time from the ```index``` page, the user is redirected to the game page where he plays the mathango game. The game page has a simple interface but a very complicated underlying Javascript code which communicates continuously with the server. Such a communication ensures security from cheaters and correct assessment of answers and validation of scores. A blue border surrounds the game controls in the screen. This border turns green on starting the game, turns red on answering a question incorrectly, and turns green again on correcting the answer. The border turns blue again if the game is stopped or paused. The data entry point is the number type input area which takes only number and is autofocussed when the game is started or resumed. 
The game is started by clicking the ```start``` button. A timer starts at right which countdowns from through the time selected before by the user. Then the questions are loaded one by one on answering each. The next question is loaded on pressing ```Enter``` key or clicking the ```>>``` button. A numpad appears on the bottom which can be used by mobile users for efficient typing. The ```Pause``` button is used for pausing the timer as well as the game. Players cannot enter anything into the input during pause time. Then the ```Resume``` button resumes the timer and the game. Players are allowed to answer till the timer turns red and stops on time exhaustion. The game data is saved on ending a game. Game can be played again using the ```Restart``` button. The ```X``` button take players back to index page. The game page is the most complex portion of the entire logic of the application. 

## Leaderboard page
url : ```/leaderboard?page=<pagenumber>&type=<1 or 2>```

This is the leaderboard page. Players are either ranked using the total right answers (highest to lowest) or the average response time per question (lowest to highest). The first three players who top the category of ranking are highlighted as gold, silver and bronze medalist. Ranking system can be changed using the two green buttons: ```average response time``` and ```total right answers```. The page is accessed by a get request. ```page``` parameters requests the required page number and the ```type``` parameter requests the required ranking list.

## Profile page 
url : ```/profiles/<username of user whose profile has been requested>?page=<page_number1>&page2=<page_number2>```

This is the user profile page. This has two purposes. One is for the user to view his own profile. Another is for the user to view profiles of other users. User's Statistics are shown on the page, along with the number of followers and number of players he/she follows. Messages posted by native user is show on his profile under ```Your posts``` and messages posted by players who he/she follows in shown under ```Posts from users whom you follow```. Also if the user requests his own page, a ```post your message``` form allows him/her to enter the content of a message and post it using the ```post``` button. If another user's profile is viewed, his posts are shown only if the requesting user follows the user whose profile had been requested. ```Follow``` button makes the requesting user follow the requested user. ```Unfollow``` button makes the requesting user unfollow the requested user.

## Login, Register, Log out pages
url : ```/login, /register, /logout```

Used for logging user in, new user registration/account creation and logging user out, respectively. Has standard CSS Aesthetics.


# File Structure

## ```mathango```     : default app 
 - ```__pycache__```  : cache of executable files 
 - ```__init__.py```  : used to mark directories on disk as Python package directories.
 - ```asgi.py```      : **A**synchronous **S**erver **G**ateway **I**nterface file 
 - ```settings.py```  :  Django settings file contains all the configuration of Mathango Django Project
 - ```urls.py```      : Used for listing url routes to function based views, class based views and including another URLconf using the include function
 - ```wsgi.py```      : Django's primary deployment platform
## ```mathangoapp```  : Mathango App 
 - ```__pycache__```  : cache of all executable files
 - ```migrations```   : migration files
 - ```static/mathangoapp``` : containing static files to be included in memory while execution
   - ```script.js```        : javascript file containing some functionality
   - ```styles.css```       : CSS file containing the entire code for controlling the aesthetics and making the webpages mobile responsive
 - ```templates/mathangoapp``` : contains all the template files to be rendered 
   - ```game.html```           : contains the HTML and Javascript for the mathango game page.
   - ```index.html```          : contains the HTML and Javascript for the mathango home page.
   - ```invalid.html```        : contains the HTML and Javascript for displaying ```Invalid request``` page
   - ```layout.html```         : contains the HTML and Javascript for standardizing the layout of all the webpages of the website
   - ```leaderboard.html```    : contains the HTML and Javascript for the mathango ```leaderboard``` page.
   - ```login.html```          : contains the HTML and Javascript for the mathango ```login``` page.
   - ```profile.html```        : contains the HTML and Javascript for the mathango ```profile``` page.
   - ```register.html```       : contains the HTML and Javascript for the mathango ```register``` page.
 - ```__init.py__```   : used to mark directories on disk as Python package directories.
 - ```admin.py```      : used to register the models defined in models.py for the admin page. 
 - ```apps.py```       : allows Django to load apps automatically when ```INSTALLED_APPS``` contains the path to an application module rather than the path to a configuration class.
 - ```models.py```     : defines all the Django models 
 - ```tests.py```      : a test framework with a small hierarchy of classes that build on the Python standard unittest library.
 - ```urls.py```       : defines the ```urlpatterns``` list which related individual urls to their respective view functions.
 - ```views.py```      : contains all the view functions for each defined url which handles requests and returns ```HTTPResponses``` or renders webpages.

## ```manage.py```     : primary tool for executing Django-specific tasks.



# How to run Mathango Application

1> Check whether Django is installed (use ```pip install django``` on cmd for installing django)

2> Navigate to the directory which contains all the three files : mathango, mathangoapp, and manage.py. 

3> Run the commands on for creating a new database : 
```
python manage.py makemigrations mathangoapp

python manage.py migrate
```
4> For running the local host server execute :

```python manage.py runserver```

5> The server starts running and will be accessible at the local server address provided in the command prompt as :

 ```Starting development server at <local server address>```
 
6> On entering the url address on web browser and browsing it shows the Mathango website.
