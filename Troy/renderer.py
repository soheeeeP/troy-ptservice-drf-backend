import json

from rest_framework import renderers


class ResponseRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status = 'success'
        if 'ErrorDetail' in str(data):
            status = 'error'

        response = json.dumps({'status': status, 'data': data})
        return response
