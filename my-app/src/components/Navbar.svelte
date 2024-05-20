<script>
  import { Navbar, NavBrand, NavHamburger, NavLi, NavUl } from 'flowbite-svelte';

  function handleBuyBook() {
    alert("The book is not complete and will be available for preorder 7-30-24.\n\nAuthor Christopher Tavolazzi is still collecting interviews for the book.\n\nThank you for your patience.");
  }
</script>

<Navbar let:NavContainer color="primary">
  <NavContainer class="border px-5 py-2 rounded-lg bg-white dark:bg-gray-600">
    <NavBrand href="/">
      <img src="https://flowbite.com/docs/images/logo.svg" class="me-3 h-6 sm:h-9" alt="Flowbite Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold">Surviving the Singularity</span>
    </NavBrand>
    <NavHamburger />
    <NavUl>
      <NavLi href="/about">About</NavLi>
      <NavLi href="/contact">Contact</NavLi>
      <NavLi href="https://docs.google.com/document/d/1plGfd2X8-TsH3aCjbSz6aJeZTpfmrHZ6zNJ2hw6ww9s/edit" target="_blank">Read a Sample</NavLi>
      <NavLi href="javascript:void(0);" on:click={handleBuyBook} style="font-weight: bold;">Buy the Book</NavLi>
    </NavUl>
  </NavContainer>
</Navbar>
