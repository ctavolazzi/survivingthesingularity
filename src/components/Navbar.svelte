<!-- <script>
  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
  // import { supabase } from '$lib/supabaseClient';

  // async function handleLogout() {
  //   await supabase.auth.signOut();
  //   goto('/');
  // }
  async function logBackBookClick() {
    await supabase.from('back_book_clicks').insert({
      timestamp: new Date(),
      referrer: document.referrer,
      user_agent: navigator.userAgent,
    });
  }

  function handleBackBook() {
    logBackBookClick();
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
  }
</script>

<Navbar let:NavContainer color="primary">
  <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
    <NavBrand href="/">
      <img src="/src/images/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <NavHamburger />
    <NavUl class="nav-items-container">
      <NavLi href="/about">
        <a class="nav-link" href="/about">About</a>
      </NavLi>
      <NavLi href="/contact">
        <a class="nav-link" href="/contact">Contact</a>
      </NavLi>
      <NavLi>
        <a class="nav-link" href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
      </NavLi>
      <NavLi class="custom-buy-button-container">
        <a class="nav-link buy-button" onclick={handleBackBook}>Back the Book</a>
      </NavLi>
    </NavUl>
  </NavContainer>
</Navbar>

<style>
  .me-3 {
    margin-right: 1rem;
  }

  .nav-link {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }

  .nav-link:hover {
    background-color: #e2e6ea; /* Slightly darker on hover */
  }

  .buy-button {
    font-weight: bold;
    background-color: #f8f9fa; /* Light background color */
    border: 1px solid #000000;
    border-radius: 4px;
    padding: 0.5rem 1rem;
  }
</style> -->

<script>
  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
  import { supabase } from '$lib/supabaseClient';

  async function logBackBookClick() {
    await supabase.from('back_book_clicks').insert({
      timestamp: new Date(),
      referrer: window.location.href,
      user_agent: navigator.userAgent,
    });
  }

  function handleBackBook() {
    logBackBookClick();
    window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity?ref=user_menu', '_blank');
  }
</script>

<Navbar let:NavContainer color="primary">
  <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
    <NavBrand href="/">
      <img src="/src/images/android-chrome-192x192.png" class="me-3 h-6 sm:h-9" alt="Surviving the Singularity Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <NavHamburger />
    <NavUl class="nav-items-container">
      <NavLi href="/about">
        <a class="nav-link" href="/about">About</a>
      </NavLi>
      <NavLi href="/contact">
        <a class="nav-link" href="/contact">Contact</a>
      </NavLi>
      <NavLi>
        <a class="nav-link" href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</a>
      </NavLi>
      <NavLi class="custom-buy-button-container">
        <button class="nav-link buy-button" on:click={handleBackBook}>Back the Book</button>
      </NavLi>
    </NavUl>
  </NavContainer>
</Navbar>

<style>
  .me-3 {
    margin-right: 1rem;
  }

  .nav-link {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }

  .nav-link:hover {
    background-color: #e2e6ea; /* Slightly darker on hover */
  }

  .buy-button {
    font-weight: bold;
    background-color: #f8f9fa; /* Light background color */
    border: 1px solid #000000;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
</style>