import { json } from '@sveltejs/kit';
import { fetchRank } from '$lib/riot.js'

export async function GET({ url }) {
    try {
        const summonerID = url.searchParams.get('summonerId')
        const data = await fetchRank(summonerID)
        return json(data)
    } catch (err) {
        console.error("error while fetching rank", err)
    }
}