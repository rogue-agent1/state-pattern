from state_pattern import StateMachine, traffic_light
tl = traffic_light()
assert tl.state == "red"
tl.trigger("next"); assert tl.state == "green"
tl.trigger("next"); assert tl.state == "yellow"
tl.trigger("next"); assert tl.state == "red"
assert tl.history == ["red","green","yellow","red"]
assert tl.can_trigger("next")
assert not tl.can_trigger("stop")
assert tl.available_events() == ["next"]
sm = StateMachine("idle")
log = []
sm.add_transition("idle","start","running", lambda o,n: log.append(f"{o}->{n}"))
sm.trigger("start")
assert log == ["idle->running"]
sm.reset(); assert sm.state == "idle"
print("state_pattern tests passed")
