import { PANTRY_API_KEY } from '$env/static/private';

export async function fetchDataPantry() {
	const response = await fetch(
		`https://getpantry.cloud/apiv1/pantry/${PANTRY_API_KEY}/basket/Changes`
	);
	if (!response.ok) {
		throw new Error('Error while fetching pantry');
	}
	return response.json();
}
