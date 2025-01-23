import { writable } from 'svelte/store';

export const menuVisible = writable(false);

export const statsDisplay = writable('overview');