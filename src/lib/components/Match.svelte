<script>
	import { onMount } from 'svelte';
	import splashPosition from './SplashPosition.js';

	let { match, summonerName, tag } = $props();

	let win = $state('');
	let champion = $state('');
	let urlSplash = $state('');
	let kills = $state('')
	let assists = $state('')
	let deaths = $state('')
	let cs =$state('')
	let gameDuration = match.info.gameDuration
	let csMIN = $derived(((Math.round(cs / (gameDuration / 600)))/10).toString().replace('.',','))

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
				kills = player.kills
				assists = player.assists
				deaths = player.deaths
				cs = player.totalMinionsKilled + player.neutralMinionsKilled
			}
		});

		urlSplash = `https://ddragon.leagueoflegends.com/cdn/img/champion/centered/${champion}_0.jpg`;
	});
</script>

<div class="flex flex-row w-full h-1/5 items-center justify-center">
	<div
		class="bg-cover h-5/6 rounded-3xl w-3/5 ml-4 {splashPosition[champion]
			? splashPosition[champion]
			: 'bg-center'} h-1/5 bg-no-repeat"
		style="background-image : {cardBackground(urlSplash, win)}"
	></div>
	<div class="h-full w-2/5 mt-4 items-center flex flex-col justify-center text-white">
		<p>{kills}/{deaths}/{assists}</p>
		<p>{cs} cs</p>
		<p>{csMIN} cs/min</p>
	</div>
</div>
