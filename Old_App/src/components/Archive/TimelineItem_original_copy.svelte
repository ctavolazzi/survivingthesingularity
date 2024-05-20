<!-- TimelineItem.svelte -->
<script>
    export let event = {
      title: '',
      date: '',
      time: '',
      icon: '',
      description: '',
      details: ''
    };
  </script>
  
  <div class="timeline-item">
    <div class="timeline-item-node">
      <div class="timeline-item-icon">
        <img src={event.icon} alt={event.title} class="h-8 w-8" />
      </div>
    </div>
    <div class="timeline-item-content">
      <div class="timeline-item-header">
        <h3 class="text-lg font-bold mb-2">{event.title}</h3>
        <p class="text-gray-500 italic mb-1">{event.date}</p>
        <p class="text-gray-500 italic">{event.time}</p>
      </div>
      <div class="timeline-item-body">
        <p class="text-sm mb-4">{event.description}</p>
        <div class="collapse border border-base-300 bg-base-100 rounded-box">
          <input type="checkbox" class="peer" />
          <div class="collapse-title text-base font-medium">
            Read more
          </div>
          <div class="collapse-content">
            <p class="text-sm">{event.details}</p>
            <!-- Add more DaisyUI components for interaction and exploration -->
            <div class="rating mt-4">
              <input type="radio" name="rating-{event.title}" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-{event.title}" class="mask mask-star-2 bg-orange-400" checked />
              <input type="radio" name="rating-{event.title}" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-{event.title}" class="mask mask-star-2 bg-orange-400" />
              <input type="radio" name="rating-{event.title}" class="mask mask-star-2 bg-orange-400" />
            </div>
            <button class="btn btn-primary mt-4">Learn More</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <style>
    .timeline-item {
      display: flex;
      align-items: center;
      margin-bottom: 40px;
    }
  
    .timeline-item-node {
      position: relative;
      width: 40px;
      height: 40px;
      background-color: #fff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-right: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
  
    .timeline-item-icon {
      display: flex;
      justify-content: center;
      align-items: center;
    }
  
    .timeline-item-content {
      flex: 1;
    }
  </style>