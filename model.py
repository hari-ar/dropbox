from google.appengine.ext import ndb


class FileModel(ndb.Model):
    fileName = ndb.StringProperty()
    fileId = ndb.StringProperty()
    parentDirectory = ndb.StringProperty()
    blob = ndb.BlobKeyProperty()
    createdBy = ndb.StringProperty()
    permissionGranted = ndb.StringProperty(repeated=True)


class DirectoryModel(ndb.Model):
    directoryId = ndb.StringProperty()
    parentDirectory = ndb.StringProperty()
    directoryName = ndb.StringProperty()
    directoryPath = ndb.StringProperty()
    userCreated = ndb.StringProperty()


