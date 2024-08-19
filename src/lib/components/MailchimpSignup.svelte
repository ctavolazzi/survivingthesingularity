<script>
  import { darkMode } from '$lib/stores/darkMode';
</script>

<div class="mailchimp-signup" class:dark={$darkMode}>
  <form action="https://irg-listings.us19.list-manage.com/subscribe/post?u=79a060ac083c62360805246c1&amp;id=fe966f6f0e&amp;v_id=4524&amp;f_id=00e7bce4f0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank">
    <h2>Subscribe to our mailing list</h2>
    <div class="form-group">
      <label for="mce-EMAIL">Email Address <span class="asterisk">*</span></label>
      <input type="email" name="EMAIL" class="required email" id="mce-EMAIL" required value="" />
    </div>
    <div class="form-group">
      <label for="gdpr_122232" class="checkbox-label">
        <input type="checkbox" id="gdpr_122232" name="gdpr[122232]" value="Y" class="checkbox">
        <span>I agree to receive marketing emails</span>
      </label>
    </div>
    <div class="form-group">
      <button type="submit" name="subscribe" id="mc-embedded-subscribe" class="button">Subscribe</button>
    </div>
    <p class="disclaimer">We respect your privacy. Unsubscribe at any time.</p>
  </form>
</div>

<style>
  .mailchimp-signup {
    --bg-color: #ffffff;
    --text-color: #2c3e50;
    --input-bg: #f8f9fa;
    --input-border: #ced4da;
    --button-bg: #2c3e50;
    --button-text: #ffffff;
    --button-hover: #34495e;
    --disclaimer-color: #6c757d;

    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: var(--bg-color);
    color: var(--text-color);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }

  :global(.dark) .mailchimp-signup {
    --bg-color: #1f2937;
    --text-color: #e5e7eb;
    --input-bg: #374151;
    --input-border: #4b5563;
    --button-bg: #e5e7eb;
    --button-text: #1f2937;
    --button-hover: #d1d5db;
    --disclaimer-color: #9ca3af;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    color: var(--text-color);
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-color);
  }

  input[type="email"] {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid var(--input-border);
    border-radius: 4px;
    background-color: var(--input-bg);
    color: var(--text-color);
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .checkbox {
    margin-right: 0.5rem;
  }

  .button {
    display: inline-block;
    width: 100%;
    padding: 0.75rem 1rem;
    background-color: var(--button-bg);
    color: var(--button-text);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 1rem;
    font-weight: 600;
  }

  .button:hover {
    background-color: var(--button-hover);
  }

  .disclaimer {
    font-size: 0.8rem;
    text-align: center;
    margin-top: 1rem;
    color: var(--disclaimer-color);
  }

  @media (max-width: 768px) {
    .mailchimp-signup {
      padding: 1rem;
      margin: 1rem auto;
    }
  }
</style>