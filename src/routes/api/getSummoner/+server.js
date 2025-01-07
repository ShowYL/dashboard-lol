import { json } from '@sveltejs/kit';
import { fetchSummoner } from '$lib/riot.js';

/** @type {import('./$types.js').RequestHandler} */
export async function GET({ url }) {
	const riotID = url.searchParams.get('riotID');
	const tag = url.searchParams.get('tag');

	const res = await fetchSummoner(riotID, tag);

	return json(res);
}
