import { useEffect, useState } from "react";
import axios from "axios";

export default function UserComponent() {
  const [name, setName] = useState("");
  useEffect(() => {
    // First example
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        console.log(response.data); // handle success
        setName(response.data.name); // assuming the response has a 'name' field
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
