# Telegram Bot for Finding a Specific Frame

For this project a Telegram Bot has been coded for predicting in which frame of a video a certain action occurs, through user input and a bisection algorithm. The frames of the whole video are obtained from The Frame X API.

> Bisection method is based on the fact that if f(x) is real and continuous function, and for two initial guesses x0 and x1 brackets the root such that: f(x0)f(x1) <0 then there exists at least one root between x0 and x1.

A user starts a new conversation with the bot and then the bot sends him one frame of the video and asks whether something has already happened or not, and this continues until the algorithm finds the frame in which the action takes place.

### Example on this repository:

There is a video of a rocket launch and we want to know at which frame exactly is the rocket launched. It will show different images to the user, asking if the rocket has taken off yet (which you can know by looking at the countdown on the top-right corner of the video). Based on the answers, it will find the first image where the rocket launches, helping to pinpoint its occurrence date. There are 61696 frames in the video but you can find the interesting frame in only 16 steps.

### How to use it with Docker:

1. Start a conversation with [@BotFather](https://t.me/botfather) on Telegram App.

2. Type the ***/newbot*** command to create a new bot. The BotFather will ask you for a name and username, then generate an authorization token for your new bot. 

3. Now that you have your token and bot, run the following commands:

   ```
   docker pull carlosjpv/bot-bisection:1.0.0
   ```

   ```
   docker run -e BOT_TOKEN=YOURTOKEN carlosjpv/bot-bisection:1.0.0
   ```

4. Open a new conversation with your bot and type the ***/start*** command to begin.
