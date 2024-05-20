<script>
  import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent } from 'svelte-vertical-timeline';
  import ItemModal from './CustomItemModal.svelte';
  import { fade } from 'svelte/transition';
  import { inview } from 'svelte-inview';

  export let event;

  let isInView = false;
  let showModal = false;

  function openModal() {
    showModal = true;
  }

  function closeModal() {
    showModal = false;
  }

  const options = {
    unobserveOnEnter: true,
    rootMargin: '-20%'
  };

  const handleChange = ({ detail }) => {
    isInView = detail.inView;
  };

  function formatDate(dateString) {
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'];

    const day = dateString.slice(-2);
    const monthIndex = parseInt(dateString.slice(-5, -3)) - 1;
    const month = monthNames[monthIndex];
    const year = dateString.slice(0, -6);

    return `${month} ${day}, ${year}`;
  }
</script>

<div use:inview={options} on:inview_change={handleChange}>
  {#if isInView}
    <div in:fade={{ duration: 400 }}>
      <TimelineItem>
        <TimelineSeparator>
          <TimelineDot aria-hidden="true" />
          <TimelineConnector aria-hidden="true" />
        </TimelineSeparator>
        <TimelineContent class="timeline-content">
          <div class="card bg-base-100 shadow-xl" id="timeline-item-{event.id}">
            <div class="card-body">
              <h3 class="timeline-date">{formatDate(event.published)}</h3>
              <h2 class="card-title">{event.title}</h2>
              <h4>{event.authors.length > 0 ? `By ${event.authors.join(', ')}` : 'Anonymous'}</h4>
              <p>
                {event.category === 'Computing' ? '🖥️' : event.category === 'Mathematics' ? '➕' : event.category === 'Technology' ? '🔩' : '📚'}
                {event.category}
              </p>
              <p>{event.abstract}</p>
              <button class="btn btn-primary" on:click={openModal}>View Details</button>
            </div>
          </div>
        </TimelineContent>
      </TimelineItem>
    </div>
  {:else}
    <div style="visibility: hidden;">
      <TimelineItem>
        <TimelineSeparator>
          <TimelineDot aria-hidden="true" />
          <TimelineConnector aria-hidden="true" />
        </TimelineSeparator>
        <TimelineContent class="timeline-content">
          <div class="card bg-base-100 shadow-xl" id="timeline-item-{event.id}">
            <div class="card-body">
              <h3 class="timeline-date">{formatDate(event.published)}</h3>
              <h2 class="card-title">{event.title}</h2>
              <h4>{event.authors.length > 0 ? `By ${event.authors.join(', ')}` : 'Anonymous'}</h4>
              <p>
                {event.category === 'Computing' ? '🖥️' : event.category === 'Mathematics' ? '➕' : event.category === 'Technology' ? '🔩' : '📚'}
                {event.category}
              </p>
              <p>{event.abstract}</p>
              <button class="btn btn-primary" on:click={openModal}>View Details</button>
            </div>
          </div>
        </TimelineContent>
      </TimelineItem>
    </div>
  {/if}
</div>

{#if showModal}
  <ItemModal {event} on:close={closeModal} />
{/if}

<style>
  .timeline-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    text-align: left;
    width: calc(100% - 50px); /* Adjust this value to take up more width */
    padding-left: 20px;
    box-sizing: border-box;
  }

  .timeline-date {
    font-weight: bold;
  }

  .card {
    width: 100%;
  }

  .card-body {
    padding: 20px;
  }

  .card-title {
    font-size: 1.5rem;
    margin-bottom: 10px;
  }

  .timeline-date, .card-title, h4, p {
    margin: 5px 0;
  }

  @media (max-width: 768px) {
    .card-title {
      font-size: 1.25rem;
    }

    .card-body {
      padding: 15px;
    }
  }

  @media (max-width: 480px) {
    .card-title {
      font-size: 1rem;
    }

    .card-body {
      padding: 10px;
    }
  }
</style>

