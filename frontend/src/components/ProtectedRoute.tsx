import { jwtDecode } from "jwt-decode";
import HomePage from "./HomePage";

interface ProtectedRouteProps {
    jwt: string | null;
    children: React.ReactNode;
}

const ProtectedRoute = ({ jwt, children }: ProtectedRouteProps) => {
    if (!jwt) {
        return <HomePage />;
    }
    try {
        jwtDecode(jwt);
        return children;
    } catch (error) {
        return <HomePage />;
    }
};

export default ProtectedRoute;