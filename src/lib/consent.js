// Single source of truth for consent localStorage key + version.
// Bump CONSENT_VERSION whenever the consent policy changes — both
// StickyCaptureBar and DisclaimerBanner will re-show automatically.
export const CONSENT_KEY = 'sts:consent';
export const CONSENT_VERSION = 'v2-2026-06-07';
