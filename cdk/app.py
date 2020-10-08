#!/usr/bin/env python3
import os.path
from aws_cdk.core import App
from stacks.photo_resizer import PhotoResizer
from stacks.vpc import YelpNetwork

src_root_dir = os.path.join(os.path.dirname(__file__),"..")

app = App()
PhotoResizer(app, "yelp-photo-resizer", src_root_dir= src_root_dir)
YelpNetwork(app, "YelpNetwork")

app.synth()
