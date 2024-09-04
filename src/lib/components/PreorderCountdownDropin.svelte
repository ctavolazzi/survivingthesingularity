<script>
    import Countdown from './Countdown.svelte';
    import PreorderDropin from './PreorderDropin.svelte';
    import Divider from './Divider.svelte';
  
    export let targetDate = new Date("2027-11-20T23:59:59").getTime();
    export let headerText = "Time Left";
</script>

<div class="text-center mt-16 mb-12">
    <div class="mb-8">
        <Divider />
    </div>
    <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6 mt-8">
    <h2 class="text-3xl font-bold mb-4">Limited Time Offer</h2>
    <Countdown {targetDate} headerText={headerText} />
    <PreorderDropin />
    </div>
    <div class="mt-8">
        <Divider />
    </div>
</div>

<style>

</style>