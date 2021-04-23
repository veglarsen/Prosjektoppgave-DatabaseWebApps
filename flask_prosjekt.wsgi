#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/vla018/public_html/flask_prosjekt/")
sys.path.insert(1,"/stud/vla018/public_html/flask_prosjekt/flask_prosjekt/")

from flask_prosjekt import app as application