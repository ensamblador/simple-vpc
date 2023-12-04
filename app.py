#!/usr/bin/env python3
import os

import aws_cdk as cdk

from network.network_stack import NetworkStack

TAGS = {"app": "generative ai business apps", "customer": "vpc-stack"}

app = cdk.App()
stk = NetworkStack(app, "vpc-stack")


if TAGS.keys():
    for k in TAGS.keys():
        cdk.Tags.of(stk).add(k, TAGS[k])
app.synth()
