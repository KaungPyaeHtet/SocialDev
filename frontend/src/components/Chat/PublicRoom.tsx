import React, { useState, useEffect } from "react";;
import { socket } from "../../socket";
import { MyForm } from "./MyForm";
import MessageList from "./MessageList";

export default function PublicRoom() {
    const [isConnected, setIsConnected] = useState(socket.connected);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        function onConnect() {
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
            <MessageList messages={messages} setMessages={setMessages}/>
            <MyForm messages={messages} setMessages={setMessages}/>
        </div>
    );
}