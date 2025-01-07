<script>
	import { onMount } from 'svelte';

	let { match, summonerName, tag } = $props();

	let win = $state('');
	let champion = $state('');
	let urlSplash = $derived(`https://ddragon.leagueoflegends.com/cdn/img/champion/splash/${champion}_0.jpg`);

    function cardBackground(urlSplash,win){
        if (win){
            return 		`linear-gradient(to bottom, rgba(100, 149, 237, 0),rgba(100, 149, 237,0.6) 80%, rgba(100, 149, 237, 1) 100%), url(${urlSplash})`
        }else{
            return `linear-gradient(to bottom, rgba(237, 50, 50, 0) 0%, rgba(237, 50, 50, 0.1) 35%, rgba(237, 50, 50, 0.3) 60%, rgba(237, 50, 50, 0.6) 80%, rgba(237, 50, 50, 1) 100%), url(${urlSplash})`
        }
    }

	onMount(() => {
		match.info.participants.forEach((player) => {
			if (player.riotIdGameName === summonerName && player.riotIdTagline === tag) {
				win = player.win;
				champion = player.championName;
			}
		});
	});

</script>

<div class="bg-cover bg-center bg-no-repeat h-1/5"
style="background-image : {cardBackground(urlSplash,win)}">
	<p>{champion}</p>
</div>
