<script>
	import { onMount } from 'svelte';
	import { _getBanner } from './+page.js';
	import { handwriting } from '$lib/components/handwritting.js';

	let bannerUrl = $state('');
	let textDisplayed = $state(false);

	async function fetchBanner() {
		bannerUrl = await _getBanner();
	}

	onMount(() => {
		fetchBanner();
	});

	let backgroundImage = $derived(
		`linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.7) 20%, rgba(0, 0, 0, 1) 100%), url(${bannerUrl})`
	);
</script>

{#if bannerUrl != ''}
	<div
		class="flex h-full w-full items-center justify-center bg-cover bg-center bg-no-repeat"
		style="background-image: {backgroundImage};"
	>
		<div class="mx-auto mb-20 mt-auto flex h-1/5 w-2/5 items-center justify-center text-slate-400">
			<button class="flex w-3/5 min-w-56 rounded bg-slate-900 p-1 text-left opacity-70 items-center"
				><span in:handwriting={{ speed: 0.6 }} onintroend={() => textDisplayed = true}>Hide on bush #GOAT</span>
				{#if textDisplayed == true}
					<span class="ml-auto"
					><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
						><g
							fill="none"
							stroke="currentColor"
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							><path
								stroke-dasharray="64"
								stroke-dashoffset="64"
								d="M3 12c0 4.97 4.03 9 9 9c4.97 0 9 -4.03 9 -9c0 -4.97 -4.03 -9 -9 -9c-4.97 0 -9 4.03 -9 9Z"
								><animate
									fill="freeze"
									attributeName="stroke-dashoffset"
									dur="0.33s"
									values="64;0"
								/></path
							><path stroke-dasharray="12" stroke-dashoffset="12" d="M7 12h9.5"
								><animate
									fill="freeze"
									attributeName="stroke-dashoffset"
									begin="0.385s"
									dur="0.11s"
									values="12;0"
								/></path
							><path stroke-dasharray="8" stroke-dashoffset="8" d="M17 12l-4 4M17 12l-4 -4"
								><animate
									fill="freeze"
									attributeName="stroke-dashoffset"
									begin="0.495s"
									dur="0.11s"
									values="8;0"
								/></path
							></g
						></svg
					></span>
				{/if}
			</button
			>
		</div>
	</div>
{:else}
	<div class="flex h-full w-full items-center justify-center">
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="50"
			height="50"
			viewBox="0 0 24 24"
			class="h-auto w-auto"
			><path
				fill="none"
				stroke="currentColor"
				stroke-dasharray="16"
				stroke-dashoffset="16"
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 3c4.97 0 9 4.03 9 9"
				><animate
					fill="freeze"
					attributeName="stroke-dashoffset"
					dur="0.2s"
					values="16;0"
				/><animateTransform
					attributeName="transform"
					dur="1.5s"
					repeatCount="indefinite"
					type="rotate"
					values="0 12 12;360 12 12"
				/></path
			></svg
		>
	</div>
{/if}
