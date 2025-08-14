import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [name, setName] = useState("");
  useEffect(() => {

    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        console.log(response.data); 
        setName(response.data.name); 
      })
      .catch((error) => {
        console.error(error); // handle error
      })
      .finally(() => {
        console.log("Request completed"); // always executed
      });
  }, []);
  return (
    <div>Welcome {name}!</div>
  )
}
