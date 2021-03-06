"""Discord platform for notify component."""
import logging
import asyncio
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    PLATFORM_SCHEMA, BaseNotificationService)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['discord.py==0.16.0']

CONF_TOKEN = 'token'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TOKEN): cv.string
})


def get_service(hass, config, discovery_info=None):
    """Get the Discord notification service."""
    token = config.get(CONF_TOKEN)
    return DiscordNotificationService(hass, token)


class DiscordNotificationService(BaseNotificationService):
    """Implement the notification service for Discord."""

    def __init__(self, hass, token):
        """Initialize the service."""
        self.token = token
        self.hass = hass

    @asyncio.coroutine
    def async_send_message(self, message, target):
        """Login to Discord, send message to channel(s) and log out."""
        import discord
        discord_bot = discord.Client(loop=self.hass.loop)

        yield from discord_bot.login(self.token)

        for channelid in target:
            channel = discord.Object(id=channelid)
            yield from discord_bot.send_message(channel, message)

        yield from discord_bot.logout()
        yield from discord_bot.close()

    def send_message(self, message=None, target=None, **kwargs):
        """Send a message using Discord."""
        self.hass.async_add_job(self.async_send_message(message, target))
