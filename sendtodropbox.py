#try to import dropbox, otherwise install it and import it

import os

try:
    import dropbox
except:
    os.system("pip install dropbox")
    import dropbox

from dropbox.files import WriteMode
import os

class DBXDownloader:

    def __init__(self):
        self.appKey = "appKey"
        self.appSecret = "appSecret"
        self.TOKEN = "TOKEN"
        self.filename = ""
        self.LOCALFILE = "" # file path (./temp/a.m4a)
        self.DROPBOXPATH = ""

        self.dbx = dropbox.Dropbox(self.TOKEN)
        # Check that the access token is valid
        try:
            self.dbx.users_get_current_account()
        except AuthError as err:
            sys.exit(
                "ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    # Uploads contents of LOCALFILE to Dropbox
    def upload(self, fileLocation, dbxUploadFolder="audio"):
        dbxUploadFolders = ["audio", "rss"]
        if dbxUploadFolder not in dbxUploadFolders:
            raise ValueError("Pasta de destino no Dropbox inválida. Selecione audio ou rss")
        self.LOCALFILE = fileLocation
        self.filename = os.path.split(fileLocation)[1]
        self.DROPBOXPATH = f'/{dbxUploadFolder}/{self.filename}' # Keep the forward slash before destination filename

        with open(self.LOCALFILE, 'rb') as f:
            # We use WriteMode=overwrite to make sure that the settings in the file
            # are changed on upload
            print("Uploading " + self.LOCALFILE + " to Dropbox as " + self.DROPBOXPATH + "...")
            try:
                self.dbx.files_upload(f.read(), self.DROPBOXPATH, mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()
    
    def getShareLink(self):
        link = self.dbx.sharing_create_shared_link(self.DROPBOXPATH).url
        link = link.replace("www.dropbox.com", "dl.dropboxusercontent.com")[:-5]
        return link

    def getRSS(self, rssName):
        print(os.path.join(os.getcwd(), "rss", rssName))
        try:
            localFolder = os.path.join(os.path.join(os.getcwd(), "rss", rssName))
            metadata, c = self.dbx.files_download('/rss/' + rssName)
            with open(localFolder, 'wb') as f:
                f.write(c.content)
            return True
        except:
            return False