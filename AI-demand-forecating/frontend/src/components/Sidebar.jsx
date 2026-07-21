import { Link } from "react-router-dom";

export default function Sidebar(){

return(

<div className="w-64 h-screen bg-blue-700 text-white">

<h1 className="text-2xl font-bold p-5">

DemandAI

</h1>

<nav className="flex flex-col">

<Link to="/" className="p-4 hover:bg-blue-600">

Dashboard

</Link>

<Link to="/products" className="p-4 hover:bg-blue-600">

Products

</Link>

<Link to="/prediction" className="p-4 hover:bg-blue-600">

Prediction

</Link>

<Link to="/history" className="p-4 hover:bg-blue-600">

History

</Link>

<Link to="/settings" className="p-4 hover:bg-blue-600">

Settings

</Link>

</nav>

</div>

);

}