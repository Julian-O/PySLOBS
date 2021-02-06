## Progress

This project has now been released. However, the API is very large, and some
parts remain untested.

### Core Infrastructure

The ability to connect to the server, send commands, receive replies and 
subscribe to notifications is all in place.

All of the SlobsServices and Slobs classes have been defined.

All of the Events and Properties have been defined.

All 268 commands that can be called on Classes and Services have been implemented.
However, they have not all been tested.

### Testing

It is difficult to write meaningful unit tests; the API is incompletely 
defined, and often depends unpredictably on the hardware set up, the
StreamLabs OBS configuration and no doubt the version.

It is necessary to run each server command and manually inspect the
result - this has been dubbed "exercising" rather than "testing" the commands
to emphasize its unsatisfactory nature.

The exercises are divided into four categories:

   * #### Read-Only Exercises
   
   These exercises are pretty safe to run, and generally just display the
   current configuration and usage of StreamLabs OBS.

   * #### UI-Affecting Exercises
   
   These exercises are pretty safe to run, but make temporary changes
   to the display: e.g. opening up dialog boxes or showing test notifications.
   
   * #### Read-Write Exercises
   
   These exercises make changes to the StreamLabs OBS configuration, but
   attempt to restore the settings back to how they were found.
   
   However, if they fail for any reason, it may leave your configuration
   changed. Use a test installation and/or make backups before running. 

   * #### Destructive Exercises
   
   These exercises make permanent changes, including **broadcasting a 
   new stream**.
   
   Ensure you are logged into a test account on your streaming host, or 
   your followers may get very confused when test data is streamed out.
   
 ### Progress Chart
 
 This unwieldy chart is colour-coded to show progress towards getting every
 Service, Class, Property, Event and Method available on the API covered 
 by the exercise code.
 
 ![Progress Chart](progress_chart.png)