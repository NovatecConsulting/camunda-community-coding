# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from ask_sdk_model.dialog import ElicitSlotDirective, ConfirmIntentDirective

import datetime
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


""" Globale Variablen für jede Session"""
camunda_url = "https://dcd56278b9d2.ngrok.io"
gericht = None
zimmernummer = None
getraenk = None


def bestellung_confirmed(handler_input):
    try:
        confirmation_status = handler_input.request_envelope.to_dict(
        )['request']['intent']['confirmation_status']
        return str(confirmation_status)
    except:
        return 'NONE'


class LaunchRequestHandler(AbstractRequestHandler):
    """Start des Skills"""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "hallo und herzlich willkommen beim zimmerservice! was möchtest du bestellen?"
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class BestellungIntentUnconfirmedHandler(AbstractRequestHandler):
    """Handler, um Bestellungen zu bearbeiten"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BestellungIntent")(handler_input) and bestellung_confirmed(handler_input) == "NONE"

    def handle(self, handler_input):
        global getraenk
        global gericht
        global zimmernummer

        getraenk_slot = ask_utils.request_util.get_slot(
            handler_input, "getraenk").to_dict()
        if getraenk_slot['value'] is not None:
            getraenk = getraenk_slot['resolutions']['resolutions_per_authority'][0]['values'][0]['value']['name']
        gericht_slot = ask_utils.request_util.get_slot(
            handler_input, "gericht").to_dict()

        if gericht_slot['value'] is not None:
            gericht = gericht_slot['resolutions']['resolutions_per_authority'][0]['values'][0]['value']['name']

        zimmernummer = ask_utils.request_util.get_slot_value(
            handler_input, "zimmernummer")

        if (getraenk != "nichts" and gericht != "nichts"):
            speak_output = f"deine bestellung lautet: {gericht} und {getraenk} für zimmer <say-as interpret-as='number'>{zimmernummer}</say-as>. möchtest du die bestellung jetzt abschließen?"
        elif (getraenk == "nichts" and gericht != "nichts"):
            speak_output = f"deine bestellung lautet: {gericht} für zimmer <say-as interpret-as='number'>{zimmernummer}</say-as>. möchtest du die bestellung jetzt abschließen?"
        elif (getraenk != "nichts" and gericht == "nichts"):
            speak_output = f"deine bestellung lautet: {getraenk} für zimmer <say-as interpret-as='number'>{zimmernummer}</say-as>.  möchtest du die bestellung jetzt abschließen?"
        else:
            return (
                handler_input.response_builder
                .speak("das kann ich leider nicht bestellen.")
                .response
            )
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("möchtest du die bestellung jetzt abschließen?")
            .add_directive(ConfirmIntentDirective())
            .response
        )


class BestellungIntentConfirmedHandler(AbstractRequestHandler):
    """Bestellung wurde nochmals bestätigt und jetzt wird der Prozess gestartet"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BestellungIntent")(handler_input) and bestellung_confirmed(handler_input) == "CONFIRMED"

    def handle(self, handler_input):
        if (getraenk != "nichts" and gericht != "nichts"):
            essen = f"{gericht} und {getraenk}"
        elif (getraenk == "nichts" and gericht != "nichts"):
            essen = f"{gericht}"
        elif (getraenk != "nichts" and gericht == "nichts"):
            essen = f"{getraenk}"

        requestBody = {
            "messageName": "Bestellung",
            "processVariables": {
                "essen": {
                    "value": essen,
                    "type": "String"
                },
                "zimmernummer": {
                    "value": zimmernummer,
                    "type": "Long"
                },
                "time": {
                    "value": str(datetime.datetime.now()),
                    "type": "String"
                }
            }
        }

        r = requests.post(camunda_url+"/rest/message", json=requestBody)
        if (r.status_code == 204):
            speak_output = "okay! danke für deine bestellung. sie wird in kürze zu deinem zimmer geliefert."
        else:
            speak_output = "deine bestellung kann derzeit nicht bearbeitet werden. versuches es bitte später erneut."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class BestellungIntentDeniedHandler(AbstractRequestHandler):
    """Falls der Gast die Bestellung nicht bestätigt"""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BestellungIntent")(handler_input) and bestellung_confirmed(handler_input) == "DENIED"

    def handle(self, handler_input):
        global gericht
        global getraenk
        global zimmernummer
        gericht = None
        getraenk = None
        zimmernummer = None
        speak_output = "okay. der bestellvorgang wurde abgebrochen."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler fuer Hilfe"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "bei mir kannst du etwas beim zimmerservice bestellen. lass uns mit dem gericht beginnen. wir haben schnitzel mit pommes, maultaschen mit kartoffelsalat und spagetti mit tomatensauce. was möchtest du essen?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler für Abbruche/Stopp"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
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
    """Handler für das Ende einer Session"""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        global zimmernummer
        global gericht
        global getraenk
        zimmernummer = None
        gericht = None
        getraenk = None

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

        speak_output = "das habe ich leider nicht verstanden. könntest du das bitte wiederholen?"

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
sb.add_request_handler(BestellungIntentUnconfirmedHandler())
sb.add_request_handler(BestellungIntentConfirmedHandler())
sb.add_request_handler(BestellungIntentDeniedHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
