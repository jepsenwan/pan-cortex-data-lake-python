#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging Service example using query, poll, delete."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.logging import LoggingService

url = 'https://apigw-qa6.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Create Logging Service instance
ls = LoggingService(
    url=url,
    verify=False,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

data = {  # Prepare 'query' data
    "q": "select * from panw.traffic limit 1",
    "startTime": 0,  # 1970
    "endTime": 1609459200,  # 2021
    "maxWaitTime": 0  # no logs in initial response
}

# Generate new 'query'
q = ls.query(data)

print(
    "\nQUERY: {}\n".format(q.text)
)

query_id = q.json()['queryId']  # access 'queryId' from 'query' response

params = {  # Prepare 'poll' params
    "sequenceNo": 0,  # initial sequenceNo
    "maxWaitTime": 3000
}

# Poll 'query' for results
p = ls.poll(query_id, params)

try:
    print(
        "{}: jobID: {}, sequenceNo: {}, retrieving from {}, size: {},"
        " took: {} ms\n\nRESULT: {}\n".format(
            p.json()['status'],
            p.json()['jobId'],
            p.json()['sequenceNo'],
            p.json()['result']['esResult']['from'],
            p.json()['result']['esResult']['size'],
            p.json()['result']['esResult']['took'],
            p.text,
        )
    )
except TypeError:
    print(
        "{}: jobID: {}, sequenceNo: {}".format(
            p.json()['status'],
            p.json()['jobId'],
            p.json()['sequenceNo'],
        )
    )

# Delete 'job'
d = ls.delete(query_id)

# Print 'delete' results
print(
    "DELETE: {}\n".format(d.text)
)
