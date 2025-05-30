from ovos_utils import classproperty
from ovos_utils.log import LOG
from ovos_workshop.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
import requests

DEFAULT_SETTINGS = {
    "log_level": "INFO"
}

class HomeyWebhookSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.override = True
        
    @classproperty
    def runtime_requirements(self):
        # if this isn't defined the skill will
        # only load if there is internet
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=True,
            gui_before_load=False,
            requires_internet=False,
            requires_network=True,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    def initialize(self,):
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)
        self.settings_change_callback = self.on_settings_changed
        #self.add_event('mycroft.light.play', self.handle_play_light)
        #self.register_intent_file('PlayLight.intent', self.handle_play_light)
        #self.add_event('mycroft.skyradio.play', self.handle_play_skyradio)  # add an event in the message.bus, in this case the speak event
        #self.add_event('mycroft.skyradio.stop', self.handle_stop_skyradio)
        #self.register_intent_file('Playskyradio.intent', self.handle_play_skyradio)
        #self.register_intent_file('Stopskyradio.intent', self.handle_stop_skyradio)

    def on_settings_changed(self):
        """This method is called when the skill settings are changed."""
        LOG.info("Settings changed!")

    @property
    def log_level(self):
        """Dynamically get the 'log_level' value from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("log_level", "INFO")

    @intent_handler(IntentBuilder("SkyRadioOnOff.intent").require("KeyWordSkyRadio.voc"))
    def handle_sky_radio_intent(self, message):
        self.log.info("SkyRadio Adapt intent is triggered with a KeyWord")
        # wait=True will block the message bus until the dialog is finished
        self.speak("this is a dummy, there is no webhook in script", wait=True)

    @intent_handler(IntentBuilder("LightOnOff.intent"))
    def LightOnOff(self):
        url = f"https://webhook.homey.app/65d346bd8b9cb2e8ec0d2f77/Terre?tag=Light"
        data = requests.get(url)
        self.log.info(f"HOMEY initiated the URL response in json {data.json()}")
        self.speak_dialog("LightOnOff", wait=True)

    @intent_handler(IntentBuilder("CurtainClose.intent"))
    def handle_curtain_close(self, message):
        self.log.info("Close curtain is triggered by an intent")
        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=CurtainClose"
        data = requests.get(url)
        self.speak_dialog("CurtainClosed", wait=True)

    @intent_handler(IntentBuilder("CurtainOpen.intent"))
    def handle_curtain_open(self, message):
        self.log.info("Open curtain is stopped by an intent")
        url = f"http://192.168.1.187/api/manager/logic/webhook/Demo/?tag=CurtainOpen"
        data = requests.get(url)
        self.speak_dialog("CurtainOpened", wait=True)

def create_skill():
    return HomeyWebhookSkill()
