#!/usr/bin/env python3.13
import os
import aws_cdk as cdk
from infra.gate_agent_be_stack import GateAgentBeStack

app = cdk.App()
GateAgentBeStack(app, "GateAgentBeStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()