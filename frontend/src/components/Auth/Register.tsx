import axios from "axios";
import { useState } from "react";

const Register = () => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [username, setUsername] = useState<string>("");

    const register = () => {
        if (
            email.trim() == "" ||
            password.trim() == "" ||
            username.trim() == ""
        ) {
            alert("At least one of the fields are empty");
        } else {
            setEmail("");
            setUsername("");
            setPassword("");
            axios.post("http://127.0.0.1:5000/register", {
                username: username,
                email: email,
                password: password,
            });
        }
    };
    return (
        <div className="d-flex align-items-center justify-content-center h-75">
            <form className="form form-control w-25 d-flex flex-column">
                <h3>Sign Up</h3>

                <div className="mb-3">
                    <label>Username</label>
                    <input
                        type="username"
                        className="form-control"
                        placeholder="Enter username"
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
                <div className="d-grid">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        onClick={(e) => {
                            e.preventDefault();
                            register();
                        }}
                    >
                        Register
                    </button>
                </div>
                <p className="forgot-password text-right">
                    Already registered <a href="/auth/sign-in">sign in?</a>
                </p>
            </form>
        </div>
    );
};

export default Register;
