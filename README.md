# Parrot Sample
* This project is developed on `Python Flask` and is used to support sampling, demonstration of interface automation/traffic playback tools.
* Currently only basic HTTP operations are provided, data is stored in running memory, will be reset after restarting the service.
* Your issues and participates in the construction are welcome.

## User Handbook
### Step 0: Basic environment preparation
* This project is based on python 2.7.x or 3.x. Please make sure that `python` and `pip` are installed on the machine running this service. Recommended version: 3.7.x
* The dependent modules have been written in requirements.txt and can be installed using `pip install -r requirements.txt`

### Step 1: Boot the application
* This project uses port 8080 by default. If there is a conflict, you can modify `_PORT_` in `app.py`.
* Start the application in command line mode: `python app.py`, if you need to debug, add `debug=True` parameter to app.run.
* If it starts normally, the screen will display "Running on http://0.0.0.0:8080/" content output, WARNING can be ignored.
* If it does not start normally, please confirm Step 0 and port usage. If you have any questions, please feedback Issue.

### Step 2: Visit the application
* The server ip can be obtained by `ipconfig` or `ifconfig` command, and then spliced ​​into a complete address, such as: `10.100.100.10:8080`, 127.0.0.1 is not recommended.
* The above address can be directly accessed in the browser window. If it is normal, the page function module will be presented.
* This site is not compatible with mobile styles, and the mobile display is not effective.
* If the access is abnormal, please make sure that the application of Step 1 is running normally, and then there is a problem to feedback Issue.

### What the application supports now
* Basic HTTP GET/POST requests. Except for the index page, the interface response text is in json format, including `timestamp` and random `tag`.
* Random exception rate, longest and shortest random time-consuming ranges, can be edited online.

#### User's Behavior
* Register: `POST` method
* Unregister: `POST` method, `token` is added in `headers`
* Logon: `POST` method, `token` would be generated and set in response `headers` and `cookies`
* Logout: `POST` method, `token` is added in `headers`, `cookies` would be cleared

#### User's Hobbies
* Hobby List: `GET` method, `token` is added in `headers`
* Hobby Detail：`GET` method, `token` is added in `headers`, and `name` parameter should be obtained from response of `Hobby List`
* Add a Hobby: `POST` method, `token` is added in `headers`
* Remove a Hobby: `POST` method, `token` is added in `headers`
* Random Suggestion: `GET` method, `token` is added in `headers`, and a `today()` parameter is added

#### Suggested demo operations
* Logon => Hobby List => Add a Hobby => Hobby List => Hobby Detail => Random Suggestion => Logout
* You can view the corresponding interface call details in the developer tool of the browser, or you can export the HAR file.
