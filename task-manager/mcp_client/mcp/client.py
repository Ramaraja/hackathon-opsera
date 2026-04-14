import subprocess
import json
import threading

class Client:
    def __init__(self, command=["npx", "-y", "opsera"]):
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self._id = 0
        self.lock = threading.Lock()

    def _next_id(self):
        with self.lock:
            self._id += 1
            return self._id

    def _send(self, payload):
        message = json.dumps(payload)
        self.proc.stdin.write(message + "\n")
        self.proc.stdin.flush()

    def _receive(self):
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("No response from MCP server")
        return json.loads(line)

    def call_tool(self, name, arguments):
        request_id = self._next_id()

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }

        self._send(payload)
        response = self._receive()

        if "error" in response:
            raise Exception(response["error"])

        return response.get("result")

    def list_tools(self):
        request_id = self._next_id()

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/list",
            "params": {}
        }

        self._send(payload)
        return self._receive().get("result")

    def close(self):
        self.proc.terminate()