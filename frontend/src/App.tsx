import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import NotFound from "./components/Auth/NotFound";
import Register from "./components/Auth/Register";
import Login from "./components/Auth/Login";
import PublicRoom from "./components/Chat/PublicRoom";

type ProtectedRouteProps = {
    user: string | null;
    children: React.ReactNode;
};

const ProtectedRoute = ({ user, children }: ProtectedRouteProps) => {
  if (!user) {
    return <div>Unauthorized Access</div>
  }

  return children;
}
export default function App() {
    
    
    const user = localStorage.getItem("Access Token") || null;
    return (
        <BrowserRouter>
            <Routes>
                <Route path="auth">
                    <Route path="sign-in" element={<Login />} />
                    <Route path="sign-up" element={<Register />} />
                </Route>
                <Route path="chat">
                    <Route path="public" element={
                        <ProtectedRoute user={user}> 
                    <PublicRoom />
                </ProtectedRoute>} />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
