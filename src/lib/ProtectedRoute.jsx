// ProtectedRoute.jsx (Simplified)

import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "./constants";
import React, { useState, useEffect } from "react";
// apiRequest is no longer needed for direct refresh

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    // --- Checks Authorization Status (Simplified) ---
    const auth = () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        
        if (!token) {
            setIsAuthorized(false);
            return;
        }

        try {
            // Check for client-side expiration *without* trying to refresh
            const decoded = jwtDecode(token);
            const tokenExpiration = decoded.exp;
            const now = Date.now() / 1000;

            if (tokenExpiration < now) {
                 setIsAuthorized(true); // Let API call handle the refresh
            } else {
                setIsAuthorized(true);
            }
        } catch (error) {
            // Handle decode errors (e.g., malformed token)
            console.error("Authorization check failed:", error);
            localStorage.removeItem(ACCESS_TOKEN); // Clear bad token
            setIsAuthorized(false);
        }
    };
    
    useEffect(() => {
        auth();
    }, []);

    if (isAuthorized === null) {
        return <div>Loading...</div>;
    }

    return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;