import { token } from './stores';
import { get } from 'svelte/store';

const headers = () => ({
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${get(token)}`
});

const paths = {
  manager: 'api/manager',
  employee: 'api/employee',
  food: 'api/food',
  category: 'api/category',
  setitem: 'api/setitem',
  getOrders: 'api/order/all'
};

const API_URL = 'http://localhost:5000/'

const postRequest = (path, payload) => fetch(API_URL + path, {
  method: 'POST',
  body: JSON.stringify(payload)
});
const getRequest = (path) => fetch(API_URL + path, {
  method: 'GET'
});
const putRequest = (path, payload) => fetch(process.env.API_URL  + path, {
  method: 'PUT',
  headers: headers(),
  body: JSON.stringify(payload)
});

export const postFood = (payload) => postRequest(paths.order, payload);

export const getManagers = () => getRequest(paths.manager);
export const getEmployees = () => getRequest(paths.employee);
export const getFoods = () => getRequest(paths.food);
export const getCategorys = () => getRequest(paths.category);
export const getOrders = () => getRequest(paths.getOrders);

export const updateOrderStatus = (payload) => putRequest(paths.order, payload);

// Public routes
export const userLogin = (email, password) => fetch(API_URL + `login?email=${email}&password=${password}`);

