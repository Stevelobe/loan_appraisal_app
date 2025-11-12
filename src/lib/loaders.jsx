
import apiRequest from "./apiRequest";
import { redirect } from "react-router-dom";
import { ACCESS_TOKEN } from "./constants"; 
export const dashboardLoader = async ({ request, params }) => {
  // Use Promise.all to fetch multiple data concurrently
  try{
        const [allUsers, allCategories, allProducts] = await Promise.all([
        apiRequest.get("/auth/allusers/"),
        apiRequest.get("/categories/"), 
        apiRequest.get("/products/") 
      ]);

      // Return the data from all responses
      return {
        users: allUsers.data,
        categories: allCategories.data,
        products: allProducts.data
      };
  }catch(error){
        if (error.response?.status === 401 || error.response?.status === 400) {
            console.error("Token refresh failed. Forcing logout and redirect.");
            throw redirect("/harmonia-login-employee-secret"); 
        }
        throw error;
  }
};

export const singleProductLoader = async ({ request, params }) => {
  const [ allCategories, allProduct] = await Promise.all([
    apiRequest.get("/categories/"), 
    apiRequest.get("/products/" + params.productId)
  ]);

  // Return the data from all responses
  return {
    categories: allCategories.data,
    product: allProduct.data
  };

};

export const allLoans = async ({ request, params }) => {
  const res = await apiRequest.get("/calculator/all-loan/" );
  return res.data;
};

export const projectsLoader = async ({ request, params }) => {
  const res = await apiRequest.get("/projects/");
    return res.data
};

export const productsLoader = async ({ request, params }) => {
  const res = await apiRequest.get("/products/");
    return res.data
};

export function authGuardLoader() {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
        throw redirect("/login");
    }
    return null;
}