import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import AppRoutes from "./routes/AppRoutes";

export default function App(){

return(

<div className="flex">

<Sidebar/>

<div className="flex-1">

<Navbar/>

<div className="p-6">

<AppRoutes/>

</div>

</div>

</div>

);

}