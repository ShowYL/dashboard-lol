<script>
	import { onMount } from 'svelte';

	let { match, summonerName, tag } = $props();

	let patchData = $state('');

	let playerField = $state('');
	let icon = $state('');
	let summonerLevel = $state('');
	let summonerID = $state('');

	let rankData = $state('');
	let soloRank = $state('');
	let flexRank = $state('');

	$inspect(soloRank)

	const borderRank = {
		UNRANKED: 0,
		IRON: 1,
		BRONZE: 2,
		SILVER: 3,
		GOLD: 4,
		PLATINUM: 5,
		EMERALD: 6,
		DIAMOND: 7,
		MASTER: 8,
		GRANDMASTER: 9,
		CHALLENGER: 10
	};

	$effect(() => {
		if (rankData !== '') {
			rankData.forEach((data) => {
				if (data.queueType === 'RANKED_SOLO_5x5') {
					const borderRankUrl = `https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank[data.tier]}.png?v=9`;
					soloRank = [
						data.tier,
						data.rank,
						data.leaguePoints,
						data.wins,
						data.losses,
						borderRankUrl
					];
				}
			});
			if (soloRank === '') soloRank = ['UNRANKED',null,`https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank['UNRANKED']}.png?v=9`]
			rankData.forEach((data) => {
				if (data.queueType === 'RANKED_FLEX_SR') {
					const borderRankUrl = `https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank[data.tier]}.png?v=9`;
					flexRank = [
						data.tier,
						data.rank,
						data.leaguePoints,
						data.wins,
						data.losses,
						borderRankUrl
					];
				}
			});
			if (flexRank === '') flexRank = ['UNRANKED',null,`https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank['UNRANKED']}.png?v=9`]
			rankData = ''
		}
	});

	async function getPatch() {
		const response = await fetch('/api/getPatch');
		const data = await response.json();
		const patch = await data.patch;
		return patch;
	}

	async function getRank(summonerId) {
		const response = await fetch(`/api/getRank?summonerId=${summonerId}`);
		const data = await response.json();
		return data;
	}

	onMount(async () => {
		match.info.participants.forEach((player) => {
			if (player.riotIdGameName === summonerName && player.riotIdTagline === tag) {
				playerField = player;
			}
		});

		patchData = await getPatch();

		summonerID = playerField.summonerId;

		rankData = await getRank(summonerID);

		icon = `https://ddragon.leagueoflegends.com/cdn/${patchData}/img/profileicon/${playerField.profileIcon}.png`;
		summonerLevel = playerField.summonerLevel;
	});
</script>

{#snippet rank(data)}
	<div class="flex h-full w-1/2 items-center">
		<div class="h-full w-1/2 flex items-center flex-col text-base mb-4">
			<img src={data[5]} alt="{data[0]} rank" class="h-3/4" />
			<p>{data[0]}</p>
			<p>{data[2]} LP</p>
		</div>
		<div class="h-full w-1/2 flex flex-col items-center justify-center text-base lg:-ml-16 xl:-ml-20">
			<p>{data[3]+data[4]} games</p>
			<p class="text-blue-400">{data[3]} win</p>
			<p class="text-red-400">{data[4]} losses</p>
			<p>{Math.round((data[3]/(data[3]+data[4]))*1000)/10}%</p>
		</div>
	</div>
{/snippet}

{#snippet unrank(data)}
	<div class="flex h-full w-1/2 items-center">
		<div class="h-full w-1/2 flex items-center flex-col text-base mb-4">
			<img src={data[2]} alt="{data[0]} rank" class="h-3/4" />
			<p>{data[0]}</p>
		</div>
	</div>
{/snippet}

<div class="flex h-full w-full flex-col items-center bg-slate-900 text-xl text-white md:flex-row">
	<div class="flex h-full w-full items-center justify-center md:w-1/3">
		<h1 class="ml-8 flex items-center space-x-4">
			<img src={icon} alt="icon of the summoner" class="h-24 w-24 rounded-2xl" />
			<ul>
				<li><p>{summonerName}#{tag}</p></li>
				<li>Level {summonerLevel}</li>
			</ul>
		</h1>
	</div>
	<div class="flex h-full w-full items-center md:w-2/3">
		{#if soloRank !== '' && soloRank[1] !== null}
			{@render rank(soloRank)}
		{:else}
			{@render unrank(soloRank)}
		{/if}
		{#if flexRank !== '' && flexRank[1] !== null}
			{@render rank(flexRank)}
		{:else}
			{@render unrank(flexRank)}
		{/if}
	</div>
</div>
