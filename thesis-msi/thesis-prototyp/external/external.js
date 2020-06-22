const felixSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}
const annaSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}
const julianSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}

const { Client, logger } = require('camunda-external-task-client-js');
const request = require('request')
// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
//  - 'asyncResponseTimeout': long polling timeout (then a new request will be issued)
const config = { baseUrl: 'http://localhost:8080/rest', use: logger, asyncResponseTimeout: 10000 };

// create a Client instance with custom configuration
const client = new Client(config);

function sendNotification(secrets, id, message) {
    const optionsToken = {
        'method': 'POST',
        'url': 'https://api.amazon.com/auth/o2/token',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'grant_type': 'client_credentials',
            'client_id': secrets.client_id,
            'client_secret': secrets.client_secret,
            'scope': 'alexa::proactive_events'
        }
    }
    console.log("REQUESTING TOKEN")
    request(optionsToken, function (error, response) {
        if (error) throw new Error(error);
        console.log("GOT TOKEN")
        res = JSON.parse(response.body)
        token = res.access_token
        const expTime = new Date()
        expTime.setHours(expTime.getHours() + 2) //expires after two hours
        const reqbody = {
            "timestamp": new Date().toISOString(),
            "referenceId": id,
            "expiryTime": expTime.toISOString(),
            "event": {
                "name": "AMAZON.MessageAlert.Activated",
                "payload": {
                    "state": {
                        "status": "UNREAD"
                    },
                    "messageGroup": {
                        "creator": {
                            "name": "Camunda: " + message
                        },
                        "count": 1
                    }
                }
            },
            "relevantAudience": {
                "type": "Multicast",
                "payload": {}
            }
        }
        const options = {
            'method': 'POST',
            'url': 'https://api.eu.amazonalexa.com/v1/proactiveEvents/stages/development',
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(reqbody)
        }
        request(options, function (error, response) {
            //if (error) throw new Error(error);
            if (error) console.log(error);
            if (response.statusCode == 202) {
                console.log(`NOTIFICATION "${message}" SENT`)
            } else {
                console.log(`NOTIFICATION "${message}" COULD NOT BE SENT`)
            }
        });
    })
}


// "service-wagen vorbereiten"
client.subscribe('service-1', async function ({ task, taskService }) {
    sendNotification(felixSkillSecret, "new-task", "eine neue aufgabe ist verfügbar: service-wagen vorbereiten.")
    sendNotification(annaSkillSecret, "new-task", "eine neue aufgabe ist verfügbar: service-wagen vorbereiten.")
    await taskService.complete(task);
});

// "bestellung servieren"
client.subscribe('service-2', async function ({ task, taskService }) {
    sendNotification(felixSkillSecret, "new-task", "eine neue aufgabe ist verfügbar: bestellung servieren")
    sendNotification(annaSkillSecret, "new-task", "eine neue aufgabe ist verfügbar: bestellung servieren")
    await taskService.complete(task);
});

// "bestellung zubereiten"
client.subscribe('kitchen-1', async function ({ task, taskService }) {
    sendNotification(julianSkillSecret, "new-task", "eine neue aufgabe ist verfügbar: bestellung zubereiten")
    await taskService.complete(task);
});

// "auf rechnung setzen"
client.subscribe('rechnung', async function ({ task, taskService }) {
    console.log("MOCK SERVICE - REQUESTING VARIABLES")
    allVariables = task.variables.getAll()
    console.log("GOT VARIABLES: ", allVariables)
    console.log("MOCK SERVICE - COMPLETE TASK")
    await taskService.complete(task);
});