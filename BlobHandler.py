import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from model import FileModel, DirectoryModel
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        directory_list = []
        file_list = []
        error_message = ""
        parent_directory = ""
        current_working_directory = ""



        if user:
            main_header = 'Welcome to your DropBox'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            # Filter directories of current user.
            current_working_directory = self.request.get("parent_directory")
            print(current_working_directory)
            cwd_data = ndb.Key('DirectoryModel', current_working_directory).get()
            print(cwd_data)
            parent_directory = cwd_data.parentDirectory
            upload = self.get_uploads()[0]
            blob_info = blobstore.BlobInfo(upload.key())
            file_name = blob_info.filename
            file_list = FileModel.query(FileModel.parentDirectory == current_working_directory)
            files = file_list.filter(FileModel.fileName == file_name).fetch()
            file_id = current_working_directory+file_name
            if len(files) == 0:
                print('Creating new File..!!')
                file_model_new = FileModel(id=file_id)
                file_model_new.fileName = file_name
                file_model_new.fileId = file_id
                file_model_new.parentDirectory = current_working_directory
                file_model_new.blob = upload.key()
                file_model_new.createdBy = user.user_id()
                file_model_new.put()
                directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == current_working_directory).fetch()
                file_list = FileModel.query(FileModel.parentDirectory == current_working_directory).fetch()
                error_message = "File Upload is Successful."
            else:
                error_message = "File with same name exists, please try again."
                directory_list = DirectoryModel.query(DirectoryModel.parentDirectory == current_working_directory).fetch()
                file_list = FileModel.query(FileModel.parentDirectory == current_working_directory).fetch()
        else:
            main_header = 'Please Login to Access This Page..!!'
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
            'parent_directory': parent_directory,
            'directory_id': current_working_directory,
            'upload_url': blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class FileDownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        file_id = self.request.get('file_id')
        file_id = ndb.Key('FileModel', file_id)
        data = file_id.get()
        self.send_blob(data.blob, save_as=data.fileName)
