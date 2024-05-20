<script>
  export let event;
  export let onClick;
</script>

<div class="event-item">
  <div class="event-content">
    <h3 class="event-date">{event.published}</h3>
    <h2 class="event-title">{event.title}</h2>
    <h4 class="event-authors">{event.authors.length > 0 ? `By ${event.authors.join(', ')}` : 'Anonymous'}</h4>
    <p class="event-category">
      {event.category === 'Computing' ? '🖥️' : event.category === 'Mathematics' ? '➕' : event.category === 'Technology' ? '🔩' : '📚'}
      {event.category}
    </p>
    <p class="event-abstract">{event.abstract}</p>
    <button class="btn btn-primary" on:click={() => onClick(event)}>Learn More</button>
  </div>
</div>

<style>
  .event-item {
    background-color: white;
    border-radius: 4px;
    margin: 20px 0;
    padding: 20px;
    max-width: 800px;
    width: 100%;
    box-sizing: border-box;
  }

  .event-content {
    text-align: left;
  }

  .event-date, .event-title, .event-authors, .event-category, .event-abstract {
    margin: 10px 0;
  }

  .event-date {
    font-weight: bold;
  }

  .event-title {
    font-size: 1.5rem;
    margin-bottom: 10px;
  }

  .event-authors {
    font-size: 1rem;
    margin-bottom: 10px;
  }

  .event-abstract {
    font-size: 1rem;
    margin-bottom: 10px;
  }

  .btn {
    background-color: #000;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
  }

  .btn:hover {
    background-color: #333;
  }
</style>
