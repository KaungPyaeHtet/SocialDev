import { useState } from "react";
import { socket } from "../../socket";


export function MyForm({ messages, setMessages }) {
    const [value, setValue] = useState("");

    function onSubmit(event) {
        event.preventDefault();
        if (!value.trim()) return;

        setMessages((prev) => [...prev, { username: "You", text: value }]);
        setValue("");

        socket.emit("message", value, (response) => {
            console.log("server response:", response);
        });
    }

    return (
        <form onSubmit={onSubmit} className="p-3">
            <div className="input-group">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Type your message..."
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                />
                <button
                    className="btn btn-primary"
                    type="submit"
                >
                    {"Send"}
                </button>
            </div>
        </form>
    );
}
