<script>
  import Hero from '$lib/components/Hero.svelte';
  import PrecedentFile from '$lib/components/PrecedentFile.svelte';
  import OfferTable from '$lib/components/OfferTable.svelte';
  import UpdateEngine from '$lib/components/UpdateEngine.svelte';
  import BookParts from '$lib/components/BookParts.svelte';
  import Close from '$lib/components/Close.svelte';
  import { offer } from '$lib/offer.js';
</script>

<svelte:head>
  <title>Surviving the Singularity</title>
  <meta name="description" content={offer.sentence} />
</svelte:head>

<Hero />
<PrecedentFile />
<OfferTable />
<UpdateEngine />
<BookParts />
<Close />
