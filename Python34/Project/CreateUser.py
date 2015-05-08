import random
import string
import MySQLdb
from recaptcha.client import captcha

import cherrypy

class SignUserUp(object):
	
	# send the recaptcha fields for validation
    @cherrypy.expose
    def validate(self, userkey, email, firstname, lastname, *args, **kwargs):
        # these should be here, in the real world, you'd display a nice error
        # then redirect the user to something useful
		
        '''
        if not "recaptcha_challenge_field" in kwargs:
            return "no recaptcha_challenge_field"

        if not "recaptcha_response_field" in kwargs:
            return "no recaptcha_response_field"

        recaptcha_challenge_field  = kwargs["recaptcha_challenge_field"]
        recaptcha_response_field  = kwargs["recaptcha_response_field"]

        # response is just the RecaptchaResponse container class. You'll need 
        # to check is_valid and error_code
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            "private_key_string_you_got_from_recaptcha",
            cherrypy.request.headers["Remote-Addr"],)

        if response.is_valid:
            #redirect to where ever we want to go on success
            raise cherrypy.HTTPRedirect("success_page")

        if response.error_code:
            # this tacks on the error to the redirect, so you can let the
            # user knowwhy their submission failed (not handled above,
            # but you are smart :-) )
            raise cherrypy.HTTPRedirect(
                "display_recaptcha?error=%s"%response.error_code)
        '''
		
        addToDatabase(userkey, email, firstname, lastname)
	
    @cherrypy.expose
    def addToDatabase(self, userkeyInput, emailInput, firstnameInput, lastnameInput):
        
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="ArnoldGon", # your username
                     passwd="123", # your password
                     db="test") # name of the data base
		
		# you must create a Cursor object. It will let
		# you execute all the queries you need
        cur = db.cursor() 

		# Use all the SQL you like
        cur.execute("INSERT INTO users (userKey, userEmail, userFirstName, userLastName) VALUES (%s,%s,%s,%s)", (userkeyInput, emailInput, firstnameInput, lastnameInput))
		
        db.commit()
		
        return "1";
		
    @cherrypy.expose
    def form(self):
        public = "public_key_string_you_got_from_recaptcha"
        captcha_html = captcha.displayhtml(
                           public,
                           use_ssl=False,
                           error="Something broke!")
		
        return "<h1>Create user</h1>" \
		"<form action='addToDatabase'>" \
		"User key:<br>" \
		"<input type='text' name='userkeyInput'>" \
		"<br>" \
		"Email:<br>" \
		"<input type='text' name='emailInput'>" \
		"<br>" \
		"First name:<br>" \
		"<input type='text' name='firstnameInput'>" \
		"<br>" \
		"last name:<br>" \
		"<input type='text' name='lastnameInput'>" \
		"%s <input type=submit value='Submit Captcha Text' \>" \
		"</form>" %captcha_html
	
if __name__ == '__main__':
    cherrypy.quickstart(SignUserUp())