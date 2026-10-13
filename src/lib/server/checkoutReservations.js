import { supabaseAdmin } from '$lib/server/supabaseAdmin.js';

/**
 * Reuse one open Stripe session per normalized email/edition. The database
 * serializes reservation creation; Stripe serializes create calls sharing the
 * reservation key. A unique preorder row alone cannot prevent two charges.
 */
export async function getOrCreateCheckout({ stripe, email, editionType, params }) {
  if (!supabaseAdmin) throw new Error('Checkout reservation database unavailable');
  const reserve = async (expiredSession = null) => {
    const { data, error } = await supabaseAdmin.rpc('reserve_checkout', {
      p_email: email, p_edition_type: editionType, p_expired_session: expiredSession,
    });
    if (error || !data?.reservation_key) throw new Error(error?.message ?? 'Checkout reservation missing');
    return data;
  };
  let reservation = await reserve();
  if (reservation.session_id) {
    const existing = await stripe.checkout.sessions.retrieve(reservation.session_id);
    if (existing.status === 'open') return existing;
    if (existing.status === 'complete') {
      // Even pending asynchronous payments must not open a second charge.
      return { pendingPayment: true };
    }
    if (existing.status !== 'expired') throw new Error('Checkout status unavailable');
    reservation = await reserve(existing.id);
    // Another request may already have rotated and attached the new session.
    if (reservation.session_id) {
      const current = await stripe.checkout.sessions.retrieve(reservation.session_id);
      if (current.status === 'open') return current;
      if (current.status === 'complete') return { pendingPayment: true };
      throw new Error('Checkout changed; retry shortly');
    }
  }
  // Stripe retains idempotency records for at least 24h. If creation may have
  // succeeded but attachment was lost, never blindly create again after that
  // guarantee expires. An operator must reconcile this exceptional reservation.
  if (Date.now() - Date.parse(reservation.created_at) > 23 * 60 * 60 * 1000) {
    throw new Error('Checkout reservation needs reconciliation');
  }
  const session = await stripe.checkout.sessions.create(params, {
    idempotencyKey: `checkout/${reservation.reservation_key}`,
  });
  const { data, error } = await supabaseAdmin.from('checkout_reservations')
    .update({ session_id: session.id })
    .eq('email', email).eq('edition_type', editionType)
    .eq('reservation_key', reservation.reservation_key)
    .select('session_id');
  if (error || !data?.length) throw new Error(error?.message ?? 'Checkout reservation changed');
  return session;
}
