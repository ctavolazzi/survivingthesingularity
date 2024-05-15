<script>
  import { fileFromPath } from "openai";
  import { onMount } from "svelte";
  //// variables
  // import api keys from .env.local
  import { config } from "dotenv"; 
  config();

  // const API_KEY = '51e31e1aada647c19f316bbfb4dfbff4';
  const NEWS_API_KEY = process.env.NEWS_API_KEY;
  const TOP_NEWS_URL = `https://newsapi.org/v2/top-headlines?country=us&apiKey=${NEWS_API_KEY}`;
  const SINGULARITY_NEWS_URL = `GET https://newsapi.org/v2/everything?q=Singularity&from=2024-03-26&sortBy=popularity&apiKey=${API_KEY}`;

  var url = 'https://newsapi.org/v2/everything?' +
          'q=Singularity&' +
          'from=2024-03-26&' +
          'sortBy=popularity&' +
          `apiKey=${NEWS_API_KEY}`;

  var req = new Request(url);

  fetch(req)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      console.log(data);
      
      // Convert the response data to a JSON string
      const jsonString = JSON.stringify(data, null, 2);
      
      // Create a Blob object with the JSON string
      const blob = new Blob([jsonString], { type: 'application/json' });
      
      // Create a temporary URL for the Blob
      const url = URL.createObjectURL(blob);
      
      // Create a link element and trigger a download
      const link = document.createElement('a');
      link.href = url;
      link.download = 'response.json';
      link.click();
      
      // Clean up the temporary URL
      URL.revokeObjectURL(url);
    })
    .catch(function(error) {
      console.log('Error:', error);
    });

  let singularity_articles = [];

  ///async
  onMount(async function() {
    const response = await fetch(TOP_NEWS_URL);
    const json = await response.json();
    articles = json["articles"];
  });
</script>

<style>
  .card {
    font-family: "Gilda Display", serif;
    margin: 5px;
    border: 4px solid #02070a;
    border-radius: 5px;
    box-shadow: 10px 10px 5px rgb(139, 139, 139);
  }
  .card-body {
    margin-bottom: 30px;
  }

  h3,
  p,
  a {
    margin: 1.5rem;
  }
  a {
    color: inherit;
    text-decoration: none;
  }

  img {
    max-width: 100%;
  }
</style>

{#each articles as article}
  <div class="card">
    {#if article.urlToImage === null}
      <br />
    {:else}
      <img src={article.urlToImage} alt="Article Image" />
    {/if}
    <div class="card-body">
      <h3>{article.title}</h3>
      {#if article.description === null}
        <p />
      {:else}
        <p>{article.description}</p>
      {/if}
      <a href={article.url}>Read story</a>
    </div>
  </div>
{/each}