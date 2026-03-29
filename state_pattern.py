#!/usr/bin/env python3
"""State machine pattern. Zero dependencies."""

class StateMachine:
    def __init__(self, initial, transitions=None):
        self.state = initial; self.transitions = transitions or {}
        self.history = [initial]; self.on_enter = {}; self.on_exit = {}

    def add_transition(self, from_state, event, to_state, action=None):
        self.transitions[(from_state, event)] = (to_state, action)
        return self

    def trigger(self, event, *args):
        key = (self.state, event)
        if key not in self.transitions:
            raise ValueError(f"No transition from {self.state} on {event}")
        to_state, action = self.transitions[key]
        if self.state in self.on_exit: self.on_exit[self.state](self.state, event)
        old = self.state; self.state = to_state; self.history.append(to_state)
        if action: action(old, to_state, *args)
        if to_state in self.on_enter: self.on_enter[to_state](to_state, event)
        return self

    def can_trigger(self, event):
        return (self.state, event) in self.transitions

    def reset(self):
        self.state = self.history[0]; self.history = [self.state]

    def available_events(self):
        return [e for (s, e) in self.transitions if s == self.state]

def traffic_light():
    sm = StateMachine("red")
    sm.add_transition("red", "next", "green")
    sm.add_transition("green", "next", "yellow")
    sm.add_transition("yellow", "next", "red")
    return sm

if __name__ == "__main__":
    tl = traffic_light()
    for _ in range(6): print(tl.state); tl.trigger("next")
