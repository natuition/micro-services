from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.api.models.gps_point import GPSPointIn
from app.api.models.point_of_path import PointOfPathIn
from app.api.models.weed_type import WeedTypeIn
from app.api.models.extracted_weed import ExtractedWeedIn
from app.api.database.db_manager import add_gps_point, add_point_of_path, get_weed_type, add_extracted_weed


router = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket</title>
    </head>
    <body>
        <h1>WebSocket robot</h1>
        <!--<h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>-->
        <ul id='messages'>
        </ul>
        <script>
            var session_id = "_"
            var ws = new WebSocket(`ws://localhost:8080/api/v1/data_gathering/ws/${session_id}/0`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/ws_robot_view")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{robot_serial_number}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, robot_serial_number: str, session_id: str):
    """
    {
        "coordinate_with_extracted_weed": [
            {
                "extracted_weeds": { "Plantain": 2 },
                "path_point_number": 10,
                "current_coordinate": [52.347466706444635, 4.945731782212521, 4] #[lati, longi, point_quality]
            },
            {
                "path_point_number": 11,
                "current_coordinate": [52.34762624, 4.945991120000001, 4]
            },
            {
                "extracted_weeds": { "Daisy": 1 },
                "path_point_number": 12,
                "current_coordinate": [52.34752468000001, 4.946158540000001, 4]
            },
            {
                "path_point_number": 13,
                "current_coordinate": [52.34736514682898, 4.94589920139857, 2]
            }
        ]
    }
    """
    await manager.connect(websocket)
    if robot_serial_number != "_":
        await manager.broadcast(f"Session n°{session_id} [{robot_serial_number}] connected.")
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(f"Session n°{session_id} [{robot_serial_number}] : {data}")
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
        if robot_serial_number != "_":
            await manager.broadcast(f"Session n°{session_id} [{robot_serial_number}] deconnected.")
