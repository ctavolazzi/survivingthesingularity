<script>
    export let searchQuery;
    export let onSearch;
  </script>
  
  <div class="search-bar">
    <input type="text" bind:value={searchQuery} placeholder="Search articles" />
    <button on:click={onSearch}>Search</button>
  </div>
  
  <style>
    .search-bar {
      /* Add your styles here */
    }
  </style>