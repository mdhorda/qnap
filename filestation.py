import os

from qnap import Qnap

class FileStation(Qnap):
    """
    Access QNAP FileStation.
    """

    def list_share(self):
        """
        List all shared folders.
        """
        return self.req(self.endpoint(
            func='get_tree',
            params={
                'is_iso': 0,
                'node': 'share_root',
            }
        ))

    def list(self, path, limit=10000):
        """
        List files in a folder.
        """
        return self.req(self.endpoint(
            func='get_list',
            params={
                'is_iso': 0,
                'limit': limit,
                'path': path
            }
        ))

    def get_file_info(self, path):
        """
        Get file information.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='stat',
            params={
                'path': dir_path,
                'file_name': file_name
            }
        ))

    def search(self, path, pattern):
        """
        Search for files/folders.
        """
        return self.req(self.endpoint(
            func='search',
            params={
                'limit': 10000,
                'start': 0,
                'source_path': path,
                'keyword': pattern
            }
        ))

    def delete(self, path):
        """
        Delete file(s)/folder(s)
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='delete',
            params={
                'path': dir_path,
                'file_total': 1,
                'file_name': file_name
            }
        ))

    def download(self, path):
        """
        Download file.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req_binary(self.endpoint(
            func='download',
            params={
                'isfolder': 0,
                'source_total': 1,
                'source_path': dir_path,
                'source_file': file_name
            }
        ))

    def upload(self, path, data, overwrite=True):
        """
        Upload file.
        """
        dir_path = os.path.dirname(path)
        file_path = path.replace('/', '-')
        file_name = os.path.basename(path)
        return self.req_post(self.endpoint(
            func='upload',
            params={
                'type': 'standard',
                'overwrite': 1 if overwrite else 0,
                'dest_path': dir_path,
                'progress': file_path
            }),
            files={
                'file': (
                    file_name,
                    data,
                    'application/octet-stream'
                )
            }
        )