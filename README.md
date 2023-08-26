# gandalf-v2
Gandalf V2 project which remakes the Gandalf game (by [Lakera.ai](http://gandalf.lakera.ai)) so I could practice my full-stack + AI tools.
Has support for multiple characters/storylines. Has basic level progression, with increasing difficulty

The project is available here: http://gandalf-v2-cae5533834d4.herokuapp.com

## Video Demo
https://github.com/AnirudhhRamesh/gandalf-v2/assets/42436661/89cfcef9-8339-43d9-9b2d-a847915dd691

How I created the project, step-by-step:

### Research and Brainstorming
- Trying out [Gandalf](http://gandalf.lakera.ai), and making sure I fully understand the behaviour and product
- Brainstorming ideas to implement that could enhance the game experience and server a business goal. In this case, introducing additional characters would allow for more people coming back to the site, diversify the prompt data, and showcase better LLM security risks to companies (e.g. Tim Cook iGPT character).

### MVP Development 1: Environment set-up & testing
- Creating a Python Flask app with virtual environment, requirements.txt and .env for API keys.
- Connecting to OpenAI API to test out the behaviour

### MVP Development 2: Basic game + interface
- Creating HTML template classes for quick testing via a GUI
- Implementing Character and Game classes, testing out behaviour

### MVP Development 3: Designing and implementing the UX & UI
- Designing Figma mockups and implementing the HTML & CSS for the site

### Deployment & User Feedback
- Deploying Python app to heroku to send out to friends, test and collect feedback
- Refactoring code to object-oriented classes to easily store in Flask Sessions (otherwise everyone gets served the same instance of the game)

### Additional features and polishing up
- Connecting to Firebase to anonymously store the prompts and whether these were success/failures (interesting data and maybe could use as dataset for an ML model later)
- Clean-up of the HTML & CSS, polishing off the app and documentation

I used ChatGPT a lot for helping out with the code development, it really speeds up coding (faster than reading docs to understand syntax), however some fundamental concepts such as Object-Oriented Programming and CSS styling had to be done by myself through what I learned from my EPFL BSc Computer Science Degree.

## Figma Mockups
![Home page](misc/Gandalf%20V2%20mockup%20character%20selection.png)

![Game page](misc/Gandalf%20V2%20mockup%20game%20selection.png)

Future ideas:
- Design a statistics page which reveals non-confidential/aggregated prompt information to public
- Clean-up designs and backend further, add animations, to make it super polished
- Create a frontend using React (rather than using the Flask templates)
