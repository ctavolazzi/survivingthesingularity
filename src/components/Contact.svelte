<script>
    function handleSubmit() {
        alert('Submission received');
        // Prevent form from actually submitting to a page.
        return false;
    }
</script>

<div class="container">
    <div class="form-wrapper">
        <h1 class="form-title">Contact Us</h1>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label for="name">Your Name</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">Your Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="message">Message</label>
                <textarea id="message" name="message" rows="4" required></textarea>
            </div>
            <div class="form-group text-center">
                <button type="submit" class="submit-btn">Send Message</button>
            </div>
        </form>
    </div>
</div>

<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    .form-wrapper {
        max-width: 400px;
        width: 100%;
        padding: 2rem;
        padding-top: 0;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .form-title {
        text-align: center;
        margin-bottom: 2rem;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }

    input,
    textarea {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .submit-btn {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #000000;
        color: #fff;
        border: 1px solid rgb(0, 0, 0);
        border-radius: 4px;
        cursor: pointer;
    }

    .submit-btn:hover {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 4px;
    }
</style>