# Dronery

Python based REST API to handle a drones delivery service using the micro framework Bottle. The principal cargo for the drones to carry on are medications. The comunication interface from/to the drones is not provided and outside of the scope of this project. This is just a demo to test the features (and lack of) of the selected framework for RESTful API development. It is a prototype not intended for production at the moment.

## General goals
- JSON based input/output
- Standards compliant endpoints with a versionated API interface '/api/v#' (althought just v1 is being developed at the moment)
- Dependencies at the minimum
- Portability (provided Python 3 is installed and available)
- Bare bones API features to keep the server implementation general enough (it imposes more processing on the client side as a side effect). This means that there are mostly generic CRUD capable endpoints with minimum "special cases" provided as "special endpoints". All in favor of predictability over specialization.
- Image files are not support in binary format, just Base64 encodings with an associated MIME type for the client to know how to handle it
- Protect sensitive API endpoints with authentication/authorization (just the very basic as a proof of concept more than security hardening)
- Provide some testing capabilities (using built-in unittest module and Boddle to mock requests)
- Provide some sort of endpoints self discovery when exploring with a web browser

## General features
- Drones management through '/api/v#/drones' endpoint
- Medications management through '/api/v#/medications' endpoint
- Images management through '/api/v#/images' endpoint (Base64 encoding for the binary content)
- Loads management through '/api/v#/loads' endpoint
- CORS enabled for browser based clients
- Cache control headers support (just a general 'no-store' policy at the moment)
- Access control over management operations (plain old username:password http auth at the moment)
- Periodic execution of an audit task to log information about battery capacity of the drones (at the moment it is just a another thread running at a fixed interval)
- Basic filtering via GET parameters for the endpoints listing collections

## Knwon issues
- When the server crashes due to an unexpected error, then the thread running the audit task keeps running on its own. This can be easily addressed by moving the audit task execution to an OS dependent scheduler alternative (like cron, systemd, etc) or running the server and the audit task in separate execution contexts. This approach was not used here to keep it simple and portable.

## Requirements
- Install Python 3.9.7+ (it may work with any Python 3 version but it is only tested against v3.9.7)
- Clone repository into a local directory (or simply unzip the downloaded archive)
- Start a terminal in that directory:
`
cd /path/to/project/
`
- Create a virtual environment (optional but recommended):
´
python -m venv .venv
´
- Activate the newly created virtual environment:
    - Bash
    `
    source .venv/bin/activate
    `
    - Windows CMD
    `
    .venv\Scripts\activate.bat
    `
    - Powershell
    `
    .venv\Scripts\activate.ps1
    `

## Test
- Make sure the previously listed requirements are met
- Install dependencies:
´
pip install -r ./tests/requirements.txt
´
- Run tests:
´
python -m unittest -v
´

## Start the server
- Make sure the previously listed requirements are met
- Install dependencies:
´
pip install -r ./requirements.txt
´
- Start the server:
´
python -m bottle main:root
´
- Point your browser to http://localhost:8080
