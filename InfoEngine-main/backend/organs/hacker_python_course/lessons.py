LESSONS = {
    "L1": {
        "title": "Python for Operators",
        "summary": "Vars, lists, dicts, functions, classes, CLI basics.",
    },
    "L2": {
        "title": "Files, Logs, and Loot",
        "summary": "Read/write files, parse logs, store loot.",
    },
    "L3": {
        "title": "Networking Essentials",
        "summary": "Sockets, TCP client/server, reverse shell basics.",
    },
    "L4": {
        "title": "Web Requests & Recon",
        "summary": "requests, GET/POST, headers, scraping.",
    },
    "L5": {
        "title": "Subprocess & System Interaction",
        "summary": "Run commands, capture output, privilege checks.",
    },
    "L6": {
        "title": "Regex for Extraction",
        "summary": "Extract emails, IPs, URLs, creds from text.",
    },
    "L7": {
        "title": "Threading & Speed",
        "summary": "Threaded scanners, parallel tasks.",
    },
    "L8": {
        "title": "Serialization & Payloads",
        "summary": "JSON, base64, simple payload formats.",
    },
    "L9": {
        "title": "Crypto Basics",
        "summary": "Hashing, encoding, integrity checks.",
    },
    "L10": {
        "title": "Building Agents",
        "summary": "State, perceive/decide/act, networking, persistence.",
    },
}


def get_lesson(lesson_id: str):
    return LESSONS.get(lesson_id)
