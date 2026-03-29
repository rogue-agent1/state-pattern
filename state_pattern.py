#!/usr/bin/env python3
"""state_pattern: State pattern with transitions and guards."""
import sys

class State:
    def __init__(self, name, on_enter=None, on_exit=None):
        self.name = name; self.on_enter = on_enter; self.on_exit = on_exit
        self.transitions = {}
    def add_transition(self, event, target, guard=None, action=None):
        self.transitions[event] = {"target": target, "guard": guard, "action": action}

class StateMachine:
    def __init__(self, initial):
        self.states = {}; self.current = None; self._initial = initial
        self.history = []

    def add_state(self, state):
        self.states[state.name] = state; return self

    def start(self, context=None):
        self.current = self.states[self._initial]
        self.history.append(self.current.name)
        if self.current.on_enter: self.current.on_enter(context)

    def send(self, event, context=None):
        if event not in self.current.transitions:
            return False
        t = self.current.transitions[event]
        if t["guard"] and not t["guard"](context):
            return False
        if self.current.on_exit: self.current.on_exit(context)
        if t["action"]: t["action"](context)
        self.current = self.states[t["target"]]
        self.history.append(self.current.name)
        if self.current.on_enter: self.current.on_enter(context)
        return True

    @property
    def state(self): return self.current.name if self.current else None

def test():
    log = []
    idle = State("idle", on_enter=lambda c: log.append("enter_idle"))
    loading = State("loading", on_enter=lambda c: log.append("enter_loading"))
    ready = State("ready", on_enter=lambda c: log.append("enter_ready"))
    error = State("error")
    idle.add_transition("fetch", "loading")
    loading.add_transition("success", "ready")
    loading.add_transition("failure", "error")
    ready.add_transition("reset", "idle")
    error.add_transition("retry", "loading")
    sm = StateMachine("idle")
    sm.add_state(idle).add_state(loading).add_state(ready).add_state(error)
    sm.start()
    assert sm.state == "idle"
    assert sm.send("fetch")
    assert sm.state == "loading"
    assert sm.send("success")
    assert sm.state == "ready"
    assert sm.send("reset")
    assert sm.state == "idle"
    assert not sm.send("success")  # Invalid transition
    assert sm.state == "idle"
    # Guard
    guarded = State("guarded")
    guarded.add_transition("go", "idle", guard=lambda c: c and c.get("allowed"))
    sm.add_state(guarded)
    sm.current = sm.states["guarded"]
    assert not sm.send("go", {"allowed": False})
    assert sm.send("go", {"allowed": True})
    # History
    assert len(sm.history) > 0
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: state_pattern.py test")
