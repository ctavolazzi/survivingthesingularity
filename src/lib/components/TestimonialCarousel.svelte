<script>
    import { onMount, onDestroy } from 'svelte';
  
    export let testimonials = [];
    export let autoplayInterval = 5000; // Time in ms between auto-rotations
  
    let currentIndex = 0;
    let intervalId;
  
    function nextTestimonial() {
      currentIndex = (currentIndex + 1) % testimonials.length;
    }
  
    function prevTestimonial() {
      currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
    }
  
    onMount(() => {
      intervalId = setInterval(nextTestimonial, autoplayInterval);
    });
  
    onDestroy(() => {
      if (intervalId) clearInterval(intervalId);
    });
  </script>
  
  <div class="testimonial-carousel">
    <button class="nav-button prev" on:click={prevTestimonial}>&lt;</button>
    
    <div class="testimonial">
      <p class="quote">"{testimonials[currentIndex].quote}"</p>
      <p class="author">- {testimonials[currentIndex].author}</p>
    </div>
    
    <button class="nav-button next" on:click={nextTestimonial}>&gt;</button>
  </div>
  
  <style>
    .testimonial-carousel {
      position: relative;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      text-align: center;
    }
  
    .testimonial {
      min-height: 150px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
  
    .quote {
      font-style: italic;
      font-size: 1.2em;
      margin-bottom: 10px;
    }
  
    .author {
      font-weight: bold;
    }
  
    .nav-button {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      font-size: 1.5em;
      cursor: pointer;
      padding: 10px;
      color: #333;
    }
  
    .prev {
      left: 0;
    }
  
    .next {
      right: 0;
    }
  </style>