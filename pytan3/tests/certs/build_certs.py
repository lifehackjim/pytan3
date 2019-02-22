#!python
# -*- coding: utf-8 -*-
"""Create certs needed for PyTan test suite.

This is a bit of a hack, and will probably only work on OSX.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import subprocess  # nosec

try:
    import pathlib
except ImportError:  # pragma: no cover
    import pathlib2 as pathlib

THIS_DIR = pathlib.Path(__file__).absolute().parent

script_contents = r"""#!/bin/bash
# thanks to: https://stackoverflow.com/a/41366949/10843944

openssl req -x509 \
    -newkey rsa:4096 \
    -sha256 \
    -days 3650 \
    -nodes \
    -keyout key.pem \
    -out cert.pem \
    -extensions san \
    -config <(echo "[req]"; echo distinguished_name=req; echo "[san]"; echo subjectAltName=DNS:example.com,DNS:example.net,DNS:localhost,IP:127.0.0.1) \
    -subj /CN=example.com

openssl req -x509 \
    -newkey rsa:4096 \
    -sha256 \
    -days 3650 \
    -nodes \
    -keyout otherkey.pem \
    -out othercert.pem \
    -extensions san \
    -config <(echo "[req]"; echo distinguished_name=req; echo "[san]"; echo subjectAltName=DNS:otherexample.com,DNS:otherexample.net,IP:127.0.0.2) \
    -subj /CN=otherexample.com

openssl ecparam -genkey -name secp256k1 -out eckey.pem
openssl req -new \
    -sha256 \
    -key eckey.pem \
    -keyout eckey.pem \
    -out eccsr.pem \
    -subj /CN=ecexample.com

openssl req -x509 \
    -sha256 \
    -days 3650 \
    -key eckey.pem \
    -in eccsr.pem \
    -out eccert.pem \
    -extensions san \
    -config <(echo "[req]"; echo distinguished_name=req; echo "[san]"; echo subjectAltName=DNS:ecexample.com,DNS:ecexample.net,DNS:localhost,IP:127.0.0.1)
"""  # noqa

if __name__ == "__main__":
    script_name = "build_certs.sh"
    script_path = THIS_DIR / script_name
    script_path.write_text(script_contents)
    script_path.chmod(0o700)
    subprocess.run(format(script_path))  # nosec
