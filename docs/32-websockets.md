# WebSockets

Asok includes a minimal, standard-library-only WebSocket server (RFC 6455). It runs in a background daemon thread alongside the WSGI server and shares the same session and authentication system.

## Setup

The WebSocket server runs on a separate port (default: `8001`). 

```python
from asok import Asok, WebSocketServer

app = Asok()
ws = WebSocketServer(port=8001)

# Handler registration goes here...

ws.start()  # Spawns daemon threads; returns immediately
```

In dev, `asok dev` forks a child that imports your app, so the WS server
starts automatically alongside the HTTP server. Ctrl-C and hot-reload stop
and restart both together.

## Security

Asok protects against Cross-Site WebSocket Hijacking (CSWH) by validating the `Origin` header during the handshake.

### Allowed Origins

By default, the server allows:
- `localhost` and `127.0.0.1` (and their common ports).
- Any origins listed in `app.config["CORS_ORIGINS"]` (if `app` is passed to the server).

You can configure origins explicitly in three ways:

1.  **Constructor**: `ws = WebSocketServer(allowed_origins=["https://myapp.com"])`
2.  **App Config**: Set `CORS_ORIGINS` in your `Asok` app instance.
3.  **Environment Variable**: Set `WS_ALLOWED_ORIGINS=https://a.com,https://b.com`.

**Wildcards** are supported (e.g., `https://*.mydomain.com`).

### Authentication

The WebSocket server shares session cookies with the main app. `conn.user` is automatically populated if the user is logged in via the standard `asok` session.

## Production Setup

## Handlers

Register handlers using decorators. Asok supports [dynamic parameters] in WebSocket paths, similar to page routing.

### `@ws.on(path)`

Handles incoming text messages for a specific path.

```python
@ws.on("/chat/[room]")
def on_message(conn, message):
    room = conn.params['room']
    name = conn.user.name if conn.user else "Guest"
    ws.broadcast(f"/chat/{room}", f"{name}: {message}")
```

### `@ws.on_connect(path)`

Triggered when a new client connects.

```python
@ws.on_connect("/notifications")
def on_connect(conn):
    print(f"Client connected from {conn.addr}")
    conn.send("Connected to notification stream")
```

### `@ws.on_disconnect(path)`

Triggered when a client closes the connection.

```python
@ws.on_disconnect("/chat")
def on_disconnect(conn):
    ws.broadcast("/chat", "Someone left the chat")
```

## Advanced Features

Asok includes built-in operators for handling common real-time features like presence tracking, room join authorization, typing indicators, and read receipts. These features leverage standard browser `CustomEvent` dispatching.

### 1. User Presence Tracking

Presence tracking monitors logged-in user connections across tabs. Multiple open tabs/connections for the same user are reference-counted to ensure accurate status reports.

* **Server-side query APIs**:
  - `ws.get_online_users()`: Returns a list of active online user IDs.
  - `ws.is_user_online(user_id)`: Returns `True` if the user is online, otherwise `False`.
* **Client-side query message**:
  Clients can fetch the list of online users by sending:
  ```json
  {"op": "get_presence"}
  ```
  The server responds with a `presence_list` broadcast:
  ```json
  {"op": "broadcast", "type": "presence_list", "users": [101, 102]}
  ```
* **Real-time broadcasts**:
  When a user transitions from offline to online (or vice-versa), the server broadcasts a status event to all active connections:
  - **Online**: `{"op": "broadcast", "type": "presence", "user_id": 42, "status": "online"}`
  - **Offline**: `{"op": "broadcast", "type": "presence", "user_id": 42, "status": "offline"}`

These messages trigger a native JS custom event on the frontend document:
```javascript
document.addEventListener("asok:ws-broadcast", (e) => {
    const data = e.detail;
    if (data.type === "presence") {
        console.log(`User ${data.user_id} is now ${data.status}`);
    }
});
```

### 2. Room Join Authorization

Secure rooms by intercepting join requests before a connection is subscribed.

Register a room authorizer callback using the `@ws.room_authorizer` decorator:
```python
@ws.room_authorizer
def authorize_room_join(conn, room):
    if room.startswith("admin:"):
        return conn.user and getattr(conn.user, "is_admin", False)
    return True
```

If authorization fails, the server sends a broadcast error back to the requester:
```json
{"op": "broadcast", "type": "error", "room": "admin:secrets", "message": "Unauthorized or invalid room join request..."}
```

### 3. Typing Indicators

Clients can broadcast typing indicators to room subscribers. 

* **Outgoing client message**:
  ```json
  {"op": "typing", "room": "chat-room", "typing": true}
  ```
* **Incoming broadcast (sent to all other subscribers in the room)**:
  ```json
  {"op": "broadcast", "type": "typing", "room": "chat-room", "user_id": 42, "typing": true}
  ```

### 4. Read Receipts

Deliver message read receipts instantly to other room members.

* **Outgoing client message**:
  ```json
  {"op": "receipt", "room": "chat-room", "message_id": 123, "status": "read"}
  ```
* **Incoming broadcast (sent to all other subscribers in the room)**:
  ```json
  {"op": "broadcast", "type": "receipt", "room": "chat-room", "message_id": 123, "user_id": 42, "status": "read"}
  ```

## The `Connection` Object

Each handler receives a `Connection` object representing the client:

| Property | Description |
|---|---|
| `conn.user` | The authenticated `User` model (if logged in via Asok cookie). |
| `conn.params` | Dict of dynamic path parameters (e.g., `{'room': 'general'}`). |
| `conn.path` | The request path (e.g., `/chat/general`). |
| `conn.headers`| Dict of HTTP headers from the handshake request. |
| `conn.addr` | Tuple of `(ip, port)` of the client. |

### Methods

- `conn.send(message)`: Send a text string.
- `conn.send_json(obj)`: Send a JSON-serializable object.
- `conn.close(code=1000, reason="")`: Close the connection.

## Broadcasting

You can send messages to all clients connected to a specific path:

```python
# Send to everyone on /chat
ws.broadcast("/chat", "Hello everyone!")

# Send JSON
ws.broadcast_json("/chat", {"type": "alert", "content": "System restart"})

# Exclude a specific connection (e.g., the sender)
ws.broadcast("/chat", "You sent a message", exclude=conn)
```

## Authentication

Authentication is automatic. When a client connects, Asok looks for the `asok_session` cookie in the handshake headers. 
- If valid, `conn.user` is populated with the corresponding model instance.
- This allows you to restrict WebSocket access using the same logic as your web pages.

## Deployment (Nginx)

In production, you should run the WebSocket server behind a reverse proxy.

```nginx
# nginx configuration
location /ws/ {
    proxy_pass http://127.0.0.1:8001/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 3600s;
}
```

## Frontend: `window.asokWS(path)`

Asok automatically injects a helper function in your HTML templates to simplify WebSocket connection. It handles the protocol (`ws` vs `wss`) and the port automatically.

```javascript
// Automatically connects to ws://localhost:8001/chat in dev
// or wss://yourdomain.com/ws/chat in production
const socket = window.asokWS('/chat');

socket.onmessage = (event) => {
    console.log('Message from server:', event.data);
};

socket.send('Hello server!');
```

This helper is available globally in any template rendered with `request.html()`.

---
[← Previous: API Development](31-api-development.md) | [Documentation](README.md) | [Next: Email Service →](33-email-service.md)
