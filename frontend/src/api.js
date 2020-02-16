import { token } from './stores';
import { get } from 'svelte/store';

const headers = () => ({
  'Accept': 'application/json',
  'Content-Type': 'application/json'
});

const paths = {
  manager: 'api/manager',
  employee: 'api/employee',
  food: 'api/food',
  category: 'api/category',
  setitem: 'api/setitem',
  setmenu: 'api/setmenu',
  getfood: 'api/food/all',
  getcategory: 'api/category/all',
  getsetitems: 'api/setitem/all',
  getsetmenu: 'api/setmenu/all',
  addcategorytofood: 'api/food/category',
  addsetitemtosetmenu: 'api/setitem/setmenu',
  addfoodtosetitem: 'api/food/setitem',
  getOrders: 'api/order/all'
};

//const API_URL = 'http://localhost:5000/'

const postRequest = (path, payload) => fetch(process.env.API_URL  + path, {
  method: 'POST',
  headers: headers(),
  body: JSON.stringify(payload)
});
const getRequest = (path) => fetch(process.env.API_URL + path, {
  method: 'GET'
});
const putRequest = (path, payload) => fetch(process.env.API_URL  + path, {
  method: 'PUT',
  headers: headers(),
  body: JSON.stringify(payload)
});
const deleteRequest = (path, payload) => fetch(process.env.API_URL  + path, {
  method: 'DELETE',
  headers: headers(),
  body: JSON.stringify(payload)
});

export const postFood = (payload) => postRequest(paths.food, payload);
export const postCategory = (payload) => postRequest(paths.category, payload);
export const postSetMenu = (payload) => postRequest(paths.setmenu, payload);
export const postFoodToCategory = (payload) => postRequest(paths.addcategorytofood, payload);
export const postSetitemToSetmenu= (payload) => postRequest(paths.addsetitemtosetmenu, payload);
export const postFoodToSetitem= (payload) => postRequest(paths.addfoodtosetitem, payload);

export const getManagers = () => getRequest(paths.manager);
export const getEmployees = () => getRequest(paths.employee);
export const getFoods = () => getRequest(paths.getfood);
export const getCategorys = () => getRequest(paths.getcategory);
export const getSetItems = () => getRequest(paths.getsetitems);
export const getSetMenus= () => getRequest(paths.getsetmenu);

export const updateFood = (payload) => putRequest(paths.food, payload);
export const deleteFood = (payload) => deleteRequest(paths.food, payload);

export const updateOrderStatus = (payload) => putRequest(paths.order, payload);

// Public routes
export const userLogin = (email, password) => fetch(process.env.API_URL + `login?email=${email}&password=${password}`);

