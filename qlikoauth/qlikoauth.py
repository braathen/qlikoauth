"""
Qlik OAuth 2.0 Authentication

Custom authentication for QlikView/Qlik Sense using OAuth 2.0 (Google)

NOTE:
OAuth v2.0 should by design always be implemented using SSL/TLS only!
"""

import cherrypy
import requests
from oauth2client.client import flow_from_clientsecrets
import xml.etree.cElementTree as ET

class GoogleAuth:
    @cherrypy.expose
    def index(self, code=None):
        flow = flow_from_clientsecrets('client_secrets.json',
                                       scope='https://www.googleapis.com/auth/userinfo.email',
                                       redirect_uri='https://localhost:1443')

        if code is None:
            auth_uri = flow.step1_get_authorize_url()
            raise cherrypy.HTTPRedirect(auth_uri)
        else:
            credentials = flow.step2_exchange(code)
            if credentials is None or credentials.invalid:
                return "Invalid credentials"

            userid = credentials.id_token['email']

            if not userid.endswith('@gmail.com'):
	        	return "Unknown email address"

            response = self.qlikview(userid)
            #response = self.sense(userid)

            if not response.startswith('http'):
                return response

            raise cherrypy.HTTPRedirect(response)

    def qlikview(self, userid):
        xml = '<Global method="GetWebTicket"><UserId>%s</UserId></Global>' % (userid)
        r = requests.post('http://localhost/QvAJAXZfc/GetWebTicket.aspx', data=xml)

        if r.text is None or 'Invalid call' in r.text:
            return 'Invalid call'

        xmldoc = ET.fromstring(r.text)

        return 'http://localhost/QvAJAXZfc/Authenticate.aspx?type=html&webticket=%s&try=%s&back=%s' % (xmldoc[0].text, '/QlikView/', '')

    def sense(self, userid):
        return "http://www.qlik.com/"

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"
    if (cherrypy.server.ssl_certificate != None and cherrypy.server.ssl_private_key != None):
         headers['Strict-Transport-Security'] = 'max-age=31536000'  # one year

if __name__ == '__main__':
    server_config={
        'server.socket_host':'0.0.0.0',
        'server.socket_port':1443,
        'server.ssl_module':'builtin',
        'server.ssl_certificate':'cert.pem',
        'server.ssl_private_key':'privkey.pem',
        'tools.secureheaders.on':True,
        'tools.sessions.on':True,
        'tools.sessions.secure':True,
        'tools.sessions.httponly':True
    }
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)
    cherrypy.config.update(server_config)
    cherrypy.quickstart(GoogleAuth())
