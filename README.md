# ForwartMessagesApi
Sends messages into telegram after POST request to /{endpoint-name} endpoint, with ability to block ip

# Get started
1. cp .env.sample .env
2. edit .env with your args
3. docker-compose up -d
4. enjoy!

```
host: localhost:5000/{endpoint-name}
method: POST
args:
  - body: message (string)
```
