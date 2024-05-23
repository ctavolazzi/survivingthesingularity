<script>
  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';
  import { user } from '$lib/userStore';
  import { goto } from '$app/navigation';
  import { supabase } from '$lib/supabaseClient';

  async function handleLogout() {
    await supabase.auth.signOut();
    user.set(null);
    goto('/');
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
      {#if $user}
        <NavLi href="/dashboard">
          <a class="nav-link" href="/dashboard">Dashboard</a>
        </NavLi>
      {:else}
        <NavLi href="/auth">
          <a class="nav-link" href="/auth">Login</a>
        </NavLi>
      {/if}
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
        <a class="nav-link buy-button" href="/buy-book">Buy the Book</a>
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
</style>
