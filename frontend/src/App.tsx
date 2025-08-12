import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import User from "./components/User";
import Auth from "./pages/Auth";
import NotFound from "./components/NotFound";

function App() {
  return (
      <Router>
          <Routes>
              <Route path="/auth/*" element={<Auth />} />
              <Route path="/user/:userName/*" element={<User />} />
              <Route path="*" element={<NotFound />} />
          </Routes>
      </Router>
  );
}
export default App;
