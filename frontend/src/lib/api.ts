const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

interface ApiResponse<T> {
    data: T;
    error: string | null;
}

class ResponseError extends Error {
    status?: number;
}

const handleResponse = async <T>(response: Response): Promise<ApiResponse<T>> => {
    const contentType = response.headers.get('Content-Type');
    const isJson = contentType && contentType.includes('application/json');

    if (!response.ok) {
        let error: ResponseError;
        const errorData = isJson ? await response.json() : { detail: response.statusText };

        if (typeof errorData === 'string') {
            error = new ResponseError(errorData);
        } else {
            const [msg] = Object.values(errorData);
            error = new ResponseError(msg as string);
        }
        error.status = response.status;
        throw error;
    }

    const data = isJson ? await response.json() : await response.text();
    return { data, error: null };
};

const api = {
    get: async <T>(url: string, headers: Record<string, string> = {}): Promise<ApiResponse<T>> => {
        const response = await fetch(`${API_BASE_URL}${url}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        });
        return handleResponse<T>(response);
    },

    post: async <T>(url: string, data: any, headers?: Record<string, string>): Promise<ApiResponse<T>> => {
        const isFormData = data instanceof FormData;
        const response = await fetch(`${API_BASE_URL}${url}`, {
            method: 'POST',
            headers: {
                ...(!isFormData && { 'Content-Type': 'application/json' }),
                ...headers,
            },
            body: isFormData ? data : JSON.stringify(data),
        });
        return handleResponse<T>(response);
    },

    put: async <T>(url: string, data: any, headers: Record<string, string> = {}): Promise<ApiResponse<T>> => {
        const isFormData = data instanceof FormData;
        const response = await fetch(`${API_BASE_URL}${url}`, {
            method: 'PUT',
            headers: {
                ...(!isFormData && { 'Content-Type': 'application/json' }),
                ...headers,
            },
            body: isFormData ? data : JSON.stringify(data),
        });
        return handleResponse<T>(response);
    },

    delete: async <T>(url: string, headers: Record<string, string> = {}): Promise<ApiResponse<T>> => {
        const response = await fetch(`${API_BASE_URL}${url}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                ...headers,
            },
        });
        return handleResponse<T>(response);
    },
};

export default api;
