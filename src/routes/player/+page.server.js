import { fetchSummoner, fetchMatches } from '$lib/riot.js';

export const load = async ({ url }) => {
	const gameName = url.searchParams.get('gameName');
	const tag = url.searchParams.get('tag');

	const summoner = await fetchSummoner(gameName, tag);
	const matches = await fetchMatches(summoner.puuid);

	const keepMain = [
		'allInPings',
		'assistMePings',
		'assists',
		'baronKills',
		'basicPings',
		'champLevel',
		'championId',
		'championName',
		'commandPings',
		'consumablesPurchased',
		'dangerPings',
		'deaths',
		'enemyMissingPings',
		'enemyVisionPings',
		'gameEndedInSurrender',
		'getBackPings',
		'goldEarned',
		'holdPings',
		'item0',
		'item1',
		'item2',
		'item3',
		'item4',
		'item5',
		'item6',
		'kills',
		'lane',
		'magicDamageDealtToChampions',
		'magicDamageTaken',
		'needVisionPings',
		'objectivesStolen',
		'onMyWayPings',
		'physicalDamageDealtToChampions',
		'physicalDamageTaken',
		'profileIcon',
		'pushPings',
		'riotIdGameName',
		'riotIdTagline',
		'summonerId',
		'summonerLevel',
		'timePlayed',
		'totalDamageDealtToChampions',
		'totalDamageShieldedOnTeammates',
		'totalDamageTaken',
		'totalHeal',
		'totalHealsOnTeammates',
		'totalMinionsKilled',
		'totalTimeCCDealt',
		'totalTimeSpentDead',
		'trueDamageDealtToChampions',
		'visionScore',
		'visionClearedPings',
		'visionWardsBoughtInGame',
		'wardsKilled',
		'wardsPlaced',
		'win'
	];

	const keepOthes = [
		'item0',
		'item1',
		'item2',
		'item3',
		'item4',
		'item5',
		'item6',
		'kills',
		'lane',
		'champLevel',
		'championId',
		'championName',
		'win'
	];

	for (let match of matches) {
		// for every match
		match.info.participants.forEach((player) => {
			// for every participant
			if (
				player.riotIdGameName === summoner.gameName &&
				player.riotIdTagline === summoner.tagLine
			) {
				// if is player researched
				Object.keys(player).forEach((property) => {
					// for each property
					if (!keepMain.includes(property)) delete player[property]; // remove the property if not in keep
				});
			} else {
				// if not the researched player
				Object.keys(player).forEach((property) => {
					// for each property
					if (!keepOthes.includes(property)) delete player[property]; // remove the property if not in keep
				});
			}
		});
	}

	return { summoner, matches };
};
