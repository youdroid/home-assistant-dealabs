"""Platform for sensor integration."""
import logging

import requests
import json
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import PLATFORM_SCHEMA
import xml.etree.ElementTree as ET
from homeassistant.const import CONF_TOKEN

_LOGGER = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36\''
}

URL = "https://www.dealabs.com/rssx/keyword-alarm/"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_TOKEN): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([DealabsSensor(config.get(CONF_TOKEN))])


class DealabsSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, token):
        self._state = None
        self.token = token
        self.data = {}
        self.attr = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return "dealabs"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:cart-plus"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attr

    def update(self):
        join_url = URL + self.token;
        rqt = requests.request(method='GET', url=join_url, headers=headers).text.encode('utf8')
        tree = ET.fromstring(rqt)
        deals = []
        nb = 0
        for child in tree.findall('./channel/item'):

            try:
                merchant = child.find('{http://www.pepper.com/rss}merchant').attrib.get('name')
            except:
                merchant = "null"
            try:
                price = child.find('{http://www.pepper.com/rss}merchant').attrib.get('price')
            except:
                price = "null"

            image = child.find('{http://search.yahoo.com/mrss/}content').attrib.get('url')

            d = Deal(child.find('category').text, merchant,
                     price,
                     self.extractTitle(child.find('title').text), child.find('link').text, child.find('pubDate').text, image)
            self.attr["Alert_" + str(nb)] = json.dumps(d.__dict__)
            nb += 1
        self._state = nb

    def extractTitle(self, str):
        return str.split('<strong>')[0]


class Deal(Entity):
    """Representation of a Sensor."""

    def __init__(self, category, merchant, price, title, link, pubDate, image):
        self.category = category
        self.merchant = merchant
        self.price = price
        self.title = title
        self.link = link
        self.pubDate = pubDate
        self.image = image
