LABS = {
    "LAB1":  {"title": "Banner Grabber",              "lesson": "L3"},
    "LAB2":  {"title": "Port Scanner",                "lesson": "L3"},
    "LAB3":  {"title": "Directory Brute Forcer",      "lesson": "L4"},
    "LAB4":  {"title": "Subdomain Enumerator",        "lesson": "L4"},
    "LAB5":  {"title": "Web Scraper",                 "lesson": "L4"},
    "LAB6":  {"title": "OS Fingerprinter",            "lesson": "L5"},
    "LAB7":  {"title": "User Enumerator",             "lesson": "L5"},
    "LAB8":  {"title": "Process Scanner",             "lesson": "L5"},
    "LAB9":  {"title": "File Exfil Script",           "lesson": "L2"},
    "LAB10": {"title": "Log Parser",                  "lesson": "L2"},
    "LAB11": {"title": "TCP Client",                  "lesson": "L3"},
    "LAB12": {"title": "TCP Server",                  "lesson": "L3"},
    "LAB13": {"title": "Reverse Shell",               "lesson": "L3"},
    "LAB14": {"title": "Bind Shell",                  "lesson": "L3"},
    "LAB15": {"title": "Simple C2 Agent",             "lesson": "L10"},
    "LAB16": {"title": "Threaded Scanner",            "lesson": "L7"},
    "LAB17": {"title": "Credential Extractor",        "lesson": "L6"},
    "LAB18": {"title": "Recon Bot",                   "lesson": "L4"},
    "LAB19": {"title": "Persistence Script",          "lesson": "L5"},
    "LAB20": {"title": "Full Python Cyber Agent",     "lesson": "L10"},
}


def get_lab(lab_id: str):
    return LABS.get(lab_id)
