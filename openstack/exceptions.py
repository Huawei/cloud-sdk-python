# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#      Huawei has modified this source file.
#     
#         Copyright 2018 Huawei Technologies Co., Ltd.
#         
#         Licensed under the Apache License, Version 2.0 (the "License"); you may not
#         use this file except in compliance with the License. You may obtain a copy of
#         the License at
#         
#             http://www.apache.org/licenses/LICENSE-2.0
#         
#         Unless required by applicable law or agreed to in writing, software
#         distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#         WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#         License for the specific language governing permissions and limitations under
#         the License.

"""
Exception definitions.
"""

import re

import six

class MissingRequiredArgument(BaseException):
    message = "ClientException"
    def __init__(self, message=None):
        self.message = message or self.message
        super(MissingRequiredArgument, self).__init__(self.message)

class SDKException(BaseException):
    """The base exception class for all exceptions this library raises."""

    def __init__(self, message=None, cause=None):
        self.message = self.__class__.__name__ if message is None else message
        self.cause = cause
        super(SDKException, self).__init__(self.message)


class EndpointNotFound(SDKException):
    """A mismatch occurred between what the client and server expect."""

    def __init__(self, message=None):
        super(EndpointNotFound, self).__init__(message)


class InvalidResponse(SDKException):
    """The response from the server is not valid for this request."""

    def __init__(self, response):
        super(InvalidResponse, self).__init__()
        self.response = response


class InvalidRequest(SDKException):
    """The request to the server is not valid."""

    def __init__(self, message=None):
        super(InvalidRequest, self).__init__(message)


class HttpException(SDKException):
    def __init__(self, message=None, details=None, response=None,
                 request_id=None, url=None, method=None,
                 http_status=None, cause=None, code=None):
        super(HttpException, self).__init__(message=message, cause=cause)
        self.details = details
        self.response = response
        self.request_id = request_id
        self.url = url
        self.method = method
        self.http_status = http_status
        self.code = code

    def __unicode__(self):
        msg = self.__class__.__name__ + ": " + self.message
        if self.details:
            msg += ", " + six.text_type(self.details)
        return msg

    def __str__(self):
        return self.__unicode__()


class NotFoundException(HttpException):
    """HTTP 404 Not Found."""
    pass


class MethodNotSupported(SDKException):
    """The resource does not support this operation type."""

    def __init__(self, resource, method):
        # This needs to work with both classes and instances.
        try:
            name = resource.__name__
        except AttributeError:
            name = resource.__class__.__name__

        message = ('The %s method is not supported for %s.%s' %
                   (method, resource.__module__, name))
        super(MethodNotSupported, self).__init__(message=message)

class MicroversionNotSupported(SDKException):
    """The service does not support microversion."""
    def __init__(self, service_type, version):
        message = ('The %s service is not support microversion' %
                   (service_type))
        super(MicroversionNotSupported, self).__init__(message=message)


class DuplicateResource(SDKException):
    """More than one resource exists with that name."""
    pass


class ResourceNotFound(NotFoundException):
    """No resource exists with that name or id."""
    pass


class ResourceTimeout(SDKException):
    """Timeout waiting for resource."""
    pass


class ResourceFailure(SDKException):
    """General resource failure."""
    pass


code_key_list = ["code", "errorCode", "errCode", "error_code"]

message_key_list = ["message", "error_message", "externalMessage",
                    "error_msg", "details", "NeutronError",
                    "computeFault", "TackerError", "error"]


def auto_detect_errors(obj):
    code = ""
    message = ""
    if isinstance(obj, dict):
        que = [obj]
        while que:
            node = que.pop()
            keys = list(node.keys())
            for key in keys:
                if key in code_key_list:
                    codevalue = node.get(key)
                    if isinstance(codevalue, dict):
                        que.append(codevalue)
                    elif code == "":
                        code = str(codevalue)
                if key in message_key_list:
                    msgvalue = node.get(key)
                    if isinstance(msgvalue, dict):
                        que.append(msgvalue)
                    elif message == "":
                        message = str(msgvalue)
                if key not in code_key_list and key not in message_key_list and isinstance(node.get(key), dict):
                    que.append(node.get(key))
            if code and message:
                break
    return [code, message]


def from_exception(exc):
    """Return an instance of an HTTPException based on httplib response."""
    if exc.response.status_code == 404:
        cls = NotFoundException
    else:
        cls = HttpException

    resp = exc.response
    details = resp.text
    resp_body = resp.content
    content_type = resp.headers.get('content-type', '')
    if resp_body and 'application/json' in content_type:

        # compatibility for HuaWei OpenStack Service error response

        exec_data = auto_detect_errors(resp.json())
        code = exec_data[0]
        message = exec_data[1]
        details = "[" + code + "]" + message if code != "" else message

        if code == "" and message == "":
            for obj in resp.json().values():
                if isinstance(obj, dict):
                    exec_data = auto_detect_errors(obj)
                    code = exec_data[0]
                    message = exec_data[1]
                    if code or message:
                        details = "[" + code + "]" + message if code != "" else message
                        break

        return cls(details=details, message=message, response=exc.response,
                   request_id=exc.request_id, url=exc.url, method=exc.method,
                   http_status=exc.http_status, cause=exc, code=code)

        # # Iterate over the nested objects to retrieve "message" attribute.
        # messages = [obj.get('message') for obj in resp.json().values()
        #             if isinstance(obj, dict)]
        # # Join all of the messages together nicely and filter out any objects
        # # that don't have a "message" attr.
        # details = '\n'.join(msg for msg in messages if msg)

    elif resp_body and 'text/html' in content_type:
        # Split the lines, strip whitespace and inline HTML from the response.
        details = [re.sub(r'<.+?>', '', i.strip())
                   for i in details.splitlines()]
        details = [msg for msg in details if msg]
        # Remove duplicates from the list.
        details_temp = []
        for detail in details:
            if detail not in details_temp:
                details_temp.append(detail)
        # Return joined string separated by colons.
        details = ': '.join(details_temp)
        return cls(details=details, message=exc.message, response=exc.response,
                   request_id=exc.request_id, url=exc.url, method=exc.method,
                   http_status=exc.http_status, cause=exc)
