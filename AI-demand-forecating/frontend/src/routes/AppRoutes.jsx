import { Routes,Route } from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import Products from "../pages/Products";
import Prediction from "../pages/Predictions";
import History from "../pages/History";
import Settings from "../pages/Settings";

export default function AppRoutes(){

return(

<Routes>

<Route path="/" element={<Dashboard/>}/>
<Route path="/products" element={<Products/>}/>
<Route path="/prediction" element={<Prediction/>}/>
<Route path="/history" element={<History/>}/>
<Route path="/settings" element={<Settings/>}/>

</Routes>

);

}