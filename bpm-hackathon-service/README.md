# BPM Hackathoon 2019
## Team Service #1
Repository for a service team

## Postgres
- user/password/database: `camunda`

## Mountebank
- Dockerfile used from https://github.com/andyrbell/mountebank/blob/master/Dockerfile
- Configure imposters in `docker/mountebank/imposters/impossters.ejs`
- Go to http://localhost:2525 to see Mountebank's configuration 

## Run the container
- go to folder bpm-hackathon-service
- run `docker-compose up`