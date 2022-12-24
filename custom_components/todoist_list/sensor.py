import hashlib

from todoist_api_python.api import TodoistAPI
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import logging
from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import async_generate_entity_id, Entity

DEFAULT_NAME = 'Todoist List'
CONF_TODOIST_API='todoist_api'
CONF_FILTER='filter'

_LOGGER: logging.Logger = logging.getLogger(__package__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_TODOIST_API): cv.string,
    vol.Optional(CONF_FILTER, default="due today"): cv.string
})


def replace_leading_spaces(s):
    stripped = s.lstrip()
    return '&nbsp;' * 2 * (len(s) - len(stripped)) + stripped


def setup_platform(hass, config, add_entities, discovery_info=None):
    sensor_name = config.get(CONF_NAME)
    filter = config.get(CONF_FILTER)
    todoist_api = config.get(CONF_TODOIST_API)
    _LOGGER.debug("SETUP: name " + sensor_name + "; filter " + filter + "; api " + todoist_api)
    api = TodoistAPI(todoist_api)
    
    if not api:
        raise Exception('Invalid api key')

    dev = []
    hash_value = hashlib.md5(str((sensor_name, str(filter), str(CONF_TODOIST_API))).encode()).hexdigest()[-10:]
    uid = '{}_{}'.format(sensor_name, hash_value)
    entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
    dev.append(TodoistSensor(entity_id, sensor_name,  api, filter))
    add_entities(dev, True)


class TodoistSensor(Entity):
    def __init__(self, entity_id, name, api, filter):
        self.entity_id = entity_id
        self._name = name
        self._api = api
        self._filter = filter
        self._tasks = []
        self._state = None
        self.

    @property
    def name(self):
        return '{} - {}'.format(self._name)

    @property
    def state(self):
        return len(self._tasks)

    @property
    def extra_state_attributes(self):
        attr = dict()
        attr['tasks'] = self._tasks
        attr[CONF_TODOIST_API] = self._api
        attr[CONF_FILTER] = self._filter

        return attr


    def update(self):
        pass
        tasks=self._api.get_tasks(filter=self._filter)
        self._tasks = []
        
        for task in tasks:
            _LOGGER.debug("task=" + task.content)
            if len(task.labels) >0:
                labels = []
                for label in task.labels:
                    labels.append(label)
            savetask={
                "content":task.content,
                #"created_at":task.created_at,
                #"description":str(task.description),
                #"url":str(task.url),
                #"due":task.due,
                #"due_date":task.due.date,
                #recurring":task.due.recurring
                #due_string":task.due.string
                #due_timezone":task.due.timezone
                "task_id":task.id,
                #"labels":labels
            }
            self._tasks.append(savetask)

    @staticmethod
    def make_note(content, task_id): #,  description, url, due, labels):
        note = dict()
        note["note_type"] = content
        note["title"] = task_id
        #note["url"] = url
        #note["lines"] = lines
        #note["children"] = children
        #note["color"] = color
        #note["checked"] = checked
        #note["unchecked"] = unchecked
        return note

    @staticmethod
    def map_node(node):
        node_data = dict()
        node_data["content"] = node.content
        node_data["task_id"] = node.task_id
        #node_data["children"] = list(map(lambda c: TodoistSensor.map_node(c), node.subitems))
        return node_data
 
