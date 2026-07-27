import { useState } from "react";
import { createProduct } from "../services/productService";

export default function ProductForm({ onProductAdded }) {
  const [formData, setFormData] = useState({
    product_name: "",
    category: "",
    store: "",
    department: "",
    current_stock: "",
    unit_price: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createProduct({
        ...formData,
        store: Number(formData.store),
        department: Number(formData.department),
        current_stock: Number(formData.current_stock),
        unit_price: Number(formData.unit_price),
      });

      alert("Product added successfully!");

      setFormData({
        product_name: "",
        category: "",
        store: "",
        department: "",
        current_stock: "",
        unit_price: "",
      });

      if (onProductAdded) {
        onProductAdded();
      }
    } catch (error) {
      console.error(error);
      alert("Failed to add product.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-xl shadow">

      <input
        type="text"
        name="product_name"
        placeholder="Product Name"
        value={formData.product_name}
        onChange={handleChange}
      />

      <input
        type="text"
        name="category"
        placeholder="Category"
        value={formData.category}
        onChange={handleChange}
      />

      <input
        type="number"
        name="store"
        placeholder="Store"
        value={formData.store}
        onChange={handleChange}
      />

      <input
        type="number"
        name="department"
        placeholder="Department"
        value={formData.department}
        onChange={handleChange}
      />

      <input
        type="number"
        name="current_stock"
        placeholder="Current Stock"
        value={formData.current_stock}
        onChange={handleChange}
      />

      <input
        type="number"
        name="unit_price"
        placeholder="Unit Price"
        value={formData.unit_price}
        onChange={handleChange}
      />

      <button type="submit">
        Add Product
      </button>

    </form>
  );
}