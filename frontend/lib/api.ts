import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const analyzeResume = async (file: File, jobDescription: string) => {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    const response = await apiClient.post('/api/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
