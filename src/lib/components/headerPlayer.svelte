<script>
	import { onMount } from 'svelte';
	import { menuVisible,statsDisplay } from './shared.js';
	import MenuMatches from './MenuMatches.svelte';

	let { matches, summonerName, tag } = $props();

	let patchData = $state('');

	let playerField = $state('');
	let icon = $state('');
	let summonerLevel = $state('');
	let summonerID = $state('');

	let rankData = $state('');
	let soloRank = $state('');
	let flexRank = $state('');

	let innerWidth = $state(0)

	$effect(() => {
		if (innerWidth >= 768) $menuVisible = false
	})

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
			if (soloRank === '')
				soloRank = [
					'UNRANKED',
					null,
					`https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank['UNRANKED']}.png?v=9`
				];
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
			if (flexRank === '')
				flexRank = [
					'UNRANKED',
					null,
					`https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/${borderRank['UNRANKED']}.png?v=9`
				];
			rankData = '';
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
		matches[0].info.participants.forEach((player) => {
			if (player.riotIdGameName === summonerName && player.riotIdTagline === tag) {
				playerField = player;
			}
		});

		patchData = await getPatch();

		summonerID = playerField.summonerId;

		rankData = await getRank(summonerID);

		icon = `https://ddragon.leagueoflegends.com/cdn/15.${patchData.split('.').pop()}.1/img/profileicon/${playerField.profileIcon}.png`;
		summonerLevel = playerField.summonerLevel;
	});
</script>

<svelte:window bind:innerWidth />

{#snippet rank(data)}
	<div class="flex flex-col md:flex-row h-full w-1/2 items-center">
		<div class="mb-4 flex h-full w-1/2 flex-col items-center text-base">
			<img src={data[5]} alt="{data[0]} rank" class="h-3/4" />
			<p>{data[0]}</p>
			<p>{data[2]} LP</p>
		</div>
		<div
			class="flex h-full w-1/2 flex-col items-center justify-center text-base lg:-ml-16 xl:-ml-20 overflow-visible whitespace-nowrap"
		>
			<p class="inline-block">{data[3] + data[4]} games</p>
			<p class="inline-block text-blue-400">{data[3]} win</p>
			<p class="inline-block text-red-400">{data[4]} losses</p>
			<p class="inline-block">{Math.round((data[3] / (data[3] + data[4])) * 1000) / 10}%</p>
		</div>
	</div>
{/snippet}

{#snippet unrank(data)}
	<div class="flex h-full w-1/2 items-center">
		<div class="mb-4 flex h-full w-full flex-col items-center text-base">
			<img src={data[2]} alt="{data[0]} rank" class="h-3/4" />
			<p>{data[0]}</p>
		</div>
	</div>
{/snippet}

<div class="flex h-full w-full flex-col items-center bg-slate-900 text-xl text-white md:flex-row">
	<div class="mt-4 flex h-full w-full flex-row items-center justify-center md:w-1/3">
		<div class="flex h-full w-3/4 items-center justify-center md:mt-0 md:w-full" onclick={() => $statsDisplay = 'overview'}>
			<h1 class="ml-8 flex items-center space-x-4">
				<img src={icon} alt="icon of the summoner" class="h-24 w-24 rounded-2xl" />
				<ul>
					<li><p>{summonerName}#{tag}</p></li>
					<li>Level {summonerLevel}</li>
				</ul>
			</h1>
		</div>
		<button
			aria-label="menubar for matches"
			class="flex h-full w-1/4 items-center justify-center md:hidden"
			onclick={(event) => {$menuVisible = true; event.stopPropagation()}}
		>
			<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"
				><g
					fill="none"
					stroke="currentColor"
					stroke-dasharray="8"
					stroke-dashoffset="8"
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					><path d="M12 5h6M12 5h-6" stroke-dashoffset="0" /><path
						d="M12 10h6M12 10h-6"
						stroke-dashoffset="0"
					/><path d="M12 15h6M12 15h-6" stroke-dashoffset="0" /><path
						d="M12 20h6M12 20h-6"
						stroke-dashoffset="0"
					/></g
				></svg
			>
		</button>
	</div>
	<div class="flex h-full w-5/6 items-center md:w-2/3">
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

{#if innerWidth<=768}
	<MenuMatches {summonerName} {tag} {matches} onMenu={true}/>
{/if}