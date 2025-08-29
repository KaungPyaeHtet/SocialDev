import { BrowserRouter, Route, Routes } from "react-router-dom";
import NotFound from "./components/Auth/NotFound";
import Register from "./components/Auth/Register";
import Login from "./components/Auth/Login";
import PublicRoom from "./components/Chat/PublicRoom";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="auth">
                    <Route path="sign-in" element={<Login />} />
                    <Route path="sign-up" element={<Register />} />
                </Route>
                <Route path="chat">
                    <Route path="public" element={<PublicRoom />} />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
