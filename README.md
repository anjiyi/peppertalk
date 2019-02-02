# PepperTalk

Pepper talk is a messenger personal assistant with a spicy personality, it implements a list of specialists that can help you with tasks and provide spicy information.

# Run book
## Dependencies:
For development, we use pipenv. Is a package manager similar to npm, where you provide a list of dependencies and pipenv takes care of resolving them. To:
- install pipenv: `brew install pipenv`
- install deps: `pipenv install`

## Run 
You will need the env variables to run pepper talk, as @anjiyi or @andrekiu for them. After getting them you can run pepper talk with 2 bash scripts:
- `./dev.sh`: starts a flask server with the proper configuration
- `./test.sh`: runs all the unit tests, MUST BE RAN BEFORE COMMITING CODE

# Code
Pepper talk is divided in:
- app.py: Routes to debug and reply to messenger
- peppertalk.py: Deprecated logic that must be migrated to specialists
- lib/: core modules that power peppertalk, see `message.py` and `reply.py` to get an idea on how to customize peppertalk
- lib/specialists: commands that peppertalk can reply to. All specialists have to extend PepperSpecialist, see `base.py`

# Tests
All the app has unit tests that are ran by `./tests.sh`, the only special test is `teste2e.py` that makes sure the app don't crash. If this test doesn't pass the pepper is dead.
