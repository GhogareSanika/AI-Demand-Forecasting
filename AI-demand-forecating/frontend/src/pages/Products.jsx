import { useEffect, useState } from "react";
import { getProducts } from "../services/productService";

export default function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await getProducts();
      console.log(data);
      setProducts(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Products</h1>

      {products.map((product) => (
        <div key={product.id}>
          {product.product_name}
        </div>
      ))}
    </div>
  );
}