# Dronery

Python based REST API to handle a drones delivery service using the micro framework Bottle.

## General goals
- JSON based input/output
- Standards compliant endpoints with a versionated API interface '/api/v#' (althought just v1 is being developed at the moment)
- Dependencies at the minimum
- Portability (use a local database)
- Bare bones API features to keep the server implementation general enough but, it imposes more processing on the client side
- Image files are not support in binary format, just Base64 encodings with an associated MIME type for the client to know how to handle it

## General features
- Drones management through '/api/v#/drones' endpoint
- Medications management through '/api/v#/medications' endpoint
- Images management through '/api/v#/images' endpoint (Base64 encoding only)
- Loads management through '/api/v#/loads' endpoint
- CORS enabled for browser based clients
- Cache control headers support (just a general no-store policy at the moment)

## Run (hosted)
- Install Python 3.9.7+ (it may work with any Python 3 version but it is only tested against v3.9.7)
- Clone repository into a local directory
- Start a terminal in that directory
- Create a virtual environment (optional but recommended)
- Install dependencies
- Start the server: python -m bottle main:root

## Test (hosted)
- Install Python 3.9.7+ (it may work with any Python 3 version but it is only tested against v3.9.7)
- Clone repository into a local directory
- Start a terminal in that directory
- Create a virtual environment (optional but recommended)
- Install dependencies
- Start the server: python -m bottle main:root
- Run tests: python -m unittest tests
