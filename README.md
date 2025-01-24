# BGP320 Device Lister

Retrieves the BGP-320 device list page and dumps it in JSON format.  The BGP-320-500 is used by AT&T Fiber.

## Installation

Create a new python3 virtual environment.  You can also install the requurements directly into your environment's python lib if you prefer.

```
python3 -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Usage

Acvitvate the python virtual environment created during installation if not already active:

```
source .venv/bin/activate
```

Then execute the script:

```
python3 bgp320-devices.py [ --url yourURL ]
```
