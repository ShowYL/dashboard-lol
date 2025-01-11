<script>
    import Match from "./Match.svelte";
    import { menuVisible } from './shared.js';

    let { summonerName, tag, matches, onMenu = false } = $props();

    let menu = $state(null);

    $effect(() => {
        if ($menuVisible) {
            window.addEventListener('click', handleClick);
        } else {
            window.removeEventListener('click', handleClick);
        }
    });

    function handleClick(event) {
        if (menu && !menu.contains(event.target)) {
            $menuVisible = false;
        }
    }
</script>

{#if onMenu}
    <div
        bind:this={menu}
        class={`fixed right-0 top-0 h-full overflow-auto w-3/5 transform bg-slate-900 text-white transition-transform duration-300 ${$menuVisible ? 'translate-x-0' : 'translate-x-full'}`}
    >
        {#each matches as match}
            <Match {match} {summonerName} {tag}/>
        {/each}
    </div>
{:else}
    {#each matches as match}
        <Match {match} {summonerName} {tag}/>
    {/each}
{/if}