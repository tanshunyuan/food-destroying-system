import { writable } from 'svelte/store'
import { storage } from './storage'

const createTokenStore = ()  => {
  const localTokenStore = storage.getItem('token');

  const {subscribe, set, update} = writable(localTokenStore);

  return {
    subscribe,
    set: token => {
      storage.setItem('token', token);
      set(token);
    },
    unset: () => {
      storage.removeItem('token');
      set(null);
    },
    update: token => {
      storage.setItem('token', token);
      update(token);
    }
  };
};

const createUserStore = () => {
  const localUserStore = JSON.parse(storage.getItem('user'));

  const {subscribe, set, update} = writable(localUserStore);

  return {
    subscribe,
    set: user => {
      console.info(user);
      storage.setItem('user', JSON.stringify(user));
      set(user);
    },
    unset: () => {
      storage.removeItem('user');
      set(null);
    },
    update: user => {
      storage.setItem('user', user); update(user);
      set(user);
    }
  }
};

export const token = createTokenStore();
export const user = createUserStore();
export const userMessage = writable('');
export const selectedEvent = writable('');
