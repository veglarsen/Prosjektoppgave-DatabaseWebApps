#!/usr/bin/python
import sys
import logging
activate_this = '/stud/vla018/public_html/flask_prosjekt/flask_prosjekt/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/vla018/public_html/flask_prosjekt/")
sys.path.insert(1,"/stud/vla018/public_html/flask_prosjekt/flask_prosjekt/")

from flask_prosjekt import app as application