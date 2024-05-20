<script>
  export let progress = 0; // The progress percentage (0 to 100)
</script>

<div class="progress-bar-container">
  <div class="progress-bar" style="width: {progress}%;"></div>
  <div class="progress-labels">
    <span class="label-left">Industrial Revolution</span>
    <span class="label-right">The Singularity</span>
  </div>
</div>

<style>
  .progress-bar-container {
    width: 100%;
    height: 40px; /* Adjust the height as needed */
    background-color: #e0e0e0; /* Grey background */
    border-radius: 10px;
    overflow: hidden;
    margin-top: 1rem;
    position: relative; /* Ensure labels are positioned relative to the progress bar */
    display: flex;
    align-items: center;
    justify-content: space-between; /* Ensure labels are positioned on the left and right */
  }

  .progress-bar {
    position: absolute; /* Position the bar absolutely within the container */
    left: 0;
    top: 0;
    height: 100%;
    background: linear-gradient(to right, #000000, #616161); /* Simple dark grey gradient */
    transition: width 0.3s ease-in-out;
  }

  .progress-labels {
    display: flex;
    justify-content: space-between;
    align-items: center; /* Vertically center the labels */
    width: 100%;
    position: relative; /* Position labels relative within the container */
    padding-left: 20px; /* Add padding to the left */
    padding-right: 20px; /* Increase padding to the right */
    z-index: 1; /* Ensure labels are on top of the progress bar */
  }

  .label-left,
  .label-right {
    font-size: 0.875rem; /* Adjust font size as needed */
    color: #ffffff; /* White color for better contrast on the bar */
    text-shadow: 1px 1px 2px #000000; /* Add a stroke for better visibility */
    white-space: nowrap; /* Ensure text doesn't wrap */
  }
</style>
