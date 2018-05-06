import webapp2
import jinja2
import os
from google.appengine.api import users
from model import DirectoryModel, FileModel
from google.appengine.ext import ndb
from google.appengine.ext import blobstore


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class RenameFile(webapp2.RequestHandler):  # Add room class handles for addition of room

    def post(self):  # Handles addition of data into ndb
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''
        # Checking if user is logged in
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            # Filter directories of current user.
            parent_directory = self.request.get("parent_directory")
            new_name = self.request.get('new_name')
            file_id = self.request.get('file_id')
            file_object = ndb.Key('FileModel', file_id).get()
            new_id = parent_directory + new_name
            file_model_new = FileModel(id=new_id)
            file_model_new.fileName = new_name
            file_model_new.fileId = new_id
            file_model_new.parentDirectory = parent_directory
            file_model_new.blob = file_object.blob
            file_model_new.createdBy = user.user_id()
            file_model_new.put()
            file_object.key.delete()
            directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == parent_directory).fetch()
            file_list = FileModel.query(FileModel.parentDirectory == parent_directory).fetch()
            current_directory_key = ndb.Key(DirectoryModel, parent_directory)
            current_directory = current_directory_key.get()

        else:
            main_header = 'Please Login to Access This Page..!!'  # Error message to indicate user not logged in.
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'directory_list': directory_list,
            'file_list': file_list,
            'error_message': error_message,
            'directory_id': current_directory.directoryId,
            'parent_directory': parent_directory,
            'upload_url': blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))