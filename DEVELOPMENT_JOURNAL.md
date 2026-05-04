# Development Journal

1. I am building out the primary infrastructure first, and then moving into developing the application. This way once I get started with building the app, I can focus on getting the logic built out without worrying about the deployment/publish section to reduce mental load/stress as the deadline approaches.

2. Now that I've finished building out most of the infrastructure i.e the docker compose, and I've tested the docker system to ensure data is persistent and seeded correctly. I have also created groups, and 3 test accounts one for each user group - `customer`, `agent`, `admin`. I will move on to building out the models

3. I have successfully created the inital Complain Models. However, as I am reading and re-reading the project documentation, I noticed the `Seeded Data Requirements` requires customer account to have `service plans` which wasn't noted under the `Module 1` section.

4. I am implementing the `Business Logic` section for `Module 1`. Once the Business Logic is completed, I will build out a simple UI using bootstrap.

5. I implemented a huge portion of the bootstrap 5 theme. I am now cleaning up the random bugs here and there. Once this is clear, I will once over the business logic (as there is a few things here and there) and then I'll start working on `Module 2`.

6. With a Basic UI built out, I am going to clear up the little bugs in and around the application. However, I need to redo the namespaces.

7. Opted not to redo the namespaces and instead made it a bit clearer what I meant.

8. Okay built out the UI, I just have to create some seed data.

9. Seed script has been created. There are a few calculations bugs on the dashboard, and Agent is currently redirecting to the summary page which they should not. Will be working on the chatbot section once the agent thing is cleared.

10. I have started working on the chatbot section, so that at the very least if I cannot complete it, I can get 80% of the way there. The Chatbot will Use the Grok LLM to get the intent of the natural request, convert it to an ORM representation, execute that against the database, and then use grok to format the returning data into a natural response.

11. I attempted to turn it into a more of an automatic thing, however, as I was building it out, it appears to require a bit too much fine tuning, with many edge cases, so I will just be feeding the user's context data to groq. The correct thing to do is to make groq/llm treat the application as a MCP type thing.

12. I have done all that was requested. What couldn't have been done within the timeframe (such as building out all the requiste filters for all the models - I built out the framework so extending it shouldn't be a problem), does have logic setup to make the continuing development much cleaner.

## AI usage

1. In following several pieces of documentations and tutorials, I mistakenly introduced a health check bug, however I didn't realize this, and as a result I threw the .env, and the db section of the compose.yml file into chatgpt, where it determined the health check was looking for defaults and not using the correct env variable.

2. Used ChatGPT to figure out how to run a shell script in a Docker Command. See `django-seed-db` section of the `compose.yml`. My original attempts failed a few times. Explictly asked how to run shell scripts in docker command.

3. Used ChatGPT to figure out how to apply User Profile to only the Customer group user account, by providing it the default code from the Django Tutorial Page.

4. Used ChatGPT to generate the form based on the model, then manually cut it down and modified the code for the UI.

5. Prompted ChatGPT, asking what was the best way to handle the roles and permissions given the limited scope.

6. Prompted ChatGPT asking how to use a seperate button to escalate the complain while adding a note, I extracted the action == "esclate" section under form.is_valid();

7. Prompted ChatGPT, by giving it the debug errors that Django threw while I attempted to debug why `crispy` wasn't rendering or loading as I expected it to.

8. Prompted ChatGPT, to build out the table css styles using my inital basic ul/li items and the model sheet from `models.py`. Also did the same for the Detail Page to make it slightly prettier.

9. Prompted ChatGPT with my incorrect totals by category logic, and it returned the 'corrected' function calls. See `summary/views.py`

10. Prompted ChatGPT to render out a proper ui/drop-down for the details view based on the existing code base I implemented under `DetailView > get_context_data()`.

11. Prompted ChatGPT to help me migrate from using fixtures to a script, since the fixtures had begun unruly and causing issues.

12. Prompted ChatGPT with the model.py file so that I can get the json context file for GROQ.

13. Had a lot of trouble integrating GROQ, I had to fight with Tools, intents, formatting etc. As a result I had a lot of errors back and forth with ChatGPT to solve them.

## Development

Durning development you might want to update the container/.env files. Use the following command to remove the docker container.

```bash
docker compose down -v
```

Building and launch the docker container using:

```bash
docker compose up --build
```

### Pip/Requirements

When you add new packages that are needed for the application to run, use the following script to generate the `requirments.txt` file. This command must be run from inside the `cfms/` folder.

```bash
pip freeze > requirements.txt 
```

### Generating Data for seeding back

Go into your running docker container (`django-docker`) and exec the following script

```bash
python manage.py dumpdata <your_app_name> --indent 2
```

### Generating Migrations

```bash
python manage.py makemigrations <app_name>
```