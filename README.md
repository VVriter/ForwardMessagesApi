1. cp .env.sample .env
2. edit .env with your args
3. docker-compose up -d
4. enjoy!

```
host: localhost:5000/send
method: POST
args:
  - body: message (string)
```
