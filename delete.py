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


class DeleteDirectory(webapp2.RequestHandler):  # Add room class handles for addition of room

    def post(self):  # Handles addition of data into ndb
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        # Checking if user is logged in
        print("called")
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            # Filter directories of current user.
            parent_directory = self.request.get("parent_directory")
            user_given_name = self.request.get("directory_id")
            user_room_key = ndb.Key('DirectoryModel', user_given_name)
            current_directory_key = user_room_key.get()
            print user_given_name
            user_sub_directories = DirectoryModel.query(DirectoryModel.parentDirectory == user_given_name).fetch()
            file_list = FileModel.query(FileModel.parentDirectory == user_given_name).fetch()
            if len(file_list) > 0 or len(user_sub_directories) > 0:
                print(len(file_list))
                print(len(user_sub_directories))
                error_message = "Directory can not be deleted. Not Empty."
                print('Cant Delete')
            else:
                current_directory_key.key.delete()

            directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == parent_directory).fetch()
            file_list = FileModel.query(FileModel.parentDirectory == parent_directory).fetch()
            current_directory_key = ndb.Key(DirectoryModel, parent_directory)
            current_directory = current_directory_key.get()
            if current_directory is None:
                parent_directory = user.user_id() + '/'
            else:
                parent_directory = current_directory.parentDirectory

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


class DeleteFile(webapp2.RequestHandler):  # Add room class handles for addition of room

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

            file_id = self.request.get('file_id')
            file_object = ndb.Key('FileModel', file_id).get()
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
