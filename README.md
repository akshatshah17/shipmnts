# shipmnts
Submission of Shipmnts task.<br/>

Features implemented in this minitwitter applications are below.<br/>
1 User can register/login.<br/>
2 User can see own profile.<br/>
3 User profile's has all information and tweets tweeted by him/her.<br/>
4 User can add tweets via his profile.<br/>
5 User can search other users profile via username.</br>
6 User can follow and unfollow other users.</br>
7 User can see tweets of other users sorted according to time in his/her timeline on index page.</br>
 
Tech Stacks used<br/>
1 Python<br/>
2 Django<br/>
3 HTML/CSS/Javascript's ready templates<br/>
4 Postgresql<br/>

How to run it in your own system?<br/>
1 Download all contents from this github repositary.<br/>
2 To install the requirements use below command in your local folder.<br/>
pip install -r requirements.txt<br/>
3 Download Postgresql and PGadmin in your system and create one database using pgadmin.<br/>
4 Change values of database in minitwitter/settings.py (line 77 to 81).<br/>
5 Now open command prompt and run this commands. </br>
python manage.py makemigrations</br>
python manage.py migrate</br>
6 At the end to run the application run this command.<br/>
python manage.py runserver
