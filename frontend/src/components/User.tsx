import axios from "axios";
import { useEffect, useState } from "react";
import { Outlet, useParams } from "react-router-dom";

const api = axios.create({
    baseURL: "http://127.0.0.1:5000",
    timeout: 1000,
});

const User = () => {
    const [user, setUser] = useState<string>("Backend data");
    const { userName } = useParams();
    useEffect(() => {
        api.get(`/users/${userName}`).then((res) => {
            console.log(res.data.name);
            setUser(res.data.name);
        });
    }, [userName]);
    return (
        <div>
            <h1> Hello {userName}</h1>
            <Outlet />
            {user}
        </div>
    );
};

export default User;
