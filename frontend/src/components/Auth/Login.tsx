import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const navigate = useNavigate();


    const loginFunc = () => {
        if (!email.trim() || !password.trim()) {
            alert("Email/username and password are required");
            return;
        }

        try {
            axios.post("http://127.0.0.1:5000/auth/login", {
                "username": username,
                "email": email,
                "password": password,
            })
                .then((res) => localStorage.setItem("Access Token", res.data.access_token))
                .catch((err) => alert(err));
            
            navigate("/chat/public");

        } catch (err) {
            if (err.response) {
                alert(err.response.data.msg || "Invalid login credentials");
            } else {
                alert("Server unreachable");
            }
        } finally {
            setEmail("");
            setUsername("");
            setPassword("");
        }
    };

    return (
        <div className="d-flex justify-content-center align-items-center h-75">
            <form className="form form-control w-25">
                <h3>Sign In</h3>
                <div className="mb-3">
                    <label>Username</label>
                    <input
                        type="Username"
                        className="form-control"
                        placeholder="Enter Username"
                        value={username || ""}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label>Email address</label>
                    <input
                        type="email"
                        className="form-control"
                        placeholder="Enter email"
                        value={email || ""}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label>Password</label>
                    <input
                        type="password"
                        className="form-control"
                        placeholder="Enter password"
                        value={password || ""}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <div className="custom-control custom-checkbox">
                        <input
                            type="checkbox"
                            className="custom-control-input"
                            id="customCheck1"
                        />
                        <label
                            className="custom-control-label"
                            htmlFor="customCheck1"
                        >
                            Remember me
                        </label>
                    </div>
                </div>
                <div className="d-grid">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        onClick={(e) => { e.preventDefault(); loginFunc() }}
                    >
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Login;
