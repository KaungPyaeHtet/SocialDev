import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import NotFound from "./components/Auth/NotFound";
import Register from "./components/Auth/Register";
import Login from "./components/Auth/Login";
import PublicRoom from "./components/Chat/PublicRoom";
import { jwtDecode } from "jwt-decode";
import Navbar from "./components/Navbar";
import { useEffect, useState } from "react";
import "./App.css"
import ProtectedRoute from "./components/ProtectedRoute";

type ProtectedRouteProps = {
    jwt: string | null;
    children: React.ReactNode;
};


export default function App() {
    
    const [jwt, setJwt] = useState<string | null>(
        localStorage.getItem("Access Token")
    );

    useEffect(() => {
        const handleStorageChange = () => {
            setJwt(localStorage.getItem("Access Token"));
        };

        window.addEventListener("storage", handleStorageChange);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
        };
    }, []);

    return (
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route
                    path="/"
                    element={<Navigate to="/chat/public" replace />}
                />
                <Route path="auth">
                    <Route
                        path="sign-in"
                        element={<Login onLogin={setJwt} />}
                    />
                    <Route
                        path="sign-up"
                        element={<Register onLogin={setJwt} />}
                    />
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
