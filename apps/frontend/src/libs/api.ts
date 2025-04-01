import axios from 'axios';

export const API = axios.create({
    baseURL: 'http://localhost:8000',
});

API.interceptors.request.use(
    (config) => {
        if (config.params) {
            const queryParams = new URLSearchParams(config.params).toString();
            config.url = `${config.url}?${queryParams}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    },
);
