# TODO service

This service allows you to efficiently manage todo tasks across two different regions. You can share tasks with your team members to improve collaboration and productivity.

## Installation
In order to run your service you need to run:

python -m {TODO_service path} --primary {The DB ip of your region} --secondary {The DB ip of your team member region}

Once your done your service is up and ready to go.


## Technical choices
DB - I spent a lot of time thinking about which DB would be the right choice for my project. I needed a database that was fast and efficient, and initially I chose Redis. However, I soon realized that it would make the table connections very complicated, and it's an in-memory database, which meant that I couldn't ensure consistency of my data. After some research, I found that MongoDB is also very fast and is a NoSQL database, which is much easier to use. I also looked into MongoDB's built-in replication feature to make the connection between the two databases more effective. However, this feature acts like a master and slave, and I needed a master and master setup, so I didn't find it very attractive for my project. I know there must be a better way to connect between th DB but i didnt found it yet.

## my design
i decided to create my tasks with the parameters:

- headline 
- description
- creation_time
- task_id 
Every task obviously needs a headline and a description.

The creation time is there to make the user's life easier. I wanted them to be able to see when they created the task, just in case there are a lot of tasks with the same headline.

The task ID is used to delete tasks. In MongoDB, every new document is created with a unique ID, but I knew that I have two databases to update. So, in order to give them the same ID, I created a unique one that will be the same in both databases


## Trade offs
The project got me thinking about alot of ways to execute my code. some of those things:

Frontend - The FastApi docs is very comftorble, but I experienced some limitations with it. For example, I found it difficult to delete a task in a user-friendly way. With HTML, I could have used buttons to make it more intuitive. The current method requires the user to enter the task ID, which may not be ideal for all users. I have also created a few HTML files that could improve the user experience.

 Features I would have liked to add:

- Task editing
- Handling all kinds of exceptions
- Task deletion by name
- Adding user name to every task
- Filtering tasks by a certain user
- Task status (completed/in progress/canceled...)
- change the way both DB's sync.



