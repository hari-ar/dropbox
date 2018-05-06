import webapp2
import jinja2
import os
from google.appengine.api import users
from model import DirectoryModel,FileModel
import time
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Data(webapp2.RequestHandler):  # Add room class handles for addition of room

    def get(self):  # Handles addition of data into ndb
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        data = 0
        print('as')
        # Checking if user is logged in
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            # Filter directories of current user.
            file_list = FileModel.query(FileModel.createdBy == user.user_id()).fetch()
            for each_file in file_list:
                blob_key = each_file.blob
                blob_info = blobstore.get(blob_key)
                data = data + blob_info.size
            print data
        else:
            main_header = 'Please Login to Access This Page..!!'  # Error message to indicate user not logged in.
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'data': data
        }

        template = JINJA_ENVIRONMENT.get_template('data.html')
        self.response.write(template.render(template_values))

