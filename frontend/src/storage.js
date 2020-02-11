export const storage = {
  getItem: key => localStorage.getItem(key),
  setItem: (key, val) => localStorage.setItem(key, val),
  removeItem: key => localStorage.removeItem(key),
};
