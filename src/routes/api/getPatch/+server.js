import { json } from '@sveltejs/kit';
import { fetchPantryPatch } from '$lib/pantry.js';

export async function GET(){
    try {
        const patch = await fetchPantryPatch();
        const transformedPatch = patch.split('-').join('.') + ".1";
        return json({ patch: transformedPatch });
    } catch (error) {
        console.error('Error while fetching patch:', error);
    }
}