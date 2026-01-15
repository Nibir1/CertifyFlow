import axios from 'axios';

/**
 * Axios Client Instance
 * ---------------------
 * Configured with the base URL from environment variables.
 * In Docker, this points to localhost:8000 via the browser.
 */
export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30s timeout for the AI generation which can be slow
});