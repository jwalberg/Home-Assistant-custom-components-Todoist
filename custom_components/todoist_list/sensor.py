import hashlib

from todoist_api_python.api import TodoistAPI
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import async_generate_entity_id, Entity

DEFAULT_NAME = 'Todoist List'
CONF_TODOIST_API='todoist_api'
CONF_FILTER='filter'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_TODOIST_API): cv.string,
    vol.Optional(CONF_FILTER, default=""): cv.string
})


def replace_leading_spaces(s):
    stripped = s.lstrip()
    return '&nbsp;' * 2 * (len(s) - len(stripped)) + stripped


def setup_platform(hass, config, add_entities, discovery_info=None):
    sensor_name = config.get(CONF_NAME)
    filter = config.get(CONF_FILTER)
    todoist_api = config.get(CONF_TODOIST_API)

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

    @property
    def name(self):
        return '{} - {}'.format(self._name)

    @property
    def state(self):
        return 1 #len(self._tasks)

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
            content = task.content
            created_at=task.created_at
            description = str(task.description)
            url = str(task.url)
            due=task.due
            #due_date=task.due.date
            #recurring=task.due.recurring
            #due_string=task.due.string
            #due_timezone=task.due.timezone
            task_id=task.id

            labels = []
            if len(task.label) >0:
                for label in labels:
                    labels.append(label)
            self._tasks.append(task)

    @staticmethod
    def make_note(note_type, title, lines, children, checked, unchecked, color, url):
        note = dict()
        note["note_type"] = note_type
        note["title"] = title
        note["url"] = url
        note["lines"] = lines
        note["children"] = children
        note["color"] = color
        note["checked"] = checked
        note["unchecked"] = unchecked
        return note

    @staticmethod
    def map_node(node):
        node_data = dict()
        node_data["checked"] = node.checked
        node_data["text"] = node.text
        node_data["children"] = list(map(lambda c: TodoistSensor.map_node(c), node.subitems))
        return node_data
