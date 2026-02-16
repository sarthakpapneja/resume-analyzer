import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export async function analyzeResume(file: File, jobDescription: string, jdFile: File | null, githubUrl: string): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append("resume", file);
    if (jobDescription) formData.append("job_description", jobDescription);
    if (jdFile) formData.append("jd_file", jdFile);
    if (githubUrl) formData.append("github_url", githubUrl);

    const response = await fetch("http://localhost:8001/api/analyze", {
        method: 'POST',
        body: formData,
        // When sending FormData, fetch automatically sets the 'Content-Type' header
        // with the correct boundary. Manually setting it can cause issues.
        // The original instruction included it, but it's typically omitted for FormData.
        // If the backend requires it explicitly, it might be a server-side expectation.
        // For now, I'll remove it as it's the standard practice for fetch with FormData.
        // headers: {
        //     'Content-Type': 'multipart/form-data',
        // },
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}
