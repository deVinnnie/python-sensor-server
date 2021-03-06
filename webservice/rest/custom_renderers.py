#from django.utils.encoding import smart_unicode
from django.utils.encoding import smart_text
from rest_framework import renderers
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS, template_render
)
import json
from rest_framework.utils import encoders
from rest_framework.settings import api_settings
from django.utils import six
from django.template import RequestContext
from rest_framework.renderers import TemplateHTMLRenderer


class RawMeasurementJSONRenderer(renderers.BaseRenderer):
    """
    Renderer which serializes to a specific lite format for a list of Measurement objects.

    Example output
    {
        measurements: [
            { "2015-01-01T00:00:00", 10.54545},
            { "2015-02-01T00:00:00", 10.54654}
        ]
    }
    """
    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder
    ensure_ascii = not api_settings.UNICODE_JSON
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}

        separators = INDENT_SEPARATORS

        if not 'measurements' in data:
            jsonRenderer = renderers.JSONRenderer()
            ret = jsonRenderer.render(data, accepted_media_type=None, renderer_context=None)
            return ret

        responseData = { "measurements" : [] }

        for d in data['measurements']:
            responseData["measurements"].append([d['timestamp'], d['value']])

        ret = json.dumps(
            responseData, cls=self.encoder_class,
            ensure_ascii=self.ensure_ascii,
            separators=separators
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))

        return ret


class RawConfigJSONRenderer(renderers.BaseRenderer):
    """
    Renderer which serializes to a specific lite format for a list of Configuration objects.

    {
        "interval" : "12",
        "meta" : "super"
    }
    """
    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder
    ensure_ascii = not api_settings.UNICODE_JSON
    charset = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        separators = INDENT_SEPARATORS

        config = {}
        for d in data:
            config[d['attribute']] = d['value']

        ret = json.dumps(
            config, cls=self.encoder_class,
            ensure_ascii=self.ensure_ascii,
            separators=separators
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))

        return ret



# Adapted from https://gist.github.com/egasimus/6095421
class BypassRenderer(object):
    bypass = True


class CustomTemplateHTMLRenderer(BypassRenderer, TemplateHTMLRenderer):
    def resolve_context(self, data, request, response):
        if response.exception:
            data['status_code'] = response.status_code
        return RequestContext(request, {'data': data})