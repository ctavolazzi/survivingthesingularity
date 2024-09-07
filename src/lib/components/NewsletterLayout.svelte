<script>
    import { goto } from '$app/navigation';
    import NewsletterList from './NewsletterList.svelte';
    import NewsletterSignup from './NewsletterSignup.svelte';
    import SkoolGroup from './SkoolGroup.svelte';
    import Spacer from './Spacer.svelte';
    import Divider from './Divider.svelte';
    import PreorderCountdownDropin from './PreorderCountdownDropin.svelte';
  
    export let newsletters = [];
    export let currentSlug = '';

    function handleSelectNewsletter(event) {
      const slug = event.detail;
      if (slug !== currentSlug) {
        goto(`/newsletter/${slug}`);
      }
    }
</script>

<Spacer height="50px" />

<div>
    <div class="flex flex-col lg:flex-row gap-8">
      <div class="w-full lg:w-1/3 order-2 lg:order-1">
        <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden sticky top-4">
          <NewsletterList 
            {newsletters} 
            on:select={handleSelectNewsletter}
            selectedSlug={currentSlug}
          />
        </div>
      </div>
      <div class="w-full lg:w-2/3 order-1 lg:order-2">
        <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden p-4 sm:p-6">
          <slot></slot>
        </div>
      </div>
    </div>

    <Divider />

    <NewsletterSignup />
    <PreorderCountdownDropin />
    <SkoolGroup />
</div>

<style>
    :global(body) {
      background-color: #f0f2f5;
    }
  
    :global(.dark body) {
      background-color: #1a202c;
    }
</style>