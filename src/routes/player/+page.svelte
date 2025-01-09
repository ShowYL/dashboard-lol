<script>
    import Match from '$lib/components/Match.svelte';
    import HeaderPlayer from '$lib/components/headerPlayer.svelte';

    let { data } = $props();

    const matches = data.matches;
    const summonerName = data.summoner.gameName;
    const tag = data.summoner.tagLine;
    const puuid = data.summoner.puuid;
    
</script>

<div class="w-full overflow-auto h-screen">
    <div class="h-1/3 w-full md:h-1/6">
        <HeaderPlayer match={matches[0]} summonerName={summonerName} tag={tag} />
    </div>
    <div class="flex h-2/3 w-full md:h-5/6">
        <div class="h-full w-3/4"></div>
        <div class="h-full w-1/4 overflow-hidden scroll-smooth hover:overflow-y-auto bg-slate-900">
            {#each matches as match}
                <Match {match} {summonerName} {tag} />
            {/each}
        </div>
    </div>
</div>