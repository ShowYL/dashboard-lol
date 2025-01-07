import { RIOT_API_KEY } from '$env/static/private';

export async function fetchSummoner(gameName, tag) {
	const response = await fetch(
		`https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/${gameName}/${tag}?api_key=${RIOT_API_KEY}`
	);
	if (!response.ok) {
		const errorText = await response.text()
		console.error(`Error while fetching summoner: ${response.status} - ${errorText}`);
		throw new Error('Error while fetching summoner');
	}
	return await response.json();
}

export async function fetchMatches(puuid) {
	const response = await fetch(
		`https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}/ids?start=0&count=20&api_key=${RIOT_API_KEY}`
	);
	if (!response.ok) {
		throw new Error('Error while fetching matches');
	}

	const data = await response.json();
	let tabmatches = [];

	for (const element of data) {
		const getmatchResponse = await fetch(
			`https://europe.api.riotgames.com/lol/match/v5/matches/${element}?api_key=${RIOT_API_KEY}`
		);

		if (!getmatchResponse.ok) {
			throw new Error(`Error while fetching match for ${puuid}`);
		}

		const matchData = await getmatchResponse.json();
		tabmatches.push(matchData);
	}

	return tabmatches;
}
