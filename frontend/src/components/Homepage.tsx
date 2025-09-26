import { Link } from "react-router-dom";

export default function HomePage() {
    return (
        <div className="home-container">
            <div className="home-content">
                <h1 className="home-title">Welcome to ChatApp 💬</h1>
                <p className="home-subtitle">
                    Connect, chat, and share instantly with friends and the
                    community.
                </p>
                <div className="home-buttons">
                    <Link to="/auth/sign-in" className="btn btn-login">
                        Login
                    </Link>
                    <Link to="/auth/sign-up" className="btn btn-register">
                        Register
                    </Link>
                </div>
            </div>
        </div>
    );
}