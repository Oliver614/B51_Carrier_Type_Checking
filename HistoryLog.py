import json
import datetime

history_log_json = open('LogFiles/history_log.json', 'r+')
history_dictionary = json.loads(history_log_json.read())


def get_history_list():
    log_list = []
    for entry in history_dictionary['entries'].items():
        log_list.append(list(entry))
    return log_list


def log_classification(image_location, carrier_type, probability):
    time = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    log_this = {time: {}}
    for variable in ["image_location", "carrier_type", "probability"]:
        log_this[time][variable] = eval(variable)
    append_history(log_this)
    dump_to_file()


def append_history(data):
    history_dictionary['entries'].update(data)


def dump_to_file():
    history_log_json.seek(0)
    # convert back to json.
    json.dump(history_dictionary, history_log_json, indent=4)



