import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request:
    def __init__(self, url):
        self._url = url

    def get_url(self):
        return self._url


class Resource:
    def __init__(self, har_data):
        self._request = Request(har_data['request']['url'])
        self._response = Response(har_data['response']['headers'],
                                  har_data['response']['content'])

    def get_fullpath(self):
        url = self._request.get_url()
        return re.sub('^(https?://)', '', url)

    def get_content(self):
        return self._response.get_content()

    def is_image(self):
        """Verify if the resource is an image.
        """
        content_type = self._response.get_content_type()

        if content_type is None:
            return False

        if re.search("image/(gif|png|jpe?g|webp)", content_type):
            return True

        return False

    def __repr__(self):
        """Returns a representation for resource.
        """
        return "<Resource is_image={}>".format(self.is_image())


class Response:
    def __init__(self, headers, content):
        self._headers = headers
        self._content = content

    def get_content(self) -> str:
        return self._content

    def get_content_type(self) -> str:
        for header in self._headers:
            if header['name'].lower() == 'content-type':
                return header['value']

        return None
