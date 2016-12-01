# URLShortener
URLShortener

URL Shortening enables a user to get a shorter URL for any URL. This way he can easily share it on twitter and with his friends.
The main advantage is the characters saved and the ease of convenience due to the shorter URL. With more and more mobile
devices being used, Shorter URL are preferred as they are easy to share. Another use of URL Shortening is the analysis 
provided by it. This way user can track how many visitors used his URL.

I have implemented URL Shortening by converting the Id (Integer, Primary key) of WebUrl Table to Base 62. I am converting to
Base 62 because I can use 62 characters in the shortened URL and they are a-z, A-Z, 0-9. I have also taken care of not 
generating swear words. Analysis is also showsn for each URL. The user also has the option of deleting URL if he wants to. I have also
implemented Pagination where user can select the page size and his records are displayed in paginated manner.

**Links**

Working Link: <http://52.15.140.132:5000/home>

Databse Schema: <https://drive.google.com/open?id=0B0s1azkCovAAVFVqR0xDUU9NYmc>

**Technologies used:**
 1. Python
 2. Flask
 3. SqlAlchemy
 4. AWS
