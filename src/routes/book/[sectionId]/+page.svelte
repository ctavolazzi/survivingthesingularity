<script>
  export let data;
</script>

<h1>{data.book.title}</h1>
<h2>{data.section.title}</h2>

<article>
  {@html data.content}
</article>

<nav>
  <a href="/book">Back to Table of Contents</a>
</nav>
