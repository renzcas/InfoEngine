# backend/core/infoengine_category.py

from typing import Any, Dict
from backend.core.catcore import Category, Morphism, Functor

# ---------------------------------------------------------
# 1. Define the InfoEngine category (backend organs)
# ---------------------------------------------------------

I = Category("InfoEngine")

ORGANS = [
    "CyberArenaBackend",
    "EpisodeEngine",
    "EventBus",
    "JuiceShopTarget",
    "CockpitAPI",
    "ObservabilityService",
]

for o in ORGANS:
    I.add_object(o)

# ---------------------------------------------------------
# 2. Define backend morphisms (real or stubbed)
# ---------------------------------------------------------

def attack_scenario(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"episode_spec": payload, "status": "constructed"}

def emit_event(episode_state: Dict[str, Any]) -> Dict[str, Any]:
    return {"event": "EPISODE_UPDATED", "data": episode_state}

def query_target(query: Dict[str, Any]) -> Dict[str, Any]:
    return {"target": "JuiceShop", "status": "up", "details": query}

def log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    return {"logged": True, "event": event}

m_attack_scenario = Morphism("attackScenario", "CyberArenaBackend", "EpisodeEngine", attack_scenario)
m_emit_event = Morphism("emitEvent", "EpisodeEngine", "EventBus", emit_event)
m_query_target = Morphism("queryTarget", "CockpitAPI", "JuiceShopTarget", query_target)
m_log_event = Morphism("logEvent", "EventBus", "ObservabilityService", log_event)

for m in [m_attack_scenario, m_emit_event, m_query_target, m_log_event]:
    I.add_morphism(m)

# Example composite morphism
m_attack_then_emit = I.compose(m_emit_event, m_attack_scenario)

# ---------------------------------------------------------
# 3. Define the Cockpit UI category
# ---------------------------------------------------------

U = Category("CockpitUI")

UI_OBJECTS = [
    "AttackMapPanel",
    "EpisodePanel",
    "EventStreamOverlay",
    "TargetStatusPanel",
]

for o in UI_OBJECTS:
    U.add_object(o)

# UI morphisms (state transforms)
def render_scenario(episode_spec: Dict[str, Any]) -> Dict[str, Any]:
    return {"panel": "AttackMapPanel", "episode": episode_spec}

def render_events(event: Dict[str, Any]) -> Dict[str, Any]:
    return {"panel": "EventStreamOverlay", "event": event}

def render_target(target_state: Dict[str, Any]) -> Dict[str, Any]:
    return {"panel": "TargetStatusPanel", "target": target_state}

ui_render_scenario = Morphism("renderScenario", "EpisodePanel", "AttackMapPanel", render_scenario)
ui_render_events = Morphism("renderEvents", "EventStreamOverlay", "EventStreamOverlay", render_events)
ui_render_target = Morphism("renderTarget", "TargetStatusPanel", "TargetStatusPanel", render_target)

for m in [ui_render_scenario, ui_render_events, ui_render_target]:
    U.add_morphism(m)

# ---------------------------------------------------------
# 4. Functor F: InfoEngine -> CockpitUI
# ---------------------------------------------------------

F = Functor("CockpitView", I, U)

# Object mapping
F.map_object("CyberArenaBackend", "AttackMapPanel")
F.map_object("EpisodeEngine", "EpisodePanel")
F.map_object("EventBus", "EventStreamOverlay")
F.map_object("JuiceShopTarget", "TargetStatusPanel")
F.map_object("CockpitAPI", "TargetStatusPanel")
F.map_object("ObservabilityService", "EventStreamOverlay")

# Morphism mapping
F.map_morphism(m_attack_scenario, ui_render_scenario)
F.map_morphism(m_emit_event, ui_render_events)
F.map_morphism(m_query_target, ui_render_target)

# ---------------------------------------------------------
# 5. Example pipeline
# ---------------------------------------------------------

def run_attack_pipeline(scenario_payload: Dict[str, Any]) -> Dict[str, Any]:
    episode_state = m_attack_scenario(scenario_payload)
    event = m_emit_event(episode_state)

    ui_episode_view = F.F_mor(m_attack_scenario)(episode_state)
    ui_event_view = F.F_mor(m_emit_event)(event)

    return {
        "backend": {
            "episode_state": episode_state,
            "event": event,
        },
        "ui": {
            "episode_view": ui_episode_view,
            "event_view": ui_event_view,
        },
    }
