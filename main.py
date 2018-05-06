#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# !/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from add import AddDirectory
import jinja2
from google.appengine.ext import blobstore
import os
from delete import DeleteDirectory, DeleteFile
from BlobHandler import FileUploadHandler, FileDownloadHandler
from Rename import RenameFile
from model import DirectoryModel, FileModel
from data import Data

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        directory_list = []
        file_list = []
        error_message = ""
        current_id = ""

        # Checking if user is logged in
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            current_id = user.user_id() + '/'
            # Filter directories of current user.
            if len(DirectoryModel.query().fetch()) == 0:
                print('Directory list is empty, create root for the user..!!')
                root_directory = DirectoryModel(id=current_id)
                root_directory.directoryId = current_id
                root_directory.directoryName = '/'
                root_directory.directoryPath = "/"
                root_directory.userCreated = user.user_id()
                root_directory.put()
            directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == current_id).fetch()
            file_list = FileModel.query(FileModel.parentDirectory == current_id).fetch()
            print(file_list)

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
            'parent_directory': current_id,
            'directory_id': current_id,
            'upload_url': blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        directory_list = []
        file_list = []
        error_message = ""
        is_root = True
        directory_id = self.request.get("directory_id")
        parent_directory = user.user_id()+'/'
        print(directory_id)
        # Checking if user is logged in
        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            current_id = user.user_id() + '/'
            if len(DirectoryModel.query().fetch()) == 0:
                print('Directory list is empty, create root for the user..!!')
                root_directory = DirectoryModel(id=current_id)
                root_directory.directoryId = current_id
                root_directory.directoryName = '/'
                root_directory.directoryPath = "/"
                root_directory.userCreated = user.user_id()
                root_directory.put()
            # Filter directories of current user.
            directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == directory_id).fetch()
            file_list = FileModel.query(FileModel.parentDirectory == directory_id).fetch()
            print("Getting data for "+directory_id)
            current_directory_key = ndb.Key(DirectoryModel, directory_id)
            current_directory = current_directory_key.get()
            if current_directory is None:
                parent_directory = user.user_id()+'/'
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
            'directory_id': directory_id,
            'parent_directory': parent_directory,
            'upload_url': blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addDirectory', AddDirectory),
    ('/deleteDirectory', DeleteDirectory),
    ('/upload', FileUploadHandler),
    ('/download', FileDownloadHandler),
    ('/deleteFile', DeleteFile),
    ('/renameFile', RenameFile),
    ('/data', Data)
], debug=True)
