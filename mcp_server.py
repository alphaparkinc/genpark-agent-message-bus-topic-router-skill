import sys
import json
from client import AgentMessageBus

bus = AgentMessageBus()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agent-message-bus-topic-router-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "subscribe_agent_topic",
                        "description": "Subscribe agent to topic pattern (supports wildcards * and #)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "agent_id": {"type": "string"},
                                "topic_pattern": {"type": "string"}
                            },
                            "required": ["agent_id", "topic_pattern"]
                        }
                    },
                    {
                        "name": "publish_agent_event",
                        "description": "Publish message event to specified topic",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {"type": "string"},
                                "message": {"type": "object"}
                            },
                            "required": ["topic", "message"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "subscribe_agent_topic":
            bus.subscribe(args.get("agent_id"), args.get("topic_pattern"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Subscribed"}]}}
        elif tool_name == "publish_agent_event":
            d = bus.publish(args.get("topic"), args.get("message"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"delivered_count": len(d), "deliveries": d})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
