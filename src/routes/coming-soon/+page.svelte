<script>
  import { onMount } from 'svelte';

	function handleBackBook() {
      window.open('https://www.kickstarter.com/projects/ctavolazzi/surviving-the-singularity-workbook', '_blank');
    }

    function handleJoinSkool() {
      // window.open('https://www.skool.com/surviving-the-singularity', '_blank');
      alert("The Skool Community is coming soon! We'll notify you when it's ready.");
    }

    function handleGetGuide() {
      window.open('https://tavolazzi.gumroad.com/l/singularitychecklist', '_blank');
    }

  onMount(() => {
    // Load Mailchimp validation script
    const script = document.createElement('script');
    script.src = '//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js';
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      // Initialize Mailchimp form validation
      window.fnames = new Array();
      window.ftypes = new Array();
      fnames[0]='EMAIL';
      ftypes[0]='email';
      fnames[1]='FNAME';
      ftypes[1]='text';
      fnames[2]='LNAME';
      ftypes[2]='text';
      fnames[3]='ADDRESS';
      ftypes[3]='address';
      fnames[4]='PHONE';
      ftypes[4]='phone';
      fnames[5]='BIRTHDAY';
      ftypes[5]='birthday';
      window.$mcj = jQuery.noConflict(true);
    };
  });
</script>

<svelte:head>
  <title>Surviving the Singularity - Skool Community Coming Soon!</title>
  <link href="//cdn-images.mailchimp.com/embedcode/classic-061523.css" rel="stylesheet" type="text/css">
</svelte:head>

<main class="container mx-auto px-4 py-8">
  <h1 class="text-4xl font-bold mb-4 text-center">Surviving the Singularity</h1>
  <h2 class="text-2xl font-semibold mb-8 text-center">Skool Community Coming Soon!</h2>

  <p class="text-xl mb-8 text-center">
    Join our community of forward-thinkers preparing for the technological singularity.
    Launching next Friday!
  </p>

  <div id="mc_embed_signup" class="max-w-2xl mx-auto mb-8">
    <form action="https://irg-listings.us19.list-manage.com/subscribe/post?u=79a060ac083c62360805246c1&amp;id=fe966f6f0e&amp;f_id=0017bce4f0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank">
      <div id="mc_embed_signup_scroll">
        <h2>Join the Waitlist</h2>
        <div class="indicates-required"><span class="asterisk">*</span> indicates required</div>
        <div class="mc-field-group">
          <label for="mce-EMAIL">Email Address <span class="asterisk">*</span></label>
          <input type="email" name="EMAIL" class="required email" id="mce-EMAIL" required value="">
        </div>
        <div id="mergeRow-gdpr" class="mergeRow gdpr-mergeRow content__gdprBlock mc-field-group">
          <div class="content__gdpr">
            <label>Marketing Permissions</label>
            <p>Please select all the ways you would like to hear from us.</p>
            <fieldset class="mc_fieldset gdprRequired mc-field-group" name="interestgroup_field">
              <label class="checkbox subfield" for="gdpr122232">
                <input type="checkbox" id="gdpr_122232" name="gdpr[122232]" class="gdpr" value="Y">
                <span>Email</span>
              </label>
            </fieldset>
            <p>You can unsubscribe at any time by clicking the link in the footer of our emails. For information about our privacy practices, please visit our website.</p>
          </div>
          <div class="content__gdprLegal">
            <p>We use Mailchimp as our marketing platform. By clicking below to subscribe, you acknowledge that your information will be transferred to Mailchimp for processing. <a href="https://mailchimp.com/legal/terms">Learn more</a> about Mailchimp's privacy practices.</p>
          </div>
        </div>
        <div id="mce-responses" class="clear">
          <div class="response" id="mce-error-response" style="display: none;"></div>
          <div class="response" id="mce-success-response" style="display: none;"></div>
        </div>
        <div aria-hidden="true" style="position: absolute; left: -5000px;">
          <input type="text" name="b_79a060ac083c62360805246c1_fe966f6f0e" tabindex="-1" value="">
        </div>
        <div class="clear">
          <input type="submit" name="subscribe" id="mc-embedded-subscribe" class="button" value="Subscribe">
        </div>
      </div>
    </form>

    <div class="button-container">
      <button class="big-button" on:click={handleGetGuide}>Get the FREE Guide</button>
      <button class="big-button" on:click={handleJoinSkool}>Join the Skool Community</button>
      <button class="big-button" on:click={handleBackBook}>Back the Book on Kickstarter</button>
    </div>
  </div>

</main>

<style>
  :global(#mc_embed_signup) {
    background: #fff;
    clear: left;
    font: 14px Helvetica,Arial,sans-serif;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }

  :global(#mc-embedded-subscribe-form input[type=checkbox]) {
    display: inline;
    width: auto;
    margin-right: 10px;
  }

  :global(#mergeRow-gdpr) {
    margin-top: 20px;
  }

  :global(#mergeRow-gdpr fieldset label) {
    font-weight: normal;
  }

  :global(#mc-embedded-subscribe-form .mc_fieldset) {
    border: none;
    min-height: 0px;
    padding-bottom: 0px;
  }

  .action-button {
    font-weight: bold;
    background-color: #f8f9fa;
    border: 1px solid #000000;
    color: #000000;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  .action-button:hover {
    background-color: #000000;
    color: #ffffff;
  }

  .button-container {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin: 1rem 0;
    }

    .big-button {
      flex: 1;
      font-weight: bold;
      font-size: 1.25rem;
      background-color: #f8f9fa;
      border: 2px solid #000000;
      border-radius: 4px;
      padding: 1rem 0.5rem;
      cursor: pointer;
      transition: background-color 0.3s ease, color 0.3s ease;
      text-align: center;
    }

    .big-button:hover {
      background-color: #000000;
      color: #ffffff;
    }
</style>