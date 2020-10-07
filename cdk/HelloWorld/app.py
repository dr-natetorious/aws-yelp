#!/usr/bin/env python3

from aws_cdk import core

from hello_world.hello_world_stack import HelloWorldStack


app = core.App()
HelloWorldStack(app, "hello-world")

app.synth()
