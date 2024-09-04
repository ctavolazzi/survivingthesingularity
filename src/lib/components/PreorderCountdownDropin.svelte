<script>
    import Countdown from './Countdown.svelte';
    import PreorderDropin from './PreorderDropin.svelte';
    import Divider from './Divider.svelte';
  
    export let targetDate = new Date("2027-11-20T23:59:59").getTime();
    export let headerText = "Time Left";
</script>

<div class="preorder-countdown-dropin">
    <Divider />
    <div class="content">
        <h2 class="title">Limited Time Offer</h2>
        <h1 class="main-title">Book Dropping Soon</h1>
        <Countdown {targetDate} {headerText} />
        <PreorderDropin />
    </div>
    <Divider />
</div>

<style>
    .preorder-countdown-dropin {
        width: 100%;
        max-width: 1200px;
        /* margin: 4rem auto; */
        /* padding: 2rem 1rem; */
    }

    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin: 2rem 0;
    }

    .title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .main-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }

    /* Ensure Countdown and PreorderDropin components stack vertically */
    :global(.preorder-countdown-dropin .content > *) {
        margin-bottom: 2rem;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .preorder-countdown-dropin {
            margin: 2rem auto;
        }

        .main-title {
            font-size: 2.5rem;
        }
    }
</style>