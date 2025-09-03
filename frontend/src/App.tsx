import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import NotFound from "./components/Auth/NotFound";
import Register from "./components/Auth/Register";
import Login from "./components/Auth/Login";
import PublicRoom from "./components/Chat/PublicRoom";
import { jwtDecode } from "jwt-decode";

type ProtectedRouteProps = {
    jwt: string | null;
    children: React.ReactNode;
};

const ProtectedRoute = ({ jwt, children }: ProtectedRouteProps) => {
    if (!jwt) {
        return <div>Unauthorized Access</div>
    }
    try {
        jwtDecode(jwt);
        return children;
    }
    catch (error) {
        return <div>Unauthorized Access</div>
    }

}
export default function App() {
    
    const jwt = localStorage.getItem("Access Token") || null;
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/chat/public" replace />} />
                <Route path="auth">
                    <Route path="sign-in" element={<Login />} />
                    <Route path="sign-up" element={<Register />} />
                </Route>
                <Route path="chat">
                    <Route
                        path="public"
                        element={
                            <ProtectedRoute jwt={jwt}>
                                <PublicRoom />
                            </ProtectedRoute>
                        }
                    />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
