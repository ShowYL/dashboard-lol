<script>
	import { statsDisplay } from './shared.js';
	import { scrollTrigger } from '$lib/components/animations/scrollTrigger.js';

	let { data } = $props();
	const puuid = data.summoner.puuid;

	let id = $state('overview');
	let match = $state(null);
	let player = $state(null);

	const findMatch = () => {
		if (id === 'overview') return data.matches;
		return data.matches.find((match) => match.metadata.matchId === id);
	};

    const findPlayer = (match) => {
        if(id ==='overview'){

        }else{
            return match.info.participants.find((participant) => {
            return participant.puuid === puuid;
        });
        }
    };

	statsDisplay.subscribe((value) => {
		id = value;
		match = findMatch();
		player = findPlayer(match);
	});
</script>

{#if id === 'overview'}
	<div class="h-full w-full overflow-hidden bg-slate-900 p-4 hover:overflow-y-auto">
		<div
			class="grid w-full auto-rows-[minmax(200px,1fr)] grid-cols-1 gap-16 scroll-smooth p-4 md:grid-cols-2 xl:grid-cols-3"
		>
			<div use:scrollTrigger class="card">
				id : {id}<br />
			</div>
			<div use:scrollTrigger class="card">2</div>
			<div use:scrollTrigger class="card">3</div>
			<div use:scrollTrigger class="card">4</div>
			<div use:scrollTrigger class="card">5</div>
			<div use:scrollTrigger class="card">6</div>
			<div use:scrollTrigger class="card">7</div>
			<div use:scrollTrigger class="card">8</div>
			<div use:scrollTrigger class="card">9</div>
		</div>
	</div>
{:else}
	<div class="h-full w-full overflow-hidden bg-slate-900 p-4 hover:overflow-y-auto">
		<div
			class="grid w-full auto-rows-[minmax(200px,1fr)] grid-cols-1 gap-16 scroll-smooth p-4 md:grid-cols-2 xl:grid-cols-3"
		>
			<div use:scrollTrigger class="card">
                id : {id}
			</div>
			<div use:scrollTrigger class="card">2</div>
			<div use:scrollTrigger class="card">3</div>
			<div use:scrollTrigger class="card">4</div>
			<div use:scrollTrigger class="card">5</div>
			<div use:scrollTrigger class="card">6</div>
			<div use:scrollTrigger class="card">7</div>
			<div use:scrollTrigger class="card">8</div>
			<div use:scrollTrigger class="card">9</div>
		</div>
	</div>
{/if}
