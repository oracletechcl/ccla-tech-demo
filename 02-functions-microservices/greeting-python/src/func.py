import io
import sys
import json
import time

def handler(ctx, data: io.BytesIO = None):
    try:
        body = json.loads(data.getvalue())
        name = body.get("name", "world")
        stress_ms = int(body.get("stress_ms", 0)) / 1000
        if stress_ms > 0:
            time.sleep(stress_ms)
        return json.dumps({"message": f"Hello, {name}!"})
    except Exception as e:
        return json.dumps({"error": str(e)})
