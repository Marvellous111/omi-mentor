# Omi-Grok Mentor App

A mentor that advices you and tells you what to do based on your conversations.

## Project Type

We could use any other framework, but for speed and for parallel development we will use fastAPI

### Stack

1. FastAPI
2. Render (for hosting, will migrate to amazon ec2 in future iterations)
3. Python
4. Omi for the conversation recording using the app (also device compatible)

## IMPORTANT NOTE

We are relying on the example given to us with a lot of tweaks since it is a good entry point.
Further work on this app will slowly move away from the example to a more concrete work.
comments tagged with (from example) are gotten from example
comments tagged with (not example) are novel
comments tagged with (perhaps example) are edited example code

Due to quick server deployment to test the code we are making use of render. Later we will migrate to amazon ec2.

## FUTURE WORK

1. Chat Continuity: Talk to mentor in an isolated environment about problems based on the topic mentor gathers from your conversations in realtime.

2. Store mentor advice and conversation in a secure database to be used for context and future references where necessary.

3. Build the homepage for the mentor app and host it for first time users of the app to see with setup instructions.

4. Build tests for the app using github actions or something else later.

5. We will add chat feature for the app as well in omi (in the omi app)

6. Change hosting service to amazon ec2 instead of render to get rid of server inactivity when spun down.

7. Look for api_base_url and api_key_notification for the app and put them inside env with codebase (question on the discord channel can be asked)

8. Create cron job to send notification from mentor to user from time to time (basically creating reminder)
