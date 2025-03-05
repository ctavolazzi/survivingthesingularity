<script>
  import NewsletterLayout from '$lib/components/NewsletterLayout.svelte';
  import NewsletterContent from '$lib/components/NewsletterContent.svelte';
  import { page } from '$app/stores';
  import { getNewsletterComponent } from '$lib/utils/newsletterLoader';

  export let data;

  // Get the component for the latest newsletter
  const latestNewsletterComponent = getNewsletterComponent(data.latestNewsletter.slug);

  // Helper function for pagination links
  function getPaginationUrl(pageNum) {
    return `/newsletter?page=${pageNum}${data.pagination.perPage !== 10 ? `&perPage=${data.pagination.perPage}` : ''}`;
  }
</script>

<svelte:head>
  <title>Surviving the Singularity Newsletters</title>
  <meta name="description" content="Browse our collection of newsletters about surviving the singularity." />
</svelte:head>

<NewsletterLayout newsletters={data.newsletters} currentSlug={data.latestNewsletter.slug} pagination={data.pagination}>
  <NewsletterContent
    component={latestNewsletterComponent}
    metadata={{
      title: data.latestNewsletter.title,
      date: data.latestNewsletter.date,
      description: data.latestNewsletter.description
    }}
  />

  {#if data.pagination.totalPages > 1}
    <div class="pagination my-8">
      <div class="pagination-controls flex justify-center items-center">
        {#if data.pagination.currentPage > 1}
          <a href={getPaginationUrl(data.pagination.currentPage - 1)} class="pagination-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </a>
        {:else}
          <span class="pagination-arrow disabled">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </span>
        {/if}

        <div class="page-numbers">
          {#each Array(data.pagination.totalPages) as _, index}
            {@const pageNum = index + 1}
            {#if
              pageNum === 1 ||
              pageNum === data.pagination.totalPages ||
              (pageNum >= data.pagination.currentPage - 1 &&
               pageNum <= data.pagination.currentPage + 1)
            }
              <a
                href={getPaginationUrl(pageNum)}
                class="pagination-number {data.pagination.currentPage === pageNum ? 'active' : ''}"
              >
                {pageNum}
              </a>
            {:else if
              (pageNum === data.pagination.currentPage - 2 && pageNum > 1) ||
              (pageNum === data.pagination.currentPage + 2 && pageNum < data.pagination.totalPages)
            }
              <span class="pagination-ellipsis">•••</span>
            {/if}
          {/each}
        </div>

        {#if data.pagination.currentPage < data.pagination.totalPages}
          <a href={getPaginationUrl(data.pagination.currentPage + 1)} class="pagination-arrow">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        {:else}
          <span class="pagination-arrow disabled">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </span>
        {/if}
      </div>

      <div class="text-center text-sm text-gray-500 dark:text-gray-400 mt-2">
        Page {data.pagination.currentPage} of {data.pagination.totalPages}
      </div>
    </div>
  {/if}
</NewsletterLayout>

<style>
  .pagination {
    position: relative;
  }

  .pagination::before {
    content: '';
    position: absolute;
    top: -1rem;
    left: 25%;
    width: 50%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(209, 213, 219, 0.5), transparent);
  }

  .pagination-controls {
    gap: 0.75rem;
  }

  .page-numbers {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .pagination-number {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 2.5rem;
    width: 2.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    border-radius: 9999px;
    color: #4b5563;
    background-color: #f3f4f6;
    transition: all 0.2s;
  }

  .pagination-number:hover {
    background-color: #e5e7eb;
  }

  .pagination-number.active {
    background-color: #f97316;
    color: white;
    box-shadow: 0 2px 4px rgba(249, 115, 22, 0.2);
  }

  .pagination-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 2.5rem;
    width: 2.5rem;
    border-radius: 9999px;
    color: #4b5563;
    background-color: #f3f4f6;
    transition: all 0.2s;
  }

  .pagination-arrow:hover {
    background-color: #e5e7eb;
  }

  .pagination-arrow.disabled {
    color: #9ca3af;
    background-color: #f3f4f6;
    cursor: not-allowed;
    opacity: 0.5;
  }

  .pagination-ellipsis {
    color: #6b7280;
    font-size: 0.625rem;
    letter-spacing: 1px;
  }

  :global(.dark) .pagination-number {
    background-color: #1f2937;
    color: #e5e7eb;
  }

  :global(.dark) .pagination-number:hover {
    background-color: #374151;
  }

  :global(.dark) .pagination-number.active {
    background-color: #f97316;
    color: white;
  }

  :global(.dark) .pagination-arrow {
    background-color: #1f2937;
    color: #e5e7eb;
  }

  :global(.dark) .pagination-arrow:hover {
    background-color: #374151;
  }

  :global(.dark) .pagination-arrow.disabled {
    color: #6b7280;
    background-color: #1f2937;
  }

  :global(.dark) .pagination-ellipsis {
    color: #9ca3af;
  }

  :global(.dark) .pagination::before {
    background: linear-gradient(to right, transparent, rgba(75, 85, 99, 0.5), transparent);
  }
</style>
