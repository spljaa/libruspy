# Simple wrapper arount Librus web page

## Goals
My aim for this project is to create python classes to deal with notifications and informations presented in Librus system.
It is used by public schools, web access is free. However notification system is rather poor.
Anf that is the place for this code. It can be scheduled to check Librus and then email new meaages or other content.

There are several started projects already. Some aim to connect to OAth and API endpoints. But that requires knowledge of token. Which to my knowledge is not shared by software vendor. Here approach is to mimic web browser to some extent.
Librus page offers some API endpoints and gateway to access it for logged users. Code makes use of it

## Inspirations
Many thanks for [weekplot project](https://github.com/utkuufuk/weekplot) as source used in calendar plotting class

## Usage
It is on my list of TODO to provide examples

## Current state
As of September 2022 I see enough parts working to push it to github.
Script can login, collect messages, school notices and trmetable events.
There is class for storing data in sqlite3 file, and class to send an email with fresh data.

