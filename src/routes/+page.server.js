import { fetchDataPantry } from '$lib/pantry.js';

export const load = async () => {
	const fetchedPantryData = await fetchDataPantry();
	return { fetchedPantryData };
};
