import webapp2
import jinja2
import os
from google.appengine.api import users
from model import DirectoryModel,FileModel
import time


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddDirectory(webapp2.RequestHandler):  # Add room class handles for addition of room

    def post(self):  # Handles addition of data into ndb
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        directory_list = []
        file_list = []
        error_message = ""
        parent_directory = ""
        # Checking if user is logged in
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            # Filter directories of current user.
            parent_directory = self.request.get("parent_directory")
            user_given_name = self.request.get("directory_name")
            user_sub_directories = DirectoryModel.query(DirectoryModel.parentDirectory == parent_directory)
            file_list = FileModel.query(FileModel.parentDirectory == parent_directory).fetch()
            current_directory_list = user_sub_directories.filter(DirectoryModel.directoryName == user_given_name)
            directory = current_directory_list.filter(DirectoryModel.directoryName == user_given_name).fetch()
            if len(directory) == 0:
                print('Creating new Directory..!!')
                new_directory_path = parent_directory + user_given_name + '/'
                new_directory_id = new_directory_path
                root_directory = DirectoryModel(id=new_directory_id)
                root_directory.directoryId = new_directory_id
                root_directory.directoryName = user_given_name
                root_directory.directoryPath = new_directory_path
                root_directory.userCreated = user.user_id()
                root_directory.parentDirectory = parent_directory
                root_directory.put()
                directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == parent_directory).fetch()
                error_message = "New Directory Created."
            else:
                error_message = "Directory exists, select unique name."
                directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == parent_directory).fetch()

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
            'directory_id': new_directory_id,
            'parent_directory': parent_directory
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

