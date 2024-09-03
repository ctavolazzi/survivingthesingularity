<script>
    import { createEventDispatcher } from 'svelte';
  
    export let currentSection = 1;
    export let totalSections = 1;
  
    const dispatch = createEventDispatcher();
  
    function goToPrevious() {
      if (currentSection > 1) {
        dispatch('navigate', { direction: 'previous' });
      }
    }
  
    function goToNext() {
      if (currentSection < totalSections) {
        dispatch('navigate', { direction: 'next' });
      }
    }
  </script>
  
  <nav class="pagination">
    <button on:click={goToPrevious} disabled={currentSection === 1} class="btn btn-primary">
      Previous
    </button>
    <span class="pagination-info">
      {currentSection} / {totalSections}
    </span>
    <button on:click={goToNext} disabled={currentSection === totalSections} class="btn btn-primary">
      Next
    </button>
  </nav>
  
  <style>
    .pagination {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 2rem;
      gap: 1rem;
    }
  
    .pagination-info {
      font-family: 'Orbitron', sans-serif;
      color: #ff7708;
      flex: 0 0 auto;
    }
  
    button {
      flex: 1;
      min-width: 100px;
    }
  
    @media (max-width: 640px) {
      .pagination {
        flex-wrap: wrap;
      }
  
      button {
        flex: 1 0 40%;
      }
  
      .pagination-info {
        order: -1;
        width: 100%;
        text-align: center;
        margin-bottom: 0.5rem;
      }
    }
  </style>