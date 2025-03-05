<script>
    import { onMount } from 'svelte';
    import PreorderButton from './PreorderButton.svelte';

    export let fullPrice = "$24.99";
    export let discountedPrice = "$9";
    export let releaseDate = "First week of November";
    export let limitedCopies = 1000;

    let availableCopies = limitedCopies;
    let timer;

    function handlePreorder() {
      // Implement your preorder logic here
      console.log('Preorder button clicked');
    }

    function reduceAvailableCopies() {
      const reduction = Math.floor(Math.random() * 3) + 1; // Random reduction between 1 and 3
      availableCopies = Math.max(0, availableCopies - reduction);

      if (availableCopies > 0) {
        scheduleNextReduction();
      } else {
        clearTimeout(timer);
      }
    }

    function scheduleNextReduction() {
      const delay = Math.floor(Math.random() * 14000) + 1000; // Random delay between 1000ms and 15000ms
      timer = setTimeout(reduceAvailableCopies, delay);
    }

    onMount(() => {
      scheduleNextReduction();
      return () => clearTimeout(timer);
    });
</script>

<div class="preorder-dropin">
<h3 class="text-3xl font-bold mb-4">Transform Your Future with 'Surviving the Singularity'</h3>
<div class="content">
    <p class="story mb-4">
    Imagine waking up confident and prepared for the AI-driven world, instead of feeling overwhelmed and left behind.
    </p>
    <p class="story-2 mb-4">That's the transformation 'Surviving the Singularity' offers. Readers like you have gone from anxious to empowered,
    from confused to clear-minded about their place in the AI revolution.
    </p>
    <ul class="list-disc pl-5 mb-6">
    <li>Gain clarity on how AI will impact your career and daily life</li>
    <li>Master practical tools to adapt and thrive in the AI era</li>
    <li>Join a community of forward-thinkers shaping the future</li>
    <li>Access exclusive insights from AI experts and ethicists</li>
    </ul>
    <p class="urgency mb-4">
    <span class="discount-highlight">Limited Time Offer:</span> Pre-order now for just <strong>{discountedPrice}</strong>
    (regular price: <s>{fullPrice}</s>)! Only <strong>{availableCopies}</strong> copies left at this special price.
    Don't miss this opportunity to secure your future!
    </p>
</div>
<div class="cta">
    <p class="release-info mb-4">Release Date: {releaseDate} | Current Pre-order Price: <span class="discount-price">{discountedPrice}</span></p>
    <div class="button-container">
        <PreorderButton buttonText={`Pre-order Now for ${discountedPrice}`} />
    </div>
    <p class="guarantee">30-day money-back guarantee. No risk, all reward.</p>
</div>
</div>

<style>
.preorder-dropin {
    background-color: #f8f9fa;
    border: 2px solid #FF9933;
    border-radius: 8px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.content {
    text-align: left;
}

.story {
    font-style: italic;
    line-height: 1.8;
    font-size: 1.1rem;
}

.urgency {
    font-weight: bold;
    color: #FF9933;
}

.discount-highlight {
    background-color: #FF9933;
    color: white;
    padding: 2px 5px;
    border-radius: 3px;
}

.discount-price {
    font-size: 1.2em;
    font-weight: bold;
    color: #FF9933;
}

.release-info {
    font-style: italic;
    color: #666;
}

.guarantee {
    font-size: 0.9rem;
    color: #666;
}

.action-button {
    font-weight: bold;
    background-color: #FF9933;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    font-size: 1rem;
    border-radius: 5px;
}

.action-button:hover {
    background-color: #FF8000;
    transform: translateY(-2px);
}

:global(.dark) .preorder-dropin {
    background-color: #2d3748;
    color: #e2e8f0;
}

:global(.dark) .urgency {
    color: #FF9933;
}

:global(.dark) .release-info,
:global(.dark) .guarantee {
    color: #a0aec0;
}

:global(.dark) .action-button {
    color: #1a202c;
}

:global(.dark) .action-button:hover {
    background-color: #FF8000;
}

.story-2 {
    line-height: 1.4;
    font-size: 1.1rem;
}


ul li {
    font-weight: bold;
}

.button-container {
    margin: 1.5rem 0;
}
</style>