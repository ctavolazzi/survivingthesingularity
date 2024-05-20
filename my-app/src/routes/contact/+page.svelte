<script>
  import Navbar from '../../components/Navbar.svelte';
  import BottomNav from '../../components/BottomNav.svelte';
  import Spacer from '../../components/Spacer.svelte'; // Import Spacer component
  import { Label, Input, Textarea, Button } from 'flowbite-svelte';

  function handleSubmit() {
    alert('Sorry, this form is not implemented yet. Please contact Christopher Tavolazzi on social media @ thecoffeejesus');
    // Prevent form from actually submitting to a page.
    return false;
  }
</script>

<Navbar />

<div class="container mx-auto p-4">
  <div class="form-wrapper max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md">
    <h1 class="form-title text-2xl font-semibold mb-6 text-center">Contact Us</h1>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="mb-6">
        <Label for="name" class="block mb-2">Your Name</Label>
        <Input id="name" type="text" placeholder="John Doe" required class="w-full" />
      </div>
      <div class="mb-6">
        <Label for="email" class="block mb-2">Your Email</Label>
        <Input id="email" type="email" placeholder="name@flowbite.com" required class="w-full" />
      </div>
      <div class="mb-6">
        <Label for="message" class="block mb-2">Message</Label>
        <Textarea id="message" rows="4" placeholder="Leave a comment..." required class="w-full"></Textarea>
      </div>
      <div class="form-group text-center">
        <Button type="submit" class="submit-btn">Send Message</Button>
      </div>
    </form>
  </div>
</div>

<!-- Spacer for bottom navigation -->
<Spacer />

<BottomNav />

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
  }

  .form-wrapper {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 2rem;
  }

  .form-title {
    text-align: center;
    margin-bottom: 2rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }
</style>
