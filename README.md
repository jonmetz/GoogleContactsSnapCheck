Introduction
==============

This utility allows you to check who on your google contacts has been affected by the recent snapchat leak, note that you will need to download the mysqldump of the leak
seperately.

Since the last two digits of each phone number in the leak have been obfuscated there will usually be incorrect matches between your contacts' phone numbers and those
in the leak, because of this, when a match is detected the program will output the full name of your Contact as well as the username of the possible match, usually it
is fairly easy to determine if a match is in fact correct.


Dependancies
==============

mysql-server

libmysqlclient-dev

python-pip

Once these packages are installed, run ```pip install -r requirements.txt``` to install the rest (note that this may require sudo)


