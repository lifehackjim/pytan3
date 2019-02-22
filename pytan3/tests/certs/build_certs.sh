#!/bin/bash
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
