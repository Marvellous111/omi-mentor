# Omi-Grok Mentor App

A mentor that advices you and tells you what to do based on your conversations.

## Project Type

I could use any other framework, but for speed and for parallel development I will use fastAPI

### Stack

1. FastAPI
2. Render (for hosting, will migrate to amazon ec2 in future iterations)
3. Python
4. Omi for the conversation recording using the app (also device compatible)

## IMPORTANT NOTE

I am relying on the example given to me with a lot of tweaks since it is a good entry point.
Further work on this app will slowly move away from the example to a more concrete work.
comments tagged with (from example) are gotten from example
comments tagged with (not example) are novel
comments tagged with (perhaps example) are edited example code

Due to quick server deployment to test the code I am making use of render. Later I will migrate to amazon ec2.

## HOW TO USE

1. Enter the omi app

2. Navigate to the explore section of the app

3. Search for Omi mentor by marvellous (Still pending approval to be made public)

4. Click on the app if found and install it. App link: ([Omi mentor](https://h.omi.me/apps/01JQBGSHPMWB0H6ER6YSR1JFS0))

5. A homepage will show when installed (due to use of render this initial load of the homepage is necessary)

6. Once the homepage shows the active session, this means the server has started, you are free to keep refreshing the homepage till you see a json response that looks like this:

  ```json
  {
    "active_sessions": 0,
    "uptime": 10.899
  }
  ```

  This means the server has been spun up and can be used by the omi app. (Check Important Note for future fix of this issue)

7. Once the homepage loads you can close it and use the recording feature of the app or device.

8. As you record you can see notifications created based on your conversations. The notifications are also stored in the chat page (You cannot interact with it in chat yet, go to future work to see the implementation path of adding this feature).

9. Play with it as much as you want, though api cost would be rate limited soon to prevent over use.

Future work is still ongoing to test and make sure the app comes out really good, and ultimately to ensure it is merged with omi as a core app.

## FUTURE WORK

- [] Chat Continuity: Talk to mentor in an isolated environment about problems based on the topic mentor gathers from your conversations in realtime.

- [] Store mentor advice and conversation in a secure database to be used for context and future references where necessary.

- [] Build the homepage for the mentor app and host it for first time users of the app to see with setup instructions.

- [] Build tests for the app using github actions or something else later.

- [] I will add chat feature for the app as well in omi (in the omi app)

- [] Change hosting service to amazon ec2 instead of render to get rid of server inactivity when spun down.

- [] Look for api_base_url and api_key_notification for the app and put them inside env with codebase (question on the discord channel can be asked)

- [] Create cron job to send notification from mentor to user from time to time (basically creating reminder)

- [] Implement rate limiter and implement feature to ensure the api isnt used for every little thing.
