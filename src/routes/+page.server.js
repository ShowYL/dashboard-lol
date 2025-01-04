import { fetchData } from "$lib/pantry.js";

export const load = ( async () => {
    const fetchedPantryData = await fetchData();
    return {fetchedPantryData};
})