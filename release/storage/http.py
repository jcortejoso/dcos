import os

import requests

from release.storage import AbstractStorageProvider
from pkgpanda.exceptions import FetchError


class HttpStorageProvider(AbstractStorageProvider):
    name = 'http'

    def __init__(self, url):
        self.__url = url.rstrip('/') + '/'

    def _get_absolute(self, path):
        assert not path.startswith('/')
        return self.__url + path

    def copy(self,
             source_path,
             destination_path):
        tmp_path = os.path.join(os.getcwd(), source_path + '.tmp')
        self.download(source_path, tmp_path)
        self.upload(destination_path, local_path=tmp_path)
        os.remove(tmp_path)

    def upload(self,
               destination_path,
               blob=None,
               local_path=None,
               no_cache=None,
               content_type=None):
        assert local_path is None or blob is None
        if local_path:
            with open(local_path, 'rb') as data:
                requests.put(self._get_absolute(destination_path), data=data, auth=(self.__user, self.__pass))
        else:
            assert blob is not None
            assert isinstance(blob, bytes)
            requests.put(self._get_absolute(destination_path), data=blob, auth=(self.__user, self.__pass))

    def download_inner(self, path, local_path):
        local_path_tmp = '{}.tmp'.format(local_path)
        url = self._get_absolute(path)
        try:
            with open(local_path_tmp, 'w+b') as f:
                r = requests.get(url, stream=True)
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
                os.rename(local_path_tmp, local_path)
        except Exception as fetch_exception:
            rm_passed = False
            # Delete the temp file, re-raise.
            try:
                os.remove(local_path_tmp)
                rm_passed = True
            except Exception:
                pass
            raise FetchError(url, local_path, fetch_exception, rm_passed) from fetch_exception

    def exists(self, path):
        url = self._get_absolute(path)

        # TODO(cmaloney): 200 is overly restrictive here... After hitting more
        # webservers expand to include other common / valid status codes that
        # indicate resource is found / exists.
        return requests.head(url=url).status_code == 200

    def fetch(self, path):
        r = requests.get(url=self._get_absolute(path))
        r.raise_for_status()
        return r.body

    def remove_recursive(self, path):
        raise NotImplementedError()

    def list_recursive(self, path):
        raise NotImplementedError()

    @property
    def url(self):
        return self.__url

    @property
    def read_only(self):
        return True

factories = {
    'read': HttpStorageProvider
}
