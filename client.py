"""Agent Message Bus & Hierarchical Topic Router.
100% Python Standard Library.
"""

import collections

class AgentMessageBus:
    """Asynchronous topic-based message bus with wildcard matching."""
    def __init__(self):
        self.subscribers = collections.defaultdict(list)

    def subscribe(self, agent_id, topic):
        self.subscribers[topic].append(agent_id)

    def publish(self, topic, message):
        delivered = []
        for reg_topic, agents in self.subscribers.items():
            if self._topic_match(reg_topic, topic):
                for ag in agents:
                    delivered.append({"agent": ag, "topic": topic, "message": message})
        return delivered

    @staticmethod
    def _topic_match(pattern, topic):
        if pattern == "#" or pattern == topic:
            return True
        p_parts = pattern.split(".")
        t_parts = topic.split(".")
        if len(p_parts) != len(t_parts) and pattern[-1] != "#":
            return False
        for p, t in zip(p_parts, t_parts):
            if p == "#":
                return True
            if p != "*" and p != t:
                return False
        return True
