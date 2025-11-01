import axios from "axios"
//import { AccessibilityIcon } from "lucide-react"
import { ACCESS_TOKEN,REFRESH_TOKEN } from "./constants"
// const Base_URL = 'http://localhost:8000/api'

const isDevelopment = import.meta.env.MODE === 'development'
const Base_URL = isDevelopment ? import.meta.env.VITE_API_BASE_URL_LOCAL : import.meta.env.VITE_API_BASE_URL_DEPLOY
const apiRequest = axios.create({
    baseURL: Base_URL, 
    withCredentials: true,
})

apiRequest.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if(token){
            config.headers.Authorization =`Bearer ${token}`
        }
        return config
    },
    (error)=>{
        return Promise.reject(error)
    }
    )   

apiRequest.interceptors.response.use(
    (response) => {
        return response; // Pass successful responses through
    },
    async (error) => {
        const originalRequest = error.config;

        // Check for 401 error and ensure it's not the refresh request itself
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true; // Mark as retried
            const refreshToken = localStorage.getItem(REFRESH_TOKEN);

            if (!refreshToken) {
                // No refresh token, force logout (optional: redirect to login)
                localStorage.removeItem(ACCESS_TOKEN);
                // The error will be propagated, eventually handled by the calling component
                return Promise.reject(error); 
            }

            try {
                // 1. Attempt to refresh token
                const res = await axios.post(`${Base_URL}/auth/token/refresh/`, { // Use plain axios here to avoid interceptor recursion
                    refresh: refreshToken,
                });

                if (res.status === 200) {
                    // 2. Save new access token
                    const newAccessToken = res.data.access;
                    localStorage.setItem(ACCESS_TOKEN, newAccessToken);

                    // 3. Update the original request's header with the new token
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                    // 4. Retry the original request
                    return apiRequest(originalRequest); 
                }
            } catch (refreshError) {
                // If refresh fails (e.g., refresh token is expired/invalid)
                console.error("Token refresh failed, forcing logout:", refreshError);
                localStorage.removeItem(ACCESS_TOKEN);
                localStorage.removeItem(REFRESH_TOKEN);
                // Propagate the original error to be handled by the component
                return Promise.reject(error);
            }
        }

        return Promise.reject(error);
    }
);

export default apiRequest 