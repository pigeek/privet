from typing import Any, Dict

SPEC: Dict[str, Any] = {
    "type": "cron",
    "title": "Cron",
    "displayName": "Cron",
    "data": {"targetGraph": None, "scheduleType": "interval", "schedule": "5 minutes", "executeImmediately": True, "useTargetGraphInput": False},
    "visual": {"width": 200},
    "uiData": {
        "infoBoxBody": "Executes a subgraph on a schedule (cron or interval).",
        "infoBoxTitle": "Cron Node",
        "contextMenuTitle": "Cron",
        "group": ["Advanced"],
    },
    "inputs": [
        {"id": "trigger", "title": "Trigger", "dataType": "boolean"},
        {"id": "targetGraph", "title": "Target Graph", "dataType": "string", "showIf": {"dataKey": "useTargetGraphInput", "equals": True}},
    ],
    "outputs": [
        {"id": "output", "title": "Last Output", "dataType": "any"},
        {"id": "iteration", "title": "Iteration", "dataType": "number"},
        {"id": "completed", "title": "Completed", "dataType": "boolean"},
        {"id": "nextRun", "title": "Next Run", "dataType": "string"},
    ],
    "editors": [
        {"type": "toggle", "dataKey": "executeImmediately", "label": "Execute Immediately"},
        {"type": "graphSelector", "dataKey": "targetGraph", "useInputToggleDataKey": "useTargetGraphInput", "label": "Target Graph"},
        {"type": "dropdown", "dataKey": "scheduleType", "label": "Schedule Type", "options": [ {"label": "Cron Expression", "value": "cron"}, {"label": "Simple Interval", "value": "interval"} ]},
        {"type": "string", "dataKey": "schedule", "label": "Schedule"},
    ],
}

