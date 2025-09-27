import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

type RegisterProps = {
    onLogin: (token: string) => void;
};

const Register = ({ onLogin }: RegisterProps) => {
    const navigate = useNavigate();
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [username, setUsername] = useState<string>("");

    const register = () => {
        if (!email.trim() || !password.trim() || !username.trim()) {
            alert("All fields are required");
            return;
        }

        axios
            .post("http://127.0.0.1:5000/auth/register", {
                username,
                email,
                password,
            })
            .then((res) => {
                const token = res.data.access_token; // make sure backend returns this
                if (token) {
                    localStorage.setItem("Access Token", token);
                    onLogin(token); // ✅ update App state
                    navigate("/chat/public");
                } else {
                    alert(
                        `Successfully registered ${username}. Please sign in.`
                    );
                    navigate("/auth/sign-in");
                }
            })
            .catch((err) =>
                alert(err.response?.data?.msg || "Registration failed")
            )
            .finally(() => {
                setEmail("");
                setUsername("");
                setPassword("");
            });
    };

    return (
        <div className="d-flex align-items-center justify-content-center h-75">
            <form className="form form-control w-25 d-flex flex-column">
                <h3>Sign Up</h3>

                <div className="mb-3">
                    <label>Username</label>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="mb-3">
                    <label>Email address</label>
                    <input
                        type="email"
                        className="form-control"
                        placeholder="Enter email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="mb-3">
                    <label>Password</label>
                    <input
                        type="password"
                        className="form-control"
                        placeholder="Enter password"
                        value={password}
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
                    Already registered? <a href="/auth/sign-in">Sign in</a>
                </p>
            </form>
        </div>
    );
};

export default Register;
