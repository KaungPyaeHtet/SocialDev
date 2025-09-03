import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
    const navigate = useNavigate();
    const jwt = localStorage.getItem("Access Token");

    const handleLogout = () => {
        localStorage.removeItem("Access Token");
        navigate("/auth/sign-in");
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
            <Link className="navbar-brand" to="/">
                ChatApp
            </Link>

            <div className="collapse navbar-collapse">
                <ul className="navbar-nav me-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="/chat/public">
                            Public Chat
                        </Link>
                    </li>
                </ul>
                <ul className="navbar-nav ms-auto">
                    {!jwt ? (
                        <>
                            <li className="nav-item">
                                <Link className="nav-link" to="/auth/sign-in">
                                    Login
                                </Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/auth/sign-up">
                                    Register
                                </Link>
                            </li>
                        </>
                    ) : (
                        <li className="nav-item">
                            <button
                                className="btn btn-outline-light"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </li>
                    )}
                </ul>
            </div>
        </nav>
    );
}
