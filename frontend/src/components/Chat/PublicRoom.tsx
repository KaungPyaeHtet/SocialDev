import React, { useState, useEffect } from "react";;
import { socket } from "../../socket";
import { MyForm } from "./MyForm";
import { ConnectionManager } from "./ConnectionManager";
import { ConnectionState } from "./ConnectionState";
import MessageList from "./MessageList";

export default function PublicRoom() {
    const [isConnected, setIsConnected] = useState(socket.connected);

    useEffect(() => {
        function onConnect() {
            console.log("CONNENCt")
            setIsConnected(true);
        }

        function onDisconnect() {
            setIsConnected(false);
        }

        socket.on("connect", onConnect);
        socket.on("disconnect", onDisconnect);

        return () => {
            socket.off("connect");
            socket.off("disconnect");
        };
    }, []);

    return (
        <div className="PublicRoom">
            <ConnectionState isConnected={isConnected} />
            <ConnectionManager />
            <MessageList />
            <MyForm />
        </div>
    );
}