<script>
  import timelineItems from '../data/timelineItems.json'; // Adjust the path as necessary

  let showModal = Array(timelineItems.timelineItems.length).fill(false);

  function toggleModal(index) {
    showModal[index] = !showModal[index];
    showModal = [...showModal]; // Trigger reactivity
  }

  function handleModalClick(event, index) {
    if (event.target === event.currentTarget) {
      toggleModal(index);
    }
  }

  function searchGoogle(title) {
    const query = encodeURIComponent(title);
    window.open(`https://www.google.com/search?q=${query}`, '_blank');
  }

  function openWikipedia(url) {
    window.open(url, '_blank');
  }
</script>

<div class="timeline-container" style="padding: 1rem; background-color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-radius: 0.5rem; max-width: 800px; margin: auto;">
  <h1 style="font-size: 1.875rem; font-weight: bold; text-align: center; color: #1F2937; margin-bottom: 1.5rem;">Timeline of Events</h1>
  <hr style="margin-bottom: 2rem; border-color: #E5E7EB;" />

  <ol style="position: relative; border-left: 2px solid #E5E7EB; padding-left: 1rem;">
    {#each timelineItems.timelineItems as item, index (item.id)}
      <li style="margin-bottom: 2.5rem; padding-left: 1rem;">
        <div style="position: absolute; width: 0.75rem; height: 0.75rem; background-color: black; border-radius: 50%; margin-top: 0.375rem; left: -0.375rem; border: 2px solid white;"></div>
        <time style="display: block; margin-bottom: 0.25rem; font-size: 0.875rem; color: #6B7280;">{item.date}</time>
        <h3 style="font-size: 1.125rem; font-weight: 600; color: #1F2937; margin-bottom: 0.5rem;">{item.title}</h3>
        <p style="font-size: 1rem; color: #4B5563; margin-bottom: 1rem;">{item.abstract}</p>
        <button 
          class="learn-more-btn" 
          on:click={() => toggleModal(index)} 
          style="display: inline-flex; align-items: center; padding: 0.5rem 1rem; background-color: transparent; color: black; font-weight: 500; border-radius: 0.25rem; border: none; cursor: pointer; transition: all 0.3s;"
        >
          Learn More 
          <svg style="width: 1rem; height: 1rem; margin-left: 0.5rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>

        {#if showModal[index]}
          <div class="modal" on:click={(e) => handleModalClick(e, index)} style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;">
            <div style="position: relative; background-color: white; padding: 2rem; border-radius: 0.5rem; max-width: 80%; max-height: 80%; overflow-y: auto;">
              <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">{item.title}</h2>
              <p style="margin-bottom: 1rem;">{item.description}</p>
              <p style="margin-bottom: 1rem;"><strong>Significance:</strong> {item.significance}</p>
              <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
                <button 
                  on:click={() => openWikipedia(item.urls.wikipedia)}
                  style="padding: 0.5rem 1rem; background-color: white; color: black; border: 2px solid black; border-radius: 0.25rem; cursor: pointer; transition: all 0.3s;"
                >
                  Wikipedia
                </button>
                <button 
                  on:click={() => searchGoogle(item.title)}
                  style="padding: 0.5rem 1rem; background-color: white; color: black; border: 2px solid black; border-radius: 0.25rem; cursor: pointer; transition: all 0.3s;"
                >
                  Search Google
                </button>
              </div>
              <button 
                on:click={() => toggleModal(index)}
                style="position: absolute; top: 0.5rem; right: 0.5rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; padding: 0.25rem 0.5rem; line-height: 1;"
              >
                ×
              </button>
            </div>
          </div>
        {/if}
      </li>
    {/each}
  </ol>

  <hr style="margin-top: 2rem; margin-bottom: 1rem; border-color: #E5E7EB;" />
</div>

<style>
  .learn-more-btn:hover {
    background-color: rgba(0, 0, 0, 0.1) !important;
  }
  .modal button:hover {
    background-color: black !important;
    color: white !important;
  }
</style>