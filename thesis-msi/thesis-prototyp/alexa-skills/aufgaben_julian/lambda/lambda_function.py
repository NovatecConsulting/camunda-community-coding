# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_model.dialog import ElicitSlotDirective, ConfirmIntentDirective, ConfirmSlotDirective
from ask_sdk_model import (
    Intent, IntentConfirmationStatus, Slot, SlotConfirmationStatus)
from ask_sdk_model.dialog_state import DialogState

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

camunda_url = "https://dcd56278b9d2.ngrok.io"
current_user = "julian"
current_group = "kitchen"
current_task = None


def get_current_task(assignee):
    """Holt alle Aufgaben, die dem assignee zugewiesen sind.
    Sind keine da oder geht etwas schief, wird der aktuelle Task auf NONE gesetzt."""
    global current_task
    try:
        current_task = None
        alle_meine_tasks_request = requests.get(
            f"{camunda_url}/rest/task?assignee={assignee}&sortBy=created&sortOrder=asc")
        if alle_meine_tasks_request.status_code == 200:
            alle_meine_tasks = alle_meine_tasks_request.json()
            if len(alle_meine_tasks) != 0:
                current_task = alle_meine_tasks[0]
    except:
        logger.info("get_current_task(assignee): request failed")


def claim_new_task(candidateGroup, assignee):
    """Die älteste, verfügbare Aufgabe der candidateGroup wird dem assignee zugewiesen."""
    try:
        alle_service_tasks_request = requests.get(
            f"{camunda_url}/rest/task?candidateGroup={candidateGroup}&unassigned=true&sortBy=created&sortOrder=asc")
        if alle_service_tasks_request.status_code == 200:
            alle_service_tasks = alle_service_tasks_request.json()
            if len(alle_service_tasks) > 0:
                oldest_task_id = alle_service_tasks[0]['id']
                requests.post(
                    f"{camunda_url}/rest/task/{oldest_task_id}/assignee", json={"userId": assignee})
            get_current_task(assignee)
    except:
        logger.info("claim_new_Task(candidateGroup, assignee): request failed")


def complete_task_failed(handler_input):
    """Wenn das Abschließen einer Aufgabe fehlschlägt"""
    return (
        handler_input.response_builder
        .speak("ich konnte deine aufgabe leider nicht abschließen.")
        .set_should_end_session(False)
        .response
    )


def no_task_assigned(handler_input):
    """Wenn dem Nutzer noch keine Aufgabe zugewiesen ist, er aber mit ihr interagieren möchte"""
    return (
        handler_input.response_builder
        .speak("frage mich zuerst, was deine aufgabe ist.")
        .set_should_end_session(False)
        .response
    )


def no_or_new_task():
    """Standard Prozedur nach dem Abschließen einer Aufgabe"""
    get_current_task(assignee=current_user)

    if current_task is None:
        claim_new_task(candidateGroup=current_group, assignee=current_user)

    if current_task is None:
        return "ich habe deine aufgabe abgeschlossen. aktuell gibt es keine weiteren verfügbaren aufgaben."
    else:
        return f"ich habe deine aufgabe abgeschlossen. deine neue aufgabe ist: {current_task['name']}. {current_task['description']}"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler für den Start des Skills. Wird bei jedem Start des Skills aufgerufen."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = f"hallo {current_user}! ich bin dein virtueller assistent und helfe dir mit allem rund um deine aufgaben. was möchtest du tun?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class AufgabeDetailsIntentHandler(AbstractRequestHandler):
    """Handler für Aufgabendetails. Gibt, wenn vorhanden, die Details zur Aufgabe zurück"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeDetailsIntent")(handler_input)

    def handle(self, handler_input):
        get_current_task(assignee=current_user)

        if current_task is None:
            claim_new_task(candidateGroup=current_group, assignee=current_user)

        if current_task is None:
            speak_output = "aktuell gibt es keine verfügbaren aufgaben."
        else:
            speak_output = f"deine aufgabe ist: {current_task['name']}. {current_task['description']}"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Generischer Abschluss
class AufgabeAbschlussIntentHandler(AbstractRequestHandler):
    """Handler für Abschluss von Aufgaben. Generischer Abschluss von Aufgaben hier möglich. 
    Jeder Aufgabentyp des Prozesses kann hiermit abgeschlossen werden.
    Angepasste Logik für den Abschluss von "zahlungsart bestimmen"."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeAbschlussIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] != "bestellung servieren":
            try:
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/complete", json={})
                if r.status_code != 204:
                    logger.info(
                        f"{current_task['name']}, Error bei Complete-Request")
                    raise Exception("Post failed")
            except:
                return complete_task_failed(handler_input)
        else:
            slot_confirmation_status = handler_input.request_envelope.to_dict(
            )['request']['intent']['slots']['direkt']['confirmation_status']
            if slot_confirmation_status == "NONE":
                speak_output = "hat der gast direkt bezahlt?"
                directive = ConfirmSlotDirective(
                    updated_intent=Intent(
                        name="AufgabeAbschlussIntent",
                        slots={
                            "direkt": Slot(
                                name="direkt",
                                value="true")
                        }),
                    slot_to_confirm="direkt")
                return (
                    handler_input.response_builder
                    .add_directive(directive)
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
                )
            else:
                request_body = {
                    "variables": {
                        "direkt": {
                            "type": "boolean",
                            "value": "true"
                        }
                    }
                }
                if slot_confirmation_status == "DENIED":
                    request_body['variables']['direkt']['value'] = "false"

                try:
                    r = requests.post(
                        f"{camunda_url}/rest/task/{current_task['id']}/complete", json=request_body)
                    if r.status_code != 204:
                        logger.info(
                            f"{current_task['name']}, Error bei Complete-Request")
                        raise Exception("Post failed")
                except:
                    return complete_task_failed(handler_input)

        speak_output = no_or_new_task()

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Angepasster Abschluss
class WagenVorbereitenIntentHandler(AbstractRequestHandler):
    """An den Task "service-wagen vorbereiten" angepasster Handler.
    Anpassung des Interaktionsmodells an den Use Case."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("WagenVorbereitenIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] == "service-wagen vorbereiten":
            try:
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/complete", json={})
                if r.status_code != 204:
                    logger.info(
                        f"{current_task['name']}, Error bei Complete-Request")
                    raise Exception("Post failed")
                speak_output = no_or_new_task()
            except:
                return complete_task_failed(handler_input)
        else:
            speak_output = "das ist nicht deine aufgabe."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Angepasster Abschluss
class ServierenIntentHandler(AbstractRequestHandler):
    """An den Task "bestellung servieren" angepasster Handler.
    Anpassung des Interaktionsmodells an den Use Case."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ServierenIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] == "bestellung servieren":
            slot_confirmation_status = handler_input.request_envelope.to_dict(
            )['request']['intent']['slots']['direkt']['confirmation_status']
            if slot_confirmation_status == "NONE":
                speak_output = "hat der gast direkt bezahlt?"
                directive = ConfirmSlotDirective(
                    updated_intent=Intent(
                        name="AufgabeAbschlussIntent",
                        slots={
                            "direkt": Slot(
                                name="direkt",
                                value="true")
                        }),
                    slot_to_confirm="direkt")
                return (
                    handler_input.response_builder
                    .add_directive(directive)
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
                )
            else:
                request_body = {
                    "variables": {
                        "direkt": {
                            "type": "boolean",
                            "value": "true"
                        }
                    }
                }
                if slot_confirmation_status == "DENIED":
                    request_body['variables']['direkt']['value'] = "false"

                try:
                    r = requests.post(
                        f"{camunda_url}/rest/task/{current_task['id']}/complete", json=request_body)
                    if r.status_code != 204:
                        logger.info(
                            f"{current_task['name']}, Error bei Complete-Request")
                        raise Exception("Post failed")
                    speak_output = no_or_new_task()
                except:
                    return complete_task_failed(handler_input)
        else:
            speak_output = "das ist nicht deine aufgabe."
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Angepasster Abschluss
class ZahlungSofortIntentHandler(AbstractRequestHandler):
    """Aufgabe "zahlungsart bestimmen", Gast zahlt sofort.
    Anpassung des Interaktionsmodells an den Use Case."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ZahlungSofortIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] == "bestellung servieren":
            try:
                request_body = {
                    "variables": {
                        "direkt": {
                            "type": "boolean",
                            "value": "true"
                        }
                    }
                }
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/complete", json=request_body)
                if r.status_code != 204:
                    logger.info(
                        f"{current_task['name']}, Error bei Complete-Request")
                    raise Exception("Post failed")
                speak_output = no_or_new_task()
            except:
                return complete_task_failed(handler_input)
        else:
            speak_output = "das ist nicht deine aufgabe."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Angepasster Abschluss
class ZahlungSpaeterIntentHandler(AbstractRequestHandler):
    """Aufgabe "zahlungsart bestimmen", Gast zahlt später.
    Anpassung des Interaktionsmodells an den Use Case."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ZahlungSpaeterIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] == "bestellung servieren":
            try:
                request_body = {
                    "variables": {
                        "direkt": {
                            "type": "boolean",
                            "value": "false"
                        }
                    }
                }
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/complete", json=request_body)
                if r.status_code != 204:
                    logger.info(
                        f"{current_task['name']}, Error bei Complete-Request")
                    raise Exception("Post failed")
                speak_output = no_or_new_task()
            except:
                return complete_task_failed(handler_input)
        else:
            speak_output = "das ist nicht deine aufgabe."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


# Angepasster Abschluss
class BestellungZubereitenIntentHandler(AbstractRequestHandler):
    """An den Task "bestellung-zubereiten" angepasster Handler.
    Anpassung des Interaktionsmodells an den Use Case."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BestellungZubereitenIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        if current_task['name'] == "bestellung zubereiten":
            try:
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/complete", json={})
                if r.status_code != 204:
                    logger.info(
                        f"{current_task['name']}, Error bei Complete-Request")
                    raise Exception("Post failed")
                speak_output = no_or_new_task()
            except:
                return complete_task_failed(handler_input)
        else:
            speak_output = "das ist nicht deine aufgabe."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


class AufgabeVorIntentHandler(AbstractRequestHandler):
    """Aufgabe überspringen. Generischer Handler.
    Alle Aufgaben lassen sich damit überspringen.
    Entweder die nächste, zugewiesene aufgabe wird zugewiesen oder die neuere aufgabe, die dem nutzer bereits zugewiesen wurde, wird ausgegeben."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeVorIntent")(handler_input)

    def handle(self, handler_input):
        global current_task

        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        try:
            alle_meine_tasks_request = requests.get(
                f"{camunda_url}/rest/task?assignee={current_user}&sortBy=created&sortOrder=asc")
            if alle_meine_tasks_request.status_code != 200:
                raise Exception("Request failed")
            alle_meine_tasks = alle_meine_tasks_request.json()
            if len(alle_meine_tasks) > 1:
                next_task_index = alle_meine_tasks.index(current_task) + 1
                if next_task_index > (len(alle_meine_tasks) - 1):
                    return (
                        handler_input.response_builder
                        .speak(f"es gibt keine neuere aufgabe. deine aufgabe ist weiterhin: {current_task['name']}. {current_task['description']}")
                        .set_should_end_session(False)
                        .response)
                # unclaim, egal bei fail
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/unclaim", json={})
                if r.status_code != 204:
                    raise Exception("Unable to unclaim current task")

                current_task = alle_meine_tasks[next_task_index]
                return (
                    handler_input.response_builder
                    .speak(f"ich habe deine aufgabe übersprungen. deine neue aufgabe ist: {current_task['name']}. {current_task['description']}")
                    .set_should_end_session(False)
                    .response)
            else:
                date = current_task['created']
                date = date.replace("+", "%2B")

                newer_unassigend_service_tasks_request = requests.get(
                    f"{camunda_url}/rest/task?candidateGroup={current_group}&unassigned=true&createdAfter={date}&sortBy=created&sortOrder=asc")
                if newer_unassigend_service_tasks_request.status_code != 200:
                    raise Exception("Request failed")
                if len(newer_unassigend_service_tasks_request.json()) > 0:
                    new_task = newer_unassigend_service_tasks_request.json()[0]
                    r = requests.post(
                        f"{camunda_url}/rest/task/{new_task['id']}/assignee", json={"userId": current_user})
                    if r.status_code != 204:
                        raise Exception("Unable to assign new task")

                    # unclaim, egal bei fail
                    r = requests.post(
                        f"{camunda_url}/rest/task/{current_task['id']}/unclaim", json={})
                    if r.status_code != 204:
                        raise Exception("Unable to unclaim current taks")

                    get_current_task(assignee=current_user)
                    speak_output = f"ich habe deine aufgabe übersprungen. deine neue aufgabe ist: {current_task['name']}. {current_task['description']}"
                else:
                    speak_output = f"es gibt keine neuere aufgabe. deine aufgabe ist weiterhin: {current_task['name']}. {current_task['description']}"
                return (
                    handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(False)
                    .response)
        except:
            logger.info("Unable to get new task")
            return (
                handler_input.response_builder
                .speak(f"ich konnte dir keine neue aufgabe zuweisen. deine aufgabe ist weiterhin: {current_task['name']}. {current_task['description']}")
                .set_should_end_session(False)
                .response)


class AufgabeZurueckIntentHandler(AbstractRequestHandler):
    """Aufgabe zurück, wird nach einem überspringen aufgerufen.
    Funktioniert allerdings nicht in jedem Fall. Bspw. wenn eine viel aktuellere aufgabe zuvor zugewiesen wurde.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeZurueckIntent")(handler_input)

    def handle(self, handler_input):
        if current_task is None:
            get_current_task(assignee=current_user)

        if current_task is None:
            return no_task_assigned(handler_input)

        try:
            date = current_task['created']
            date = date.replace("+", "%2B")

            older_unassigned_service_tasks_request = requests.get(
                f'{camunda_url}/rest/task?candidateGroup={current_group}&unassigned=true&createdBefore={date}&sortBy=created&sortOrder=asc')
            if older_unassigned_service_tasks_request.status_code != 200:
                raise Exception("Request failed")
            logger.info(older_unassigned_service_tasks_request.json())
            len_list = len(older_unassigned_service_tasks_request.json())
            logger.info(len_list)
            if len_list > 0:
                new_task = older_unassigned_service_tasks_request.json()[
                    len_list - 1]
                r = requests.post(
                    f"{camunda_url}/rest/task/{new_task['id']}/assignee", json={"userId": current_user})
                if r.status_code != 204:
                    raise Exception("Unable to assign new task")

                # unclaim, egal bei fail
                r = requests.post(
                    f"{camunda_url}/rest/task/{current_task['id']}/unclaim", json={})
                if r.status_code != 204:
                    raise Exception("Unable to unclaim current taks")
                get_current_task(assignee=current_user)
                speak_output = f"okay. deine aufgabe ist: {current_task['name']}. {current_task['description']}"
            else:
                speak_output = f"es gibt keine freie ältere aufgabe. deine aufgabe ist weiterhin: {current_task['name']}. {current_task['description']}"
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response)
        except:
            logger.info("Unable to get old task")
            return (
                handler_input.response_builder
                .speak(f"ich konnte dir die aufgabe nicht zuweisen. deine aufgabe ist weiterhin: {current_task['name']}. {current_task['description']}")
                .set_should_end_session(False)
                .response)


class AufgabeFreigebenIntentHandler(AbstractRequestHandler):
    """Handler für Freigabe von Aufgaben.
    Generisch, geht mit jeder Aufgabe."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeFreigebenIntent")(handler_input)

    def handle(self, handler_input):
        get_current_task(assignee=current_user)

        try:
            # unclaim, wenn current_task == NOne, kein problem wegen try catch
            r = requests.post(
                f'{camunda_url}/rest/task/{current_task["id"]}/unclaim', json={})
            if r.status_code != 204:
                raise Exception("Unable to unclaim current task")
            speak_output = "ich habe deine aufgabe freigegeben."
        except:
            speak_output = "ich konnte deine aufgabe nicht freigeben."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response)


class AufgabeUebergabeIntentHandler(AbstractRequestHandler):
    """Handler für Übergeben von Aufgaben an andere Personen. An sich generisch, aber man muss die Personen angeben."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AufgabeUebergabeIntent")(handler_input)

    def handle(self, handler_input):
        get_current_task(assignee=current_user)
        person = ask_utils.request_util.get_slot_value(
            handler_input, "person")  # this slot is required!
        if (person != "julian" and person != "felix" and person != "anna"):
            return (
                handler_input.response_builder
                .add_directive(ElicitSlotDirective(slot_to_elicit="person"))
                .speak(f"{person} kenne ich nicht. du kannst die aufgabe an anna oder felix übergeben. an wen möchtest du die aufgabe übergeben?")
                .ask('an wen möchtest du die aufgabe übergeben?')
                .response)
        try:
            alle_person_tasks_request = requests.get(
                f'{camunda_url}/rest/task?assignee={person}&sortBy=created&sortOrder=asc')
            if alle_person_tasks_request.status_code != 200:
                raise Exception("Unable to retrieve tasks")
            alle_person_tasks = alle_person_tasks_request.json()
            if (len(alle_person_tasks) < 2):
                r = requests.post(f'{camunda_url}/rest/task/{current_task["id"]}/assignee', json={
                                  "userId": person})  # set assignee without checking
                if r.status_code != 204:
                    raise Exception("Unable to assign new task")
            else:
                raise Exception("Already two tasks assigned")

            get_current_task(assignee=current_user)

            if current_task is None:
                claim_new_task(candidateGroup=current_group,
                               assignee=current_user)

            if current_task is None:
                speak_output = f"ich habe deine aufgabe an {person} übergeben. aktuell gibt es keine weiteren verfügbaren aufgaben."
            else:
                speak_output = f"ich habe deine aufgabe an {person} übergeben. deine neue aufgabe lautet: {current_task['name']}. {current_task['description']}"
        except:
            speak_output = "ich konnte deine aufgabe nicht übergeben"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler für Hilfe."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "du kannst zum beispiel details zu deiner aufgabe erfragen, deine aufgabe abschließen, übergeben oder freigeben. was möchtest du tun?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Wenn der Nutzer Stopp/Abbruch sagt."""

    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "bis bald!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler für Ende der Session."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        global current_task
        current_task = None

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "das habe ich leider nicht verstanden. kannst du das bitte wiederholen?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AufgabeAbschlussIntentHandler())
sb.add_request_handler(WagenVorbereitenIntentHandler())
sb.add_request_handler(ZahlungSpaeterIntentHandler())
sb.add_request_handler(ZahlungSofortIntentHandler())
sb.add_request_handler(ServierenIntentHandler())
sb.add_request_handler(BestellungZubereitenIntentHandler())
sb.add_request_handler(AufgabeDetailsIntentHandler())
sb.add_request_handler(AufgabeVorIntentHandler())
sb.add_request_handler(AufgabeZurueckIntentHandler())
sb.add_request_handler(AufgabeFreigebenIntentHandler())
sb.add_request_handler(AufgabeUebergabeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
