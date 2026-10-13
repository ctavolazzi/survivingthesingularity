import { env } from '$env/dynamic/private';
import manifest from '$lib/data/bundleManifest.js';
import { validateBundleRelease } from '$lib/bundleRelease.js';

export function currentBundleRelease() {
  return validateBundleRelease(env, manifest);
}
