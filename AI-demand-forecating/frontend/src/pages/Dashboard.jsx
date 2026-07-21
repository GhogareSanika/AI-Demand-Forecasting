import { useEffect } from "react";
import axios from "../services/api";

export default function Dashboard() {
  useEffect(() => {
    axios.get("/health")
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return <h1>Dashboard</h1>;
}