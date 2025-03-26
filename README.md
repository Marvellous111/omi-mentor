# Omi-Grok Mentor App

This project is a fastAPI application

## Project Type: FastAPI

We could use any other framework, but for speed and for parallel development we will use fastAPI

## IMPORTANT NOTE

We are relying on the example given to us with a lot of tweaks since it is a good entry point.
Further work on this app will slowly move away from the example to a more concrete work.
comments tagged with (from example) are gotten from example
comments tagged with (not example) are novel
comments tagged with (perhaps example) are edited example code

## FUTURE WORK

1. Chat Continuity: Talk to mentor in an isolated environment about problems based on the topic mentor gathers from your conversations in realtime.

2. Store mentor advice and conversation in a secure database to be used for context and future references where necessary.

## HOSTING SERVICE

Amazon ec2 or Render will be used for the hosting service.


Tasks to complete (not to be pushed):
1. Host the platform on either render or ec2 (must not have downtimes) use credit model if needed, coolify is also great
2. Register the app on the omi app
3. Use the endpoint for the webhook for the transcript url
4. Get the app url for the app and put it in the code
5. Look for api_base_url and api_key_notification for the app and put them inside env with codebase (question on the discord channel can be asked)