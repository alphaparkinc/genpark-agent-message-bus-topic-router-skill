from client import AgentMessageBus

bus = AgentMessageBus()
bus.subscribe("Security_Bot", "alert.#")
bus.subscribe("Ops_Bot", "alert.critical")

messages = bus.publish("alert.critical", {"message": "Memory threshold exceeded 95%"})
print("Delivered Message Events:", messages)
