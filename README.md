About
=====

This is a demonstration project how to get started with OAuth 2.0 for QlikView and Qlik Sense integration. After setup users will be able to authenticate using their Google account. The example uses Google's OAuth 2.0 library available for both C# and Python, although the example is based on Python the code should be quite self-explaining and the workflow would more or less be the same for C#.

Note
----

* OAuth 2.0 should only be implemented using SSL/TLS only!
* Proper certificates needs to be used and converted to .pem format and copied to the same directory as the script.

Installation
------------

* Download and install [Python 2.x](https://www.python.org/) (NOT compatible with 3.x due to the Google library dependencies)

* To install or upgrade pip, securely download [git-pip.py](https://bootstrap.pypa.io/get-pip.py). Then run the following (which may require administrator access):

```sh
python get-pip.py
```

* After pip is installed run the following command:

```sh
pip install https://github.com/braathen/qlikoauth/zipball/master
```

The required dependencies and the project itself should now be downloaded and installed to C:\Qlik\ on Windows and we can continue with the configuration!

Configuration
-------------

The client_secrets.json file needs to be updated with your own CLIENT_ID, CLIENT_SECRET and proper redirect uri. For testing purposes it's ok to keep the defauilt uri as it is.

```json
{
  "web": {
    "client_id": "YOUR_OWN_CLIENT_ID",
    "client_secret": "YOUR_OWN_CLIENT_SECRET",
    "redirect_uris": ["https://qlikgoogle.localtest.me:1443"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```

In the C:\Qlik\qlikoauth\qlikoauth.py file there are some things to consider and maybe adjust to your own liking or setup. Make sure to set the redirect_uri properly here as well.

```python
flow = flow_from_clientsecrets('client_secrets.json',
                               scope='https://www.googleapis.com/auth/userinfo.email',
                               redirect_uri='https://qlikgoogle.localtest.me:1443')
```

This line checks the domain of the authenticated user. Note: If you don't have your own domain and take some precaution it means that every Google user on the planet will be able to authenticate against your QlikView/Sense server. It might be a good idea to prevent this, even though you can of course determine who can see what from a QlikView/Sense perspective.

```python
if not userid.endswith('@gmail.com'):
```

The below line points to the QlikView Server, make sure it's correct. In this case it defaults to localhost, but it does not necessarily need to be on the same machine.

```python
r = requests.post('http://localhost/QvAJAXZfc/GetWebTicket.aspx', data=xml)
```

Same thing with this line...

```python
return 'http://localhost/QvAJAXZfc/Authenticate.aspx?type=html&webticket=%s&try=%s&back=%s' % (xmldoc[0].text, '/QlikView/', '')
```

And that's all there is to it! The only thing left to do is to setup QlikView Server to respond to webticket requests from the machine running this code. I recommend using IP whitelists.

Running
-------

Open a terminal window, change to the installed directory and give the following command:

```sh
python qlikoauth.py
```

This launches a webserver on the port 1443 (you can change this in the code). In QlikView and Qlik Sense, set this url as custom authentication URL.

License
-------

This software is made available "AS IS" without warranty of any kind under The Mit License (MIT). QlikTech support agreement does not cover support for this software.

Meta
----

* Code: `git clone git://github.com/braathen/qlikoauth.git`
* Home: <https://github.com/braathen/qlikoauth>
* Bugs: <https://github.com/braathen/qlikoauth/issues>
