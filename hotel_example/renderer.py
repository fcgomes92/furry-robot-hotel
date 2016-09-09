from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


class _JSONResponse(object):
    content_type = 'application/json'
    charset = 'utf-8'
    renderer = JSONRenderer()

    def http_json_response(self, content: str, status=status.HTTP_200_OK,
                           content_type=None, charset=None):
        data = self.renderer.render(content)
        return HttpResponse(
            status=status,
            content_type=content_type if content_type else self.content_type,
            content=data.encode(charset) if charset else data)


JSONResponse = _JSONResponse()
