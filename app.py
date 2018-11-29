""" app.py """
# coding: utf-8

from logging import Formatter
from logging import INFO
from logging import StreamHandler
from logging import getLogger

import csv
import io
import re

from flask import Flask
from flask import request
from flask import render_template


logger = getLogger(__name__)  # pylint: disable=invalid-name
handler = StreamHandler()  # pylint: disable=invalid-name
handler.setFormatter(Formatter("%(module)s:%(lineno)s %(message)s"))
logger.setLevel(INFO)
logger.addHandler(handler)


app = Flask(__name__)  # pylint: disable=invalid-name


@app.route("/", methods=["GET"])
def get_index():
    """ GET / """
    return render_template("index.html")


@app.route("/", methods=["POST"])
def post_index():
    """ POST / """
    message_in = request.form["message_in"]
    logger.error(message_in)
    messages = []
    with io.StringIO(message_in) as _f:
        _reader = csv.reader(_f, dialect="excel-tab")
        for cols in _reader:
            if "".join(cols) == "":
                continue
            cols = [re.sub(r"\r?\n", " <br />", col) for col in cols]
            # in backlog markdown, cell "-" lead to break table
            cols = [col.replace("-", "") if col == "-" else col for col in cols]  # noqa: E501
            messages.append(" | ".join(cols))

    if len(messages) > 2:
        _messages = [messages[0], " | ".join(["----"] * len(messages))]
        _messages.extend(messages[1:])
        messages = _messages

    message_out = "\n".join(messages)

    return render_template(
        "index.html",
        message_in=message_in,
        message_out=message_out,
    )


if __name__ == '__main__':
    app.run(debug=True)
