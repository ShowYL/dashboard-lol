<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { handwriting } from '$lib/components/handwritting.js';

	let { data } = $props();

	let bannerUrl = data.fetchedPantryData.banner;
	let textDisplayed = $state(false);
	let researchClicked = $state(false);
	let input = $state(null);
	let inputValue = $state('');
	let inputDiv = $state(null);
	let showText = $state(false); // for transition purpose by entering the dom after the initialitation
	let gameName = $state('');
	let tag = $state('');
	let erreur = $state('');

	$effect(() => {
		if (researchClicked){
			input?.focus()
			input?.select()
		}else{
			erreur = ''
		}
	});

	async function checkValidInput() {
		if (inputValue === '') {
			erreur = 'Please fill in the field';
			return;
		}

		if (!inputValue.includes('#')) {
			erreur = "Le tag n'est pas renseigné";
			return;
		}

		gameName = inputValue.split('#')[0];
		tag = inputValue.split('#')[1];

		if (!/^[a-zA-Z0-9 ]{3,16}$/.test(gameName)) {
			erreur = 'le nom est incorrect';
			return;
		}

		if (!/^[a-zA-Z0-9 ]{3,5}$/.test(tag)) {
			erreur = 'le tag est incorrect';
			return;
		}

		const res = await checkSummoners(gameName, tag);

		if (!res) {
			erreur = "Le joueur n'existe pas";
			return;
		}

		// Redirect to another page with parameters
		goto(`/player?gameName=${gameName}&tag=${tag}`);
	}

	async function checkSummoners(name, letag) {
		try {
			const res = await fetch(`/api/getSummoner?riotID=${name}&tag=${letag}`);
			if (!res.ok) {
				return null;
			}
			return await res.json();
		} catch (err) {
			return null;
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
		window.addEventListener('click', handleClick);
		showText = true; // Trigger the transition on mount
	});

	function handleKeydown(event) {
		if (event.ctrlKey && event.key === 'k') {
			event.preventDefault();
			researchClicked = !researchClicked;
		}

		if (event.key === 'Enter' && researchClicked) {
			checkValidInput();
		}
	}

	function handleClick(event) {
		if (researchClicked && inputDiv && !inputDiv.contains(event.target)) {
			researchClicked = false;
		}
	}

	let backgroundImage = $derived(
		`linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3) 40%,rgba(0,0,0,0.7) 65%,rgba(0,0,0,0.9) 75%, rgba(0, 0, 0, 1) 100%), url(${bannerUrl})`
	);
</script>

<div
	class="flex h-full w-full items-center justify-center bg-cover bg-center bg-no-repeat flex-col"
	style="background-image: {backgroundImage};"
>
	<div class="mx-auto mb-16 mt-auto flex h-1/5 w-2/5 items-center justify-center text-slate-400">
		{#if !researchClicked}
			<button
				class="flex h-9 w-3/5 min-w-56 items-center rounded bg-slate-900 p-1 text-left opacity-70 shadow-2xl"
				onclick={(event) => {
					event.stopPropagation();
					researchClicked = true;
				}}
			>
				{#if showText}
					<span
						in:handwriting|global={{ speed: 1.2 }}
						onintroend={() => (textDisplayed = true)}
					>
						Hide on bush#GOAT
					</span>
				{/if}
				{#if textDisplayed}
					<span class="ml-auto">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
						>
							<g
								fill="none"
								stroke="currentColor"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
							>
								<path
									stroke-dasharray="64"
									stroke-dashoffset="64"
									d="M3 12c0 4.97 4.03 9 9 9c4.97 0 9 -4.03 9 -9c0 -4.97 -4.03 -9 -9 -9c-4.97 0 -9 4.03 -9 9Z"
								>
									<animate
										fill="freeze"
										attributeName="stroke-dashoffset"
										dur="0.33s"
										values="64;0"
									/>
								</path>
								<path stroke-dasharray="12" stroke-dashoffset="12" d="M7 12h9.5">
									<animate
										fill="freeze"
										attributeName="stroke-dashoffset"
										begin="0.385s"
										dur="0.11s"
										values="12;0"
									/>
								</path>
								<path
									stroke-dasharray="8"
									stroke-dashoffset="8"
									d="M17 12l-4 4M17 12l-4 -4"
								>
									<animate
										fill="freeze"
										attributeName="stroke-dashoffset"
										begin="0.495s"
										dur="0.11s"
										values="8;0"
									/>
								</path>
							</g>
						</svg>
					</span>
				{/if}
			</button>
		{:else}
			<div class="h-9 w-3/5 min-w-56">
				<div
					bind:this={inputDiv}
					class="flex rounded bg-slate-900 p-1 text-left opacity-70 shadow-2xl"
				>
					<input
						bind:this={input}
						bind:value={inputValue}
						class="w-5/6 rounded bg-slate-900 p-1 focus:border-none focus:outline-none"
						placeholder="game name + #TAG"
					/>
					<button
						class="flex w-1/6 items-center justify-end rounded"
						aria-label="button to search player"
						onclick={checkValidInput}
						><svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							><g
								fill="none"
								stroke="currentColor"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								><path
									d="M3 12c0 4.97 4.03 9 9 9c4.97 0 9 -4.03 9 -9c0 -4.97 -4.03 -9 -9 -9c-4.97 0 -9 4.03 -9 9Z"
								/><path d="M7 12h9.5" /><path d="M17 12l-4 4M17 12l-4 -4" /></g
							></svg
						></button
					>
				</div>
				<div><p>{erreur}</p></div>
			</div>
		{/if}
	</div>
	<div class="text-slate-700 text-xs"> 
		<p>Dashboard LoL is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc</p>
	</div>
</div>
