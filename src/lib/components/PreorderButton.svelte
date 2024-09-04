<script>
    export let buttonText = "Preorder Now";
    let isLoading = false;
    let error = null;

    async function handlePreorder() {
        isLoading = true;
        error = null;

        try {
            const response = await fetch('/api/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const { url } = await response.json();

            // Redirect to Stripe Checkout
            window.location.href = url;
        } catch (err) {
            console.error('Preorder error:', err);
            error = 'An error occurred. Please try again.';
        } finally {
            isLoading = false;
        }
    }
</script>

<button
    on:click={handlePreorder}
    disabled={isLoading}
    class="preorder-button"
>
    {#if isLoading}
        <span class="loader"></span>
    {:else}
        {buttonText}
    {/if}
</button>

{#if error}
    <p class="error-message">{error}</p>
{/if}

<style>
    .preorder-button {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        border: none;
        border-radius: 50px;
        color: #fff;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        padding: 15px 30px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }

    .preorder-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    .preorder-button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }

    .preorder-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .preorder-button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: rgba(255, 255, 255, 0.2);
        transform: rotate(45deg);
        transition: all 0.3s ease;
    }

    .preorder-button:hover::before {
        left: 100%;
    }

    .loader {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #ffffff;
        border-radius: 50%;
        border-top: 3px solid transparent;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .error-message {
        color: #ff4757;
        font-weight: bold;
        margin-top: 10px;
        text-align: center;
    }
</style>