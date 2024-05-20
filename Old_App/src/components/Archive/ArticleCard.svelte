<script>
    export let article;
  </script>
  
  <div class="article-card">
    <h3>{article.title}</h3>
    <p>{article.description}</p>
    <a href={article.url} target="_blank">Read more</a>
  </div>
  
  <style>
    .article-card {
      /* Add your styles here */
    }
  </style>