import os
import zipfile
import requests
from config import link_webdriver, FolderProject

class ParseWebDriver:
    """
    class which is dedicated to work with selenium and install selenium manually
    """
    def __init__(self) -> None:
        self.name_archive = link_webdriver.split('/')[-1]
        self.path, self.path_webdriver, \
            self.path_archive  = self.get_path_driver()
        self.presence_driver, \
            self.presence_archive = self.check_driver_presence()

    def get_path_driver(self) -> set:
        """
        Method which is dedicated to produce the returnla of the values of the driver
        Input:  value which is required ro be used
        Output: we created our link to the webdriver for it
        """
        value_path = os.path.join(FolderProject.folder_current, 
                                FolderProject.folder_storage) 
        return value_path, os.path.join(value_path, 'chromedriver'), \
                os.path.join(value_path, self.name_archive)

    def check_driver_presence(self) -> set:
        """
        Method which is dedicated to check drivers presence of the values
        Input:  None
        Output: boolean value which is required to be used
        """
        os.path.exists(self.path) or os.mkdir(self.path)
        return (os.path.exists(os.path.join(self.path_webdriver, 'chromedriver')) and \
                os.path.isfile(os.path.join(self.path_webdriver, 'chromedriver')) or \
                os.path.exists(self.path_webdriver) and os.path.isfile(self.path_webdriver)), \
                os.path.exists(self.path_archive) and os.path.isfile(self.path_archive)

    def produce_webdriver_values(self) -> None:
        """
        Method which is dedicated to produce webdriver for the selenium
        Input:  None
        Output: we created and unarchived values
        """
        if self.presence_driver:
            return os.path.join(self.path_webdriver, 'chromedriver')
        elif not self.presence_driver and self.presence_archive:
            self.produce_further_transformations()
        else:
            archive_value = requests.get(link_webdriver, stream=True)
            with open(self.path_archive, 'wb') as archive_new:
                archive_new.write(archive_value.content)
            self.produce_further_transformations()
        return os.path.join(self.path_webdriver, 'chromedriver')

    def produce_further_transformations(self) -> None:
        """
        Method which is dedicated to produce values out of the archive
        Input:  path of the result
        Output: we created values of the 
        """
        try:
            with zipfile.ZipFile(self.path_archive) as myzip:
                if 'chromedriver' in myzip.namelist():
                    myzip.extract('chromedriver', self.path_webdriver)
                    os.chmod(os.path.join(self.path_webdriver, 'chromedriver'), 755)
        except Exception as e:
            #TODO add here logger
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        finally:
            os.remove(self.path_archive)
