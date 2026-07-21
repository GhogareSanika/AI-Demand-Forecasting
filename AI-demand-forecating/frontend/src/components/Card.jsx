export default function Card({title,value}){

return(

<div className="bg-white rounded-lg shadow p-5">

<h3 className="text-gray-500">

{title}

</h3>

<p className="text-3xl font-bold">

{value}

</p>

</div>

);

}