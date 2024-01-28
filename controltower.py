import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.exceptions import ClientError
from urllib import request, error
import os
import json

from functools import partial

REGION = os.environ["AWS_REGION"]
SERVICE = "controltower"
SERVICE_URL = f'https://prod.{REGION}.blackbeard.aws.a2z.com/'

def make_signed_headers(method, url, data=None, params=None, headers=None):
    session = boto3.Session()
    credentials = session.get_credentials()
    creds = credentials.get_frozen_credentials()

    request = AWSRequest(method=method, url=url, data=data, params=params, headers=headers)
    SigV4Auth(creds, SERVICE, REGION).add_auth(request)
    return dict(request.headers)

def signed_request(method, url, data=None, headers=None):
    signed_headers = make_signed_headers(method=method, url=url, data=data, headers=headers)
    return request.Request(url, method=method, headers=signed_headers, data=data)

def execute_control_tower_operation(operation, data):
    headers = {
        'Content-Type': 'application/x-amz-json-1.0',
        'X-Amz-Target': f'AWSBlackbeardService.{operation}',
    }
    data = json.dumps(data).encode()
    try:
        _request = signed_request(
            method='POST',
            url=SERVICE_URL,
            headers=headers,
            data=data
        )
        response = request.urlopen(_request)
    except error.HTTPError as e:
        err = json.load(e.fp)
        raise ClientError(
            operation_name=operation,
            error_response={
                'Error': {
                    'Code': err['__type'].split('#')[-1],
                    'Message': err.get('Message', "")
                }
            }
        ) from e

    return json.loads(response.read())

def exec_wrapper(operation, **kwargs):
    return execute_control_tower_operation(operation, kwargs)

def __getattr__(param):
    operation = ''.join(map(lambda x: x.title(), param.split('_')))
    return partial(exec_wrapper, operation)
