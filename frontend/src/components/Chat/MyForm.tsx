import { useEffect, useState } from "react";
import { socket } from "../../socket";
import { jwtDecode } from "jwt-decode";


export function MyForm({ messages, setMessages }) {
    const [value, setValue] = useState("");
    const [user, setUser] = useState("");
    useEffect(() => { 
        const token = localStorage.getItem("Access Token");
        if (token) {
            const decoded: { username: string; [key: string]: any } =
                jwtDecode(token);
            setUser(decoded.username);
        }
    }, [])

    function onSubmit(event) {
        event.preventDefault();
        if (!value.trim()) return;

        setMessages((prev) => [...prev, { username: user, text: value }]);
        setValue("");

        socket.emit("message", { "user" : user, "message": value} , (response) => {
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
                    Send
                </button>
            </div>
        </form>
    );
}
