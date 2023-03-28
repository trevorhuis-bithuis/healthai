import axios from 'axios';

const api = axios.create({
  baseURL: 'https://healthai.fly.dev'
});


export default api;
