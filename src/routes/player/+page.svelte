<script>
    import MenuMatches from '$lib/components/MenuMatches.svelte';
    import HeaderPlayer from '$lib/components/headerPlayer.svelte';

    let { data } = $props();

    const matches = data.matches;
    const summonerName = data.summoner.gameName;
    const tag = data.summoner.tagLine;
    const puuid = data.summoner.puuid;
</script>

<div class="w-full overflow-auto h-screen">
    <div class="h-1/3 w-full md:h-1/6">
        <HeaderPlayer matches={matches} summonerName={summonerName} tag={tag} />
    </div>
    <div class="flex h-2/3 w-full md:h-5/6">
        <div class="h-full w-full md:w-3/4"></div>
        <div class="hidden md:block md:h-full md:w-1/4 overflow-hidden scroll-smooth hover:overflow-y-auto bg-slate-900">
            <MenuMatches matches={matches}/>
        </div>
    </div>
</div>