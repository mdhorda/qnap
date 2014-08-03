import logging
import unittest
from qnap.filestation import FileStation

logging.disable(logging.CRITICAL)

host = 'usademo.myqnapcloud.com'
user = 'qnap'
password = 'qnap'

filestation = FileStation(host, user, password)

class SuccessfulLoginTestCase(unittest.TestCase):
    def runTest(self):
        self.assertIsNotNone(filestation.sid)

class FailedLoginTestCase(unittest.TestCase):
    def runTest(self):
        fs = FileStation(host, user, 'invalid_password')
        self.assertIsNone(fs.sid)

class ServerUnreachableTestCase(unittest.TestCase):
    def runTest(self):
        fs = FileStation('invalid' + host, user, password)
        self.assertIsNone(fs.sid)

class ListSharesTestCase(unittest.TestCase):
    def runTest(self):
        shares = filestation.list_share()
        self.assertTrue(len(shares) > 0)
        multimedia_shares = [x for x in shares if x['text'] == 'Multimedia']
        self.assertTrue(len(multimedia_shares) > 0)

class ListFilesTestCase(unittest.TestCase):
    def runTest(self):
        file_list = filestation.list('/Multimedia')
        self.assertIsNotNone(file_list)
        self.assertIsNotNone(file_list['datas'])
        self.assertTrue(len(file_list['datas']) > 0)

class ListFilesInInvalidFolderTestCase(unittest.TestCase):
    def runTest(self):
        file_list = filestation.list('/invalid_folder')
        self.assertIsNotNone(file_list)
        self.assertIsNotNone(file_list['success'])

class FileInfoTestCase(unittest.TestCase):
    def runTest(self):
        file_info = filestation.get_file_info('/Multimedia/Sample/picture/sample001.jpg')
        self.assertIsNotNone(file_info)
        self.assertIsNotNone(file_info['datas'])
        self.assertTrue(len(file_info['datas']) > 0)

class FileInfoForInvalidFileTestCase(unittest.TestCase):
    def runTest(self):
        file_info = filestation.get_file_info('/Multimedia/Sample/picture/invalid.jpg')
        self.assertIsNotNone(file_info)
        self.assertIsNotNone(file_info['datas'])
        self.assertTrue(len(file_info['datas']) > 0)
        self.assertTrue(file_info['datas'][0]['exist'] == 0)

class SearchTestCase(unittest.TestCase):
    def runTest(self):
        search_results = filestation.search('/Multimedia/Sample/picture', 'sample')
        self.assertIsNotNone(search_results)
        self.assertIsNotNone(search_results['datas'])
        self.assertTrue(len(search_results['datas']) > 0)

class DeleteFileTestCase(unittest.TestCase):
    def runTest(self):
        # The delete call will fail since the demo QNAP server is read-only
        delete_result = filestation.delete('/Multimedia/Sample/picture/sample001.jpg')
        print delete_result
        self.assertIsNotNone(delete_result)
        self.assertIsNotNone(delete_result['success'])

class DownloadFileTestCase(unittest.TestCase):
    def runTest(self):
        file_contents = filestation.download('/Multimedia/Sample/picture/sample001.jpg')
        self.assertIsNotNone(file_contents)
        self.assertTrue(len(file_contents) == 292568)

class UploadFileTestCase(unittest.TestCase):
    def runTest(self):
        # The upload call will fail since the demo QNAP server is read-only
        upload_result = filestation.upload('/Multimedia/Sample/picture/sample.txt', 'sample data')
        self.assertIsNotNone(upload_result)
        self.assertIsNotNone(upload_result['success'])

if __name__ == '__main__':
    unittest.main()
