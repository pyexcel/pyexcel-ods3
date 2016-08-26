import sys
import datetime


def float_value(value):
    """convert a value to float"""
    ret = float(value)
    return ret


def date_value(value):
    """convert to data value accroding ods specification"""
    ret = "invalid"
    try:
        # catch strptime exceptions only
        if len(value) == 10:
            ret = datetime.datetime.strptime(
                value,
                "%Y-%m-%d")
            ret = ret.date()
        elif len(value) == 19:
            ret = datetime.datetime.strptime(
                value,
                "%Y-%m-%dT%H:%M:%S")
        elif len(value) > 19:
            ret = datetime.datetime.strptime(
                value[0:26],
                "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        pass
    if ret == "invalid":
        raise Exception("Bad date value %s" % value)
    return ret


def time_value(value):
    """convert to time value accroding the specification"""
    hour = int(value[2:4])
    minute = int(value[5:7])
    second = int(value[8:10])
    if hour < 24:
        ret = datetime.time(hour, minute, second)
    else:
        ret = datetime.timedelta(hours=hour, minutes=minute, seconds=second)
    return ret


def boolean_value(value):
    """get bolean value"""
    return value


ODS_FORMAT_CONVERSION = {
    "float": float,
    "date": datetime.date,
    "time": datetime.time,
    "boolean": bool,
    "percentage": float,
    "currency": float
}


ODS_WRITE_FORMAT_COVERSION = {
    float: "float",
    int: "float",
    str: "string",
    datetime.date: "date",
    datetime.time: "time",
    datetime.timedelta: "timedelta",
    bool: "boolean"
}


VALUE_CONVERTERS = {
    "float": float_value,
    "date": date_value,
    "time": time_value,
    "boolean": boolean_value,
    "percentage": float_value,
    "currency": float_value
}


VALUE_TOKEN = {
    "float": "value",
    "date": "date-value",
    "time": "time-value",
    "boolean": "boolean-value",
    "percentage": "value",
    "currency": "value"
}


if sys.version_info[0] < 3:
    ODS_WRITE_FORMAT_COVERSION[unicode] = "string"
