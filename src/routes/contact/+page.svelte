<script>
  import Navbar from '../../components/Navbar.svelte';
  import BottomNav from '../../components/BottomNav.svelte';
  import Spacer from '../../components/Spacer.svelte'; // Import Spacer component
</script>

<Navbar />

<div class="container mx-auto p-4">
  <div class="form-wrapper max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md">
    <h1 class="form-title text-2xl font-semibold mb-6 text-center">Get in touch:</h1>
    <p class="text-center">Please use the Mailchimp form below to get in touch with us.</p>
    <iframe src="https://us19.list-manage.com/contact-form?u=79a060ac083c62360805246c1&form_id=c4630b003308d7c72c1d0479c30c9a64" width="100%" height="600px" frameborder="0" style="border:0; overflow:hidden;" title="Mailchimp contact form"></iframe>
  </div>
</div>

<!-- Spacer for bottom navigation -->
<Spacer height="6rem" />

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
</style>
