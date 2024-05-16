<script>
  import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';
  import ItemModal from './ItemModal.svelte';
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
        <TimelineOppositeContent slot="opposite-content" class="timeline-time">
          <h3>{formatDate(event.published)}</h3>
          <h4>{event.authors.length > 0 ? `By ${event.authors.join(', ')}` : 'Anonymous'}</h4>
          <p>
            {event.category === 'Computing' ? '🖥️' : event.category === 'Mathematics' ? '➕' : event.category === 'Technology' ? '🔩' : '📚'}
            {event.category}
          </p>
        </TimelineOppositeContent>
        <TimelineSeparator>
          <TimelineDot aria-hidden="true" />
          <TimelineConnector aria-hidden="true" />
        </TimelineSeparator>
        <TimelineContent>
          <div class="card bg-base-100 shadow-xl" id="timeline-item-{event.id}">
            <div class="card-body">
              <h2 class="card-title">{event.title}</h2>
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
        <TimelineOppositeContent slot="opposite-content" class="timeline-time">
          <h3>{formatDate(event.published)}</h3>
          <h4>{event.authors.length > 0 ? `By ${event.authors.join(', ')}` : 'Anonymous'}</h4>
          <p>
            {event.category === 'Computing' ? '🖥️' : event.category === 'Mathematics' ? '➕' : event.category === 'Technology' ? '🔩' : '📚'}
            {event.category}
          </p>
        </TimelineOppositeContent>
        <TimelineSeparator>
          <TimelineDot aria-hidden="true" />
          <TimelineConnector aria-hidden="true" />
        </TimelineSeparator>
        <TimelineContent>
          <div class="card bg-base-100 shadow-xl" id="timeline-item-{event.id}">
            <div class="card-body">
              <h2 class="card-title">{event.title}</h2>
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
  .timeline-time {
    text-align: left;
    padding: 0 1rem;
  }

  .card {
    margin: 0 auto;
    padding: 1rem;
    text-align: left;
  }

  .card-body {
    display: flex;
    flex-direction: column;
    align-items: flex-start; /* Align items to the left */
  }

  .card-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .btn {
    margin-top: 1rem;
  }

  @media (max-width: 768px) {
    .timeline-time {
      padding: 0.5rem;
    }

    .card {
      padding: 0.5rem;
    }

    .card-body {
      padding: 0.5rem;
    }
  }

  @media (max-width: 480px) {
    .timeline-time {
      padding: 0.5rem;
    }

    .card-title {
      font-size: 1.25rem;
    }

    .card-body {
      padding: 0.5rem;
    }

    .btn {
      width: 100%;
    }
  }
</style>
