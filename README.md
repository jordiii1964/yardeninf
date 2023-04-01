# TODO service

This service allows you to efficiently manage todo tasks across two different regions. You can share tasks with your team members to improve collaboration and productivity.

## Installation
In order to run your service you need to run:

python {TODO_service} --primary {main DB server of the region your in} --secondary {the DB ip in the other region}

Once your done your service is up and ready to go.


## Technical choices
DB - I spent a lot of time thinking about which DB would be the right choice for my project. I needed a database that was fast and efficient, and initially I chose Redis. However, I soon realized that it would make the table connections very complicated, and it's an in-memory database, which meant that I couldn't ensure consistency of my data. After some research, I found that MongoDB is also very fast and is a NoSQL database, which is much easier to use. I also looked into MongoDB's built-in replication feature to make the connection between the two databases more effective. However, this feature acts like a master and slave, whereas I needed a master and master setup, so I didn't find it very attractive for my project.

## Trade offs
The project got me thinking about alot of ways to execute my code. some of those things:

Frontend - The FastApi docs is very comftorble, but I experienced some limitations with it. For example, I found it difficult to delete a task in a user-friendly way. With HTML, I could have used buttons to make it more intuitive. The current method requires the user to enter the task ID, which may not be ideal for all users. I have also created a few HTML files that could improve the user experience.

 Features I would have liked to add:

- Task editing
- Handling all kinds of errors
- Task deletion by name
- Adding user names to every task
- Filtering tasks by a certain user
- Task status (completed/in progress/canceled...)


