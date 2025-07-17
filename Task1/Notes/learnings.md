# My leanings from the further reading section

## Readme Driven Development
- Not mindless jumping towards coding, first verbalize your thoughts then codify it.

## 12 Factor App

- CDC BB PP CDD LA

1. Codebase : 1 and version tracked
2. Dependencies : all explicitly specified
3. Config : store in env variables

4. Backing Sevices : treat services like db's, queues as attached resources (eg swap local and aws without any code changes)
5. Build Release Run : separate 3 stages ( enable repeatable deployments and rollbacks)

6. Processes : run app as one or more stateless process (to enable horizontal scaling and fault tolerance) i.e do not create any in memory stuff
7. Port Binding : export services (self contained apps)

8. Concurrency : scale out via process model (workers, queues)
9. Disposability : fast startup and graceful shutdown
10. Dev/Prod Parity : keep dev/prod as similar as possible

11. Logs : treat logs as event streams and not files (so that they are captured by the host machine) Every print statement and sys.stderr caught
12. Admin Processes : as one-off task

## Best practice for rest api-design
- nouns not verbs /users
- correct methods
- version it
- secure it (use auth)
- paginate results
- standard responses (proper status codes)
- document it

### Threads, Async and multiple worker nodes

* async is when a process that is occupying some time wont stop the cpu from doing the other tasks
* thread is when there is fast context switching and so it appears that it multiple processes are running, but its just 1 but multiple hat switching
* multiple worker nodes are like different linux processes
* concurrency multiple tasks in progress at same time, not necessarily same moment(async and threads)
* parallelism multiple tasks actually executing at the same time. (gunicorn)