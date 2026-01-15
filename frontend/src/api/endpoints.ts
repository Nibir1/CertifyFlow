import { apiClient } from './client';
import type { FATProcedure, TechSpecPayload } from '../types';

/**
 * API Service Layer
 * -----------------
 * Encapsulates all backend communication logic.
 */
export const api = {
    /**
     * Sends raw text to the backend and returns structured JSON.
     */
    generateProcedure: async (payload: TechSpecPayload): Promise<FATProcedure> => {
        const response = await apiClient.post<FATProcedure>('/api/v1/generate', payload);
        return response.data;
    },

    /**
     * Sends the approved JSON to the backend and returns a PDF Blob.
     */
    generatePDF: async (procedure: FATProcedure): Promise<Blob> => {
        const response = await apiClient.post('/api/v1/generate-pdf', procedure, {
            responseType: 'blob', // Critical for handling binary file downloads
        });
        return response.data;
    }
};