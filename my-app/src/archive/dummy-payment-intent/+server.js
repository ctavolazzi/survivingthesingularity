// src/routes/dummy-payment-intent/+server.js
export async function POST({ request }) {
  try {
    console.log('Received request to create dummy payment intent');
    const { amount, currency } = await request.json();
    console.log('Request JSON:', { amount, currency });

    // Simulate a payment intent creation response
    const paymentIntent = {
      id: 'pi_dummy',
      object: 'payment_intent',
      amount,
      currency,
      client_secret: 'pi_dummy_secret_123456',
      status: 'requires_payment_method'
    };

    console.log('Dummy Payment Intent created:', paymentIntent);

    return new Response(JSON.stringify({ clientSecret: paymentIntent.client_secret }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error creating dummy payment intent:', error);
    return new Response(JSON.stringify({ error: 'Internal Server Error', message: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}
