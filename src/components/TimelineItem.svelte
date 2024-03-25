<script>
    import { TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent, TimelineOppositeContent } from 'svelte-vertical-timeline';
    
    export let event;
    let showModal = false;
  
    function openModal() {
      showModal = true;
    }
  
    function closeModal() {
      showModal = false;
    }
  </script>
  
  <TimelineItem>
    <TimelineOppositeContent slot="opposite-content" class="timeline-time">
      <h3>{event.time}</h3>
      <p>{event.time.includes('am') ? 'Morning' : 'Afternoon'}</p>
      <p>{event.time.includes('am') ? '🌅' : '🌆'}</p>
    </TimelineOppositeContent>
    <TimelineSeparator>
      <TimelineDot />
      <TimelineConnector />
    </TimelineSeparator>
    <TimelineContent>
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title">{event.title}</h2>
          <p>{event.description}</p>
          <button class="btn btn-primary" on:click={openModal}>Open Modal</button>
        </div>
      </div>
    </TimelineContent>
  </TimelineItem>
  
  {#if showModal}
    <div class="modal-overlay" on:click={closeModal}>
      <div class="modal" on:click|stopPropagation>
        <div class="modal-content">
          <h2>{event.title}</h2>
          <p>{event.details}</p>
          <button class="btn btn-primary" on:click={closeModal}>Close</button>
        </div>
      </div>
    </div>
  {/if}
  
  <style>
    .timeline-time {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      padding-right: 20px;
    }
  
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999;
    }
  
    .modal {
      background-color: white;
      border-radius: 8px;
      padding: 20px;
      max-width: 400px;
      width: 100%;
    }
  
    .modal-content {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  
    .modal-content h2 {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 10px;
    }
  
    .modal-content p {
      margin-bottom: 20px;
    }
  </style>