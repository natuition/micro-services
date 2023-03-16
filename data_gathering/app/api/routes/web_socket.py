from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.api.models.session import SessionUpdate
from app.api.models.gps_point import GPSPointIn
from app.api.models.point_of_path import PointOfPathIn
from app.api.models.weed_type import WeedTypeIn
from app.api.models.extracted_weed import ExtractedWeedIn
from app.api.database.db_manager import update_session, add_gps_point, add_point_of_path, get_weed_type, add_extracted_weed
import pytz

router = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket</title>
        <style>
            input:valid {
                background-color: palegreen;
            }

            input:invalid {
                background-color: lightpink;
            }
        </style>
    </head>
    <body>
        <h1>WebSocket robot</h1>
        <h2>Your robot: <span id="ws-id"></span></h2>
        <form action="" onsubmit="changeRobot(event)">
            <input type="text" id="robotSN" autocomplete="off" required="required" pattern="SN[0-9]{3}" value="SN000"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var robot_id = "SN000";
            var messages = document.getElementById('messages');
            document.querySelector("#ws-id").textContent = robot_id;

            var ws = new WebSocket(`ws://${window.location.host}/api/v1/data_gathering/ws/client/${robot_id}`);

            ws.onmessage = function(event) {
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
                if(messages.childElementCount>5) messages.removeChild(messages.firstChild);
            };

            function changeRobot(event) {
                robot_id = document.getElementById("robotSN").value
                ws.close();
                ws = new WebSocket(`ws://${window.location.host}/api/v1/data_gathering/ws/client/${robot_id}`);
                document.querySelector("#ws-id").textContent = robot_id;
                while(messages.firstChild){
                    messages.removeChild(messages.firstChild);
                }
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.clients_active_connections: Dict[WebSocket, str] = dict()
        self.robots_active_connections: Dict[WebSocket, str] = dict()

    async def connect(self, websocket: WebSocket, robot_serial_number: str, is_robot: bool = False):
        await websocket.accept()
        if is_robot:
            self.robots_active_connections[websocket] = robot_serial_number
            await self.broadcast("Connected", robot_serial_number)
        else:
            self.clients_active_connections[websocket] = robot_serial_number

    def disconnect(self, websocket: WebSocket):
        if websocket in self.robots_active_connections:
            self.robots_active_connections.pop(websocket)
        else:
            self.clients_active_connections.pop(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, robot_serial_number: str = None):
        if robot_serial_number:
            for connection, sn in self.clients_active_connections.items():
                if robot_serial_number == sn:
                    await connection.send_text(message)
        else:
            for connection, _ in self.clients_active_connections.items():
                await connection.send_text(message)


manager = ConnectionManager()


@router.get("/ws_robot_view", response_class=HTMLResponse)
async def get_web_socket_view():
    return HTMLResponse(html)


@router.websocket("/ws/client/{robot_serial_number}")
async def get_robot_websocket_endpoint(websocket: WebSocket, robot_serial_number: str):
    await manager.connect(websocket, robot_serial_number)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/robot/{robot_serial_number}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, robot_serial_number: str, session_id: str):
    await manager.connect(websocket, robot_serial_number, True)
    try:
        while True:
            data = await websocket.receive_json()
            await update_session(
                session_id,
                SessionUpdate(
                    end_time=datetime.now(pytz.timezone('Europe/Berlin'))
                )
            )
            data["session_id"] = session_id
            await manager.broadcast(f"{data}", robot_serial_number)
            for point_data in data["coordinate_with_extracted_weed"]:
                current_coordinate = point_data["current_coordinate"]
                path_point_number = point_data["path_point_number"]
                gps_point_id = await add_gps_point(
                    GPSPointIn(
                        latitude=current_coordinate[0],
                        longitude=current_coordinate[1],
                        quality=int(current_coordinate[2])
                    )
                )
                point_of_path_id = await add_point_of_path(
                    PointOfPathIn(
                        point_number=int(path_point_number),
                        session_id=int(session_id),
                        gps_point_id=gps_point_id
                    )
                )
                if "extracted_weeds" in point_data:
                    for weed_name, number in point_data["extracted_weeds"].items():
                        weed_type_id = await get_weed_type(
                            WeedTypeIn(
                                label=weed_name
                            )
                        )
                        await add_extracted_weed(
                            ExtractedWeedIn(
                                point_of_path_id=point_of_path_id,
                                session_id=int(session_id),
                                weed_type_id=weed_type_id.id,
                                number=int(number)
                            )
                        )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Disconnected", robot_serial_number)
