import { token } from './stores';
import { get } from 'svelte/store';

const headers = () => ({
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${get(token)}`
});

const paths = {
  enrol: 'api/enrol',
  features: 'api/features',
  students: 'api/student',
  courses: 'api/course',
  years: 'api/year',
  allEvents: 'api/event/all'
};

const postRequest = (path, payload) => fetch(process.env.API_URL + path, {
  method: 'POST',
  headers: headers(),
  body: JSON.stringify(payload)
});
const getRequest = (path) => fetch(process.env.API_URL + path, {
  method: 'GET',
  headers: headers(),
});

export const postEnrol = (payload) => postRequest(paths.enrol, payload);
export const postFeatures = (payload) => postRequest(paths.features, payload);

export const getStudents = () => getRequest(paths.students);
export const getYears = () => getRequest(paths.years);
export const getCourses = () => getRequest(paths.courses);
export const getAllEvents = () => getRequest(paths.allEvents);
export const getAttendance = (eventID) => getRequest(`api/attendance?event=${eventID}`);

// Public routes
export const userLogin = (email, password) => fetch(process.env.API_URL + `user/login?email=${email}&password=${password}`);

