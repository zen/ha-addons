"""
Support for Blebox wLightBoxS lights.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.flux_led/
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    Light, PLATFORM_SCHEMA, ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)
from homeassistant.const import CONF_HOST, CONF_NAME

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['https://github.com/zen/python-blebox/archive/master.zip#python-blebox==0.0.3']

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'wLightBoxS LED'

SUPPORT_WLIGHTBOXS = (
    SUPPORT_BRIGHTNESS
)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Blebox wLightBoxS platform."""

    from pyblebox.wlightboxs import wLightBoxS
    from pyblebox.exceptions import wLightBoxSConnectionError

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)

    wlightboxs = wLightBoxS(host)

    try:
        if wlightboxs.get_status()['device']['type'] != 'wLightBoxS':
            _LOGGER.error("Device %s is not a wLightBoxS controller", host)
            return
    except wLightBoxSConnectionError:
        _LOGGER.warning("No connection to device: %s", host)

    add_devices([wLightBoxS(host)], True)


class wLightBoxS(Light):
    """Representation of an wLightBoxS."""

    def __init__(self, light):
        """Initialize a wLightBoxS."""

        self._light = light
        self._name = None
        self._state = None
        self._brightness = None
        self._supported_features = SUPPORT_BRIGHTNESS
        self._available = False

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def supported_features(self):
        """Flag supported features."""
        return self._supported_features

    @property
    def brightness(self):
        """Return the brightness of the light."""

        return self._brightness

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def is_on(self):
        """Return true if light is on."""

        return self._state['on'] if self._state is not None else None

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        from pyblebox.exceptions import wLightBoxSConnectionError

        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)

        try:
            if not self.is_on:
                self._light.set_on()
            if brightness is not None:
                self._light.set_brightness(brightness)
        except wLightBoxSConnectionError:
            _LOGGER.warning("No connection to device")

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        from pyblebox.exceptions import wLightBoxSConnectionError

        try:
            self._light.set_off()
        except wLightBoxSConnectionError:
            _LOGGER.warning("No connection to device")

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        from pyblebox.exceptions import wLightBoxSConnectionError

        try:
            self._state = self._light.get_status()
            self._available = True
            self._brightness = self._light.get_brightness()
        except wLightBoxSConnectionError:
            _LOGGER.warning("No route to device")
            self._available = False
