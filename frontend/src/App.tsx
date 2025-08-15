import { BrowserRouter, Route, Routes } from "react-router-dom";
import NotFound from "./components/NotFound";
import Register from "./components/Register";
import Login from "./components/Login";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="auth">
                    <Route path="sign-in" element={<Login />} />
                    <Route path="sign-up" element={<Register />} />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
