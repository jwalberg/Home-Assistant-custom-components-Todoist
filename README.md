

# Todoist List sensor

This sensor downloads a list of tasks from [*Todoist*](https://todoist.com/). At this point, consider this verions 0.0.0.
 
## Configuration options

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `Todoist List` | Name of sensor |
| `todoist_api` | `string` | `True` | - | Todoist API key |
| `filter` | `string` | `False` |  | A valid search filter using Todoist's filter rules|

## Example usage
```
sensor:
 -  platform: todoist_list
    todoist_api: !secret todoist_list_api
    filter: "due before today"
```

## Installation


### TODO



## Hints

* To present data downloaded by this sensor use companion card: [*Lovelace Todoist List card*](https://github.com/PiotrMachowski/Lovelace-Google-Keep-card)

* **What to do if Home Assistant does not find this component?**

  Most likely you have to install additional dependency required for it to run. Activate Python environment Home Assistant is running in and use following command:
  ```bash
  pip install todoist_api_python
  ```

## Acknowledgements
This was forked from the [Google Keep](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Google-Keep) project for Home Assistant.
