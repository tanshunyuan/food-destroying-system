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
  setitem: 'api/setitem'
};

const postRequest = (path, payload) => fetch(process.env.API_URL + path, {
  method: 'POST',
  body: JSON.stringify(payload)
});
const getRequest = (path) => fetch(process.env.API_URL + path, {
  method: 'GET'
});

export const postFood = (payload) => postRequest(paths.order, payload);
//export const postFeatures = (payload) => postRequest(paths.features, payload);

export const getManagers = () => getRequest(paths.manager);
export const getEmployees = () => getRequest(paths.employee);
export const getFoods = () => getRequest(paths.food);
export const getCategorys = () => getRequest(paths.category);
//export const getAttendance = (eventID) => getRequest(`api/attendance?event=${eventID}`);

// Public routes
export const userLogin = (email, password) => fetch(process.env.API_URL + `login?email=${email}&password=${password}`);

