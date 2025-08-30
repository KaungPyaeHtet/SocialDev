import React, { useEffect, useState } from 'react'
import { socket } from '../../socket';

const MessageList = () => {
    const [messages, setMessages] = useState([]);
    const [user, setUser] = useState();

    useEffect(() => {
        function onChatEvent(data) {
            console.log(data.username)
            setUser(data.username);
            setMessages(prev => [...prev, data.message])
        }
        socket.on("chat", onChatEvent);
        return () => {
            socket.off("chat");
        };
    }, []);
  return (
      <div>
          {user ? messages.map((message, id) => <ul>
              <li key={id}>{user} | {message}</li>
          </ul>) : <div>SHIT</div>}
    </div>
  )
}

export default MessageList