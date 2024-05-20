<script>
    import { getArticles } from '$lib/api';
    import { onMount } from 'svelte';
  
    let articles = [];
    let searchQuery = 'Singularity';
  
    async function loadArticles() {
      articles = await getArticles(searchQuery);
    }
  
    function handleSearch() {
      loadArticles();
    }
  
    // onMount(() => {
    //   loadArticles();
    // });
  </script>
  
  <div>
    <h2>News Articles</h2>
    <input type="text" bind:value={searchQuery} placeholder="Search articles" />
    <button on:click={handleSearch}>Search</button>
  
    {#if articles.length === 0}
      <p>Loading articles...</p>
    {:else}
      <ul>
        {#each articles as article}
          <li>
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <a href={article.url} target="_blank">Read more</a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>