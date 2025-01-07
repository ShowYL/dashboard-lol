<script>
	import Match from '$lib/components/Match.svelte';

	let { data } = $props();

	const matches = data.matches;
	const summonerName = data.summoner.gameName;
	const tag = data.summoner.tagLine;
	const puuid = data.summoner.puuid;

	console.log(matches[0]);
</script>

<div class="h-full w-full">
	<div class="h-1/6 w-full"></div>
	<div class="flex h-5/6 w-full">
		<div class="w-3/4 h-full"></div>
		<div class="w-1/4 h-full overflow-auto">
			{#each matches as match}
				<Match {match} {summonerName} {tag} />
			{/each}	
		</div>
	</div>
</div>
