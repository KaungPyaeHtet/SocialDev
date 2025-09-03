import { useEffect } from 'react'
import { socket } from '../../socket';

const MessageList = ({messages, setMessages}) => {

    useEffect(() => {
        function onChatEvent(data) {
            console.log("data", data)
            setMessages(prev => [...prev, { username: data.username, text: data.message }])
        }
        socket.on("chat", onChatEvent);
        return () => {
            socket.off("chat", onChatEvent);
        };
    }, [messages]);
    
  return (
      <div className="d-flex justify-content-center" style={{height: "80vh"}}>
          <div className="w-50 vh-50">
              <div className="card shadow-sm h-100">
                  <div className="card-header bg-primary text-white">
                      Chat Messages
                  </div>
                  <ul className="list-group list-group-flush overflow-auto h-100">
                      {messages.length > 0 ? (
                          messages.map((msg, id) => (
                              <li
                                  key={id}
                                  className="list-group-item d-flex justify-content-between align-items-center"
                              >
                                  <span>
                                      <strong className="text-primary">
                                          {msg.username}
                                      </strong>
                                      : {msg.text}
                                  </span>
                              </li>
                          ))
                      ) : (
                          <li className="list-group-item text-center text-muted">
                              No messages yet
                          </li>
                      )}
                  </ul>
              </div>
          </div>
      </div>
  );
}

export default MessageList