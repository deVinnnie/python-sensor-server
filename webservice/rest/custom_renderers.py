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

class RawMeasurementJSONRenderer(renderers.BaseRenderer):
    """
    Renderer which serializes to a specific lite format for a list of Measurement objects.
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

        """"
         {
            measurements: [
                { "2015-01-01T00:00:00", 10.54545},
                { "2015-02-01T00:00:00", 10.54654}
            ]
         }
        """

        ret = '{ "measurements": ['
        for d in data['measurements']:
            ret+= '{{"{}", {} }},'.format(d['timestamp'], d['value'])
            ret+="\n"
        ret += "]}"

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
    Renderer which serializes to a specific lite format for a list of Measurement objects.
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

        """"
        {
            "interval" : "12",
            "meta" : "super"
        }
        """

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
