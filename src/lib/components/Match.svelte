<script>
	import { onMount } from 'svelte';
	import splashPosition from './SplashPosition.js';
	import { statsDisplay,menuVisible } from './shared.js';

	let { match, summonerName, tag } = $props();

	let win = $state('');
	let champion = $state('');
	let urlSplash = $state('');
	let kills = $state('');
	let assists = $state('');
	let deaths = $state('');
	let cs = $state('');
	let id = $state('overview');
	let gameDuration = match.info.gameDuration;
	let csMIN = $derived((Math.round(cs / (gameDuration / 600)) / 10).toString().replace('.', ','));

	function cardBackground(urlSplash, win) {
		if (win) {
			return `linear-gradient(to bottom, rgba(100, 149, 237, 0),rgba(100, 149, 237,0.6) 80%, rgba(100, 149, 237, 1) 100%), url(${urlSplash})`;
		} else {
			return `linear-gradient(to bottom, rgba(237, 50, 50, 0) 0%, rgba(237, 50, 50, 0.1) 35%, rgba(237, 50, 50, 0.3) 60%, rgba(237, 50, 50, 0.6) 80%, rgba(237, 50, 50, 1) 100%), url(${urlSplash})`;
		}
	}

	onMount(() => {
		match.info.participants.forEach((player) => {
			if (player.riotIdGameName === summonerName && player.riotIdTagline === tag) {
				win = player.win;
				champion = player.championName;
				kills = player.kills;
				assists = player.assists;
				deaths = player.deaths;
				cs = player.totalMinionsKilled + player.neutralMinionsKilled;
			}
		});
		id = match.metadata.matchId;
		urlSplash = `https://ddragon.leagueoflegends.com/cdn/img/champion/centered/${champion}_0.jpg`;
	});
</script>

<div class="flex h-1/5 w-full flex-row items-center justify-center" onclick={() => {$statsDisplay = id; $menuVisible = false}}>
	<div
		class="ml-4 h-5/6 w-3/5 rounded-2xl bg-cover {splashPosition[champion]
			? splashPosition[champion]
			: 'bg-center'} h-1/5 bg-no-repeat"
		style="background-image : {cardBackground(urlSplash, win)}"
	></div>
	<div class="mt-4 flex h-full w-2/5 flex-col items-center justify-center text-white">
		<p>{kills}/{deaths}/{assists}</p>
		<p>{cs} cs</p>
		<p>{csMIN} cs/min</p>
	</div>
</div>
