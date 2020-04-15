import requests
import json
import logging

# MIT License
#
# Copyright (c) 2020 Yash Karandikar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

logger = logging.getLogger(__name__)


def request(target: str, headers: dict):
    with requests.Session() as session:
        session.headers.update(headers)
        url = f"https://theorangealliance.org/api{target}"
        logger.info(f"Recieved request to {url}")
        with session.get(url) as resp:
            if resp.status_code != 200:
                logger.info(
                    f"Status code was not 200 ({resp.status_code}), attempting to gather error message"
                )
                try:
                    data = json.loads(resp.text)
                except json.decoder.JSONDecodeError:
                    raise WebException(resp.text)
                else:
                    raise WebException(data["_message"])
            data = json.loads(resp.text)
    logger.info(f"Request succsessful, returning response to origin")

    return data


class WebException(Exception):
    def __init__(self, message: str):
        if message == "The supplied API key was not found.":
            message = "The supplied API key was invalid."
        self.message = message
        logger.error(f"fatal: {self.message}")
        super().__init__(message)
