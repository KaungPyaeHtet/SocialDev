import { useState } from "react";
import { socket } from "../../socket";


export function MyForm({ messages, setMessages }) {
    const [value, setValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    function onSubmit(event) {
        event.preventDefault();
        if (!value.trim()) return;

        setMessages((prev) => [...prev, { username: "You", text: value }]);
        setValue("");
        setIsLoading(true);

        socket.emit("message", value, (response) => {
            console.log("server response:", response);
            setIsLoading(false);
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
                    disabled={isLoading}
                />
                <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={isLoading || !value.trim()}
                >
                    {isLoading ? "Sending..." : "Send"}
                </button>
            </div>
        </form>
    );
}
