import api from "./api";

// Get All Products
export const getProducts = async () => {
  const response = await api.get("/products");
  return response.data;
};

// Get Single Product
export const getProduct = async (id) => {
  const response = await api.get(`/products/${id}`);
  return response.data;
};

// Create Product
export const createProduct = async (productData) => {
  const response = await api.post("/products", productData);
  return response.data;
};

// Update Product
export const updateProduct = async (id, productData) => {
  const response = await api.patch(`/products/${id}`, productData);
  return response.data;
};

// Delete Product
export const deleteProduct = async (id) => {
  const response = await api.delete(`/products/${id}`);
  return response.data;
};