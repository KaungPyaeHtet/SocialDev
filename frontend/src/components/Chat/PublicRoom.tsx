import { useEffect, useState } from "react";
import { socket } from "../../socket"

const PublicRoom = () => {
    const [isConnected, setIsConnected] = useState(socket.connected);
    const [joinEvents, setJoinEvents] = useState([]);
    useEffect(() => {
        function onConnect() {
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
        }

        function onJoinEvent(value) {
            // setJoinEvents((previous) => [...previous, value]);
            console.log(value);
        }
        
        socket.on("connect", onConnect);
        socket.on("disconnect", onDisconnect);
        socket.emit("join", { data: "Hello, Server!" });
        socket.on("handle_response", onJoinEvent);

        return () => {
            socket.off("connect", onConnect);
            socket.off("disconnect", onDisconnect);
            socket.off("join", onJoinEvent);
        };
    }, []);

  return (
    <div>PublicRoom</div>
  )
}

export default PublicRoom