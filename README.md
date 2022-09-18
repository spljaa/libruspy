# Simple wrapper around Librus web page

## Goals
My aim for this project is to create python classes to deal with notifications and informations presented in Librus system.
It is used by public schools, web access is free. However notification system is rather poor.
Anf that is the place for this code. It can be scheduled to check Librus and then email new meaages or other content.

There are several started projects already. Some aim to connect to OAth and API endpoints. But that requires secret token. Which to my knowledge is not shared by software vendor. Here approach is to mimic web browser to some extent.
Librus page offers some API endpoints and gateway to access it for logged users. Code makes use of it

## Inspirations
Many thanks for [weekplot project](https://github.com/utkuufuk/weekplot) as source used in calendar plotting class


## How it works
Python class keeps a session with all cookies required to interact with Librus web page. Some of them seems to be shor-lived.
There is more complex ulr handling for Messages. As it is on separate web page. 


## Usage
It is on my list of TODO to provide examples

## Current state
As of September 2022 I see enough parts working to push it to github.
Script can login, collect messages, grades, school notices and timetable events.
There is class for storing data in sqlite3 file, and class to send an email with fresh data.

I have no plans to provide write-like actions. Thus for sending a message one needs to use web browser. 
Simple reason for that is lack of testing environment - I do not want to spam teachers (yet...)
