<script>
    import { onMount } from 'svelte';
    import { handwriting } from '$lib/components/handwritting.js';

    let { data } = $props();

    let bannerUrl = data.fetchedPantryData.banner;
    let textDisplayed = $state(false);
    let researchClicked = $state(false);
    let input = $state('');
    let showText = $state(false); // for transition purpose by entering the dom after the initialitation

    $effect(() => {
        if (researchClicked) {
            input?.focus();
        }
    });

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
    }

    function handleClick(event) {
        if (researchClicked && event.target != input) {
            console.log('here');
            researchClicked = false;
        }
    }

    let backgroundImage = $derived(
        `linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3) 40%,rgba(0,0,0,0.7) 65%,rgba(0,0,0,0.9) 75%, rgba(0, 0, 0, 1) 100%), url(${bannerUrl})`
    );
</script>

<div
    class="flex h-full w-full items-center justify-center bg-cover bg-center bg-no-repeat"
    style="background-image: {backgroundImage};"
>
    <div class="mx-auto mb-20 mt-auto flex h-1/5 w-2/5 items-center justify-center text-slate-400">
        {#if !researchClicked}
            <button
                class="flex w-3/5 min-w-56 items-center rounded bg-slate-900 p-1 text-left opacity-70 shadow-2xl"
                onclick={(event) => {
                    event.stopPropagation();
                    researchClicked = true;
                }}
            >
                {#if showText}
                    <span in:handwriting|global={{ speed: 1.2 }} onintroend={() => (textDisplayed = true)}>
                        Hide on bush#GOAT
                    </span>
                {/if}
                {#if textDisplayed}
                    <span class="ml-auto">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
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
                                <path stroke-dasharray="8" stroke-dashoffset="8" d="M17 12l-4 4M17 12l-4 -4">
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
            <input
                bind:this={input}
                class="flex w-3/5 min-w-56 rounded bg-slate-900 p-1 text-left opacity-70 shadow-2xl focus:border-none"
                placeholder="riotID + #TAG"
            />
        {/if}
    </div>
</div>