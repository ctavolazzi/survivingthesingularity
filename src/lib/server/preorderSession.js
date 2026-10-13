/** Only sessions created for this offer can confer this offer's entitlement. */
export function isPreorderSession(session) {
  return session?.mode === 'payment'
    && session.metadata?.product === 'early-access-bundle-v1'
    && ['standard', 'authors'].includes(session.metadata?.edition_type);
}
