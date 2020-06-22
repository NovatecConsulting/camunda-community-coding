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

from ask_sdk_model.dialog import ElicitSlotDirective

from datetime import date

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


camunda_url = "https://dcd56278b9d2.ngrok.io"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "hallo. ich bin dein virtueller assistent rund um kennzahlen. was möchtest du wissen?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class UebersichtIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("UebersichtIntent")(handler_input)
    def handle(self, handler_input):
        try:
            amount_open_tasks = requests.get(f'{camunda_url}/rest/task/count').json()["count"]
            amount_process_instances = requests.get(f'{camunda_url}/rest/process-instance/count').json()["count"]
            speak_output = f'momentan gibt es {amount_open_tasks} offene aufgaben und {amount_process_instances} laufende prozesse.'
            if (amount_open_tasks == 1):
                speak_output = f'momentan gibt es eine offene aufgabe und {amount_process_instances} laufende prozesse.'
            if (amount_process_instances == 1):
                speak_output = f'momentan gibt es {amount_open_tasks} offene aufgaben und einen laufenden prozess.'
            if (amount_open_tasks == 1 and amount_process_instances == 1):
                speak_output = f'momentan gibt es eine offene aufgabe und einen laufenden prozess.'
        except:
            speak_output = 'die anfrage konnte nicht bearbeitet werden. versuches es später erneut.'
        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            .response
        )


class OffeneTasksGruppeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("OffeneTasksGruppeIntent")(handler_input)
    def handle(self, handler_input):
        try:
            gruppe = ask_utils.request_util.get_slot(handler_input, "gruppe").to_dict()['resolutions']['resolutions_per_authority'][0]['values'][0]['value']['name']
            if (gruppe != "kitchen" or gruppe != "service"):
                count_open_tasks = requests.get(f'{camunda_url}/rest/task/count?candidateGroup={gruppe}').json()["count"]
                if (gruppe == "kitchen"):
                    gruppe = "küche"
                if (count_open_tasks == 1):
                    speak_output = f'{gruppe} hat {count_open_tasks} aufgabe.'
                else:
                    speak_output = f'{gruppe} hat {count_open_tasks} aufgaben.'
                return (
                    handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(False)
                    .response
                )
            else:
                return (
                    handler_input.response_builder
                    .speak(f"die gruppe {gruppe} kenne ich nicht. welche gruppe meinst du?")
                    .ask("welche gruppe meinst du?")
                    .add_directive(ElicitSlotDirective(slot_to_elicit="gruppe"))
                    .response)
        except:
            speak_output = 'die anfrage konnte nicht bearbeitet werden. versuche es später erneut.'
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
            )


class AnzahlInstanzenHeuteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AnzahlInstanzenHeuteIntent")(handler_input)
    def handle(self, handler_input):
        try:
            prozess = ask_utils.request_util.get_slot(handler_input, "prozess").to_dict()['resolutions']['resolutions_per_authority'][0]['values'][0]['value']['name']
            today = str(date.today()) + "T00:00:00.000%2B0200"
            if prozess == "zimmerservice":
                count_running_instances = requests.get(f'{camunda_url}/rest/history/process-instance/count?processDefinitionName={prozess}&startedAfter={today}').json()["count"]
                speak_output = f'der zimmerservice wurde heute {count_running_instances} mal gerufen.'
                return (
                    handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(False)
                    .response
                )
            else:
                return (
                    handler_input.response_builder
                    .speak(f'den prozess {prozess} kenne ich nicht. welchen prozess meinst du?')
                    .ask("welchen prozess meinst du?")
                    .add_directive(ElicitSlotDirective(slot_to_elicit="prozess"))
                    .response)
        except:
            speak_output = 'die anfrage konnte nicht bearbeitet werden. versuche es später erneut.'
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
            )


class OffeneTasksProzessIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("OffeneTasksProzessIntent")(handler_input)
    def handle(self, handler_input):
        try:
            prozess = ask_utils.request_util.get_slot(handler_input, "prozess").to_dict()['resolutions']['resolutions_per_authority'][0]['values'][0]['value']['name']
            if (prozess == "zimmerservice"):
                count_open_tasks = requests.get(f'{camunda_url}/rest/task/count?processDefinitionName=zimmerservice').json()["count"]
                if (count_open_tasks == 1):
                    speak_output = f'Beim Zimmerservice gibt es aktuell {count_open_tasks} aufgabe.'
                else:
                    speak_output = f'Beim Zimmerservice gibt es aktuell {count_open_tasks} aufgaben.'
                return (
                    handler_input.response_builder
                    .speak(speak_output)
                    .set_should_end_session(False)
                    .response
                )
            else:
                return (
                    handler_input.response_builder
                    .speak(f"den prozess {prozess} kenne ich nicht. welchen prozess meinst du?")
                    .ask("welchen prozess meinst du?")
                    .add_directive(ElicitSlotDirective(slot_to_elicit="prozess"))
                    .response)
        except:
            speak_output = 'die anfrage konnte nicht bearbeitet werden. versuche es später erneut.'
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(False)
                .response
            )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "du kannst dir einen überblick geben lassen oder nach speziellen kennzahlen fragen. was möchtest du wissen?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "bis bald!!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "das habe ich nicht verstanden. könntest du das bitte wiederholen?"

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
sb.add_request_handler(UebersichtIntentHandler())
sb.add_request_handler(OffeneTasksGruppeIntentHandler())
sb.add_request_handler(AnzahlInstanzenHeuteIntentHandler())
sb.add_request_handler(OffeneTasksProzessIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
