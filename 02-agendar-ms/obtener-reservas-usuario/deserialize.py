import datetime


def default_serializer(obj):
    if isinstance(obj, (datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

    return json.dumps(rows, default=default_serializer)