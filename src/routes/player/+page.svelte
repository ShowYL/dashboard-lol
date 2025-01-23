<script>
	import MenuMatches from '$lib/components/MenuMatches.svelte';
	import HeaderPlayer from '$lib/components/headerPlayer.svelte';
	import StatsPage from '$lib/components/StatsPage.svelte';
	import { statsDisplay } from '$lib/components/shared.js';
	import { onMount } from 'svelte';

	let { data } = $props();

	const matches = data.matches;
	const summonerName = data.summoner.gameName;
	const tag = data.summoner.tagLine;
	const puuid = data.summoner.puuid;

	onMount(() => {
		window.addEventListener('keydown', (e) => {
			if (e.key === 'h') {
				$statsDisplay = 'overview';
			}
		});
	});
</script>

<div class="h-screen w-full overflow-auto">
	<div class="h-3/5 w-full md:h-1/6">
		<HeaderPlayer {matches} {summonerName} {tag} />
	</div>
	<div class="flex h-2/5 w-full md:h-5/6">
		<div class="h-full w-full bg-slate-900 md:w-3/4">
			<StatsPage {data} />
		</div>
		<div
			class="hidden overflow-hidden scroll-smooth bg-slate-900 hover:overflow-y-auto md:block md:h-full md:w-1/4"
		>
			<MenuMatches {matches} {summonerName} {tag} />
		</div>
	</div>
</div>
