PySLOBS: A Python Wrapper for the StreamLabs OBS API
-------------------------------------

### About the API

Streamlabs OBS (SLOBS) is a live streaming software that integrates Open Broadcaster 
Software with additional features.

It offers the 
[Streamlabs OBS API](https://github.com/stream-labs/streamlabs-obs-api-docs) to allow
third-party applications to interact with the application while it is running.

This includes selecting, editing and monitoring scenes, video sources and audio 
sources. It includes monitoring performance.

This doesn't include chat or getting notifications about donations, subscriptions and
followers. You will need to look elsewhere for that.

Typically, it would be accessed from same computer that is running Stream OBS, or from
a computer on the same LAN.

The API is based on [WebSockets](https://en.wikipedia.org/wiki/WebSocket) so it can
be accessed from a browser in JavaScript. (Apparently, it can also be accessed through
a named pipe.)

###  About the Python Wrapper

Rather than accessing it from Javascript, this Python wrapper allows access to
Streamlabs OBS from a Python application. The details about websockets are hidden
and more Pythonic interfaces are provided.

This Python wrapper is based on `asyncio`. If you have not used the `asyncio` features
of Python before, please consult a tutorial.

##### Versions

Python 3.7 is the minimum, and has not been tested.
Python 3.9 is recommended, and has been tested.

##### Clean Python

The Python interface is designed to allow you to write PEP8-compliant Python code.

Camel-case items in the original API are represented in their preferred PEP8 form - 
i.e. underscores between words to avoid ambiguity and capitalised constants.

Enumerated types and named tuples are used in preference to JSON dictionaries and 
numeric constants where possible.

Identifiers that clash with reserved words used in Python are suffixed with `_` - e.g.
`id_()`.

Date-times from notifications do not have a timezone associated with them. They  are in
the timezone of the host running the API. 

### Alpha Release

The API is moderately large. This version of the Python wrapper does NOT cover all of it
- or even a large proportion of it. It is focussed on the areas the developers actively
want to use first. However, the aim is to have a sufficient prepared infrastructure that
extending it out it a fairly rote task.

See `PROGRESS.md` for an idea of what is and isn't implemented.

### Usage

### Authentication

To connect to StreamLabs OBS, you must be authenticated. 
See `tests\config.py` for instructions.

#### Connection

First, you need a `SlobsConnection` instance.
Connections actively process received messages, so it is important that they
be included in the `asyncio` event loop.

So your main program might look like this:
 
    import asyncio
    import logging
    from pyslobs import connection
 
    async def main():
        token = "API token from Remote Control screen"
        
        # Provide any non-default port and IP address here
        conn = connection.SlobsConnection(token)  

        # Give CPU to both your task and the connection instance.
        await asyncio.gather(
                conn.background_processing(),
                do_your_thing(conn)
                )
                
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())      
 
Connections should be closed when complete, so the background processing can 
know to shut-down.

#### Services

Once you have a connection, it can be used to instantiate any of nine Services:

1. AudioService
1. NotificationsService
1. PerformanceService
1. SceneCollectionsService
1. ScenesService 
1. SelectionService 
1. SourcesService
1. StreamingService
1. TransitionsService

Services can be used:
  * subscribe to events, such as when the user selects a new active scene.
  * to make some limited direct changes, such as setting an active scene by
    scene id.
  * fetch Objects that can be manipulated more directly.
  
#### Classes  
  
In the original API they describe "Classes", which are called represented by subclasses
of `SlobsClass` in the Python API.

Subclasses include:

1. AudioSource
1. Scene
1. SceneItem
1. SceneItemFolder
1. SceneNode
1. Selection
1. Source

Instances of SlobsClass should only be constructed through Services methods and methods
on other instances. 

Objects may have properties (such as names) that can be accessed. Be careful that the
values of these properties may be out-of-date if the value was changed within the app
or if it was changed through a different instance referencing the same SLOBS resource.

Objects can be used to fetch other Objects or `namedtuples` describing other records 
in the API.

#### Subscriptions

Some `Services` offer methods that allow you to subscribe to events.

TO DO: Instructions

## Examples:

The examples folder contains many small programs to demonstrate how to use the
API.

See `tests\config.py` for instructions on authentication.

## Special cases:

* Sources have an additional field `configurable` which isn't documented.
