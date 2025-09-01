import React, { useState, useEffect } from "react";;
import { MyForm } from "./MyForm";
import MessageList from "./MessageList";

export default function PublicRoom() {
    const [messages, setMessages] = useState([]);

    return (
        <div className="PublicRoom">
            <MessageList messages={messages} setMessages={setMessages}/>
            <MyForm messages={messages} setMessages={setMessages}/>
        </div>
    );
}