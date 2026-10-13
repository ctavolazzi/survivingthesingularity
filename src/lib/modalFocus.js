// Only the top modal owns focus and background inertness. Suspending a modal
// restores its changes first; resuming it records the current background state.
const modalStack = [];
const inertBackground = new Map();

export function hasActiveModal() {
  return modalStack.length > 0;
}

function applyBackground() {
  for (const [element, wasInert] of inertBackground) element.inert = wasInert;
  inertBackground.clear();
  const active = modalStack.at(-1);
  if (!active) return;
  active.node.inert = false;
  let branch = active.node;
  while (branch.parentElement && branch !== document.body) {
    for (const sibling of branch.parentElement.children) {
      if (sibling !== branch && !active.outsideControls.includes(sibling) && sibling instanceof HTMLElement) {
        inertBackground.set(sibling, sibling.inert);
        sibling.inert = true;
      }
    }
    branch = branch.parentElement;
  }
}

/**
 * Call after a custom modal is visible, and release before hiding it. Focus
 * returns to a suspended modal if present; the caller restores its own trigger
 * when the last modal closes. The released surface becomes inert immediately.
 */
export function containModalFocus(node, initialFocus, outsideControls = []) {
  const previous = modalStack.at(-1);
  if (previous?.node.contains(document.activeElement)) previous.focused = document.activeElement;
  const entry = { node, outsideControls, focused: initialFocus };
  modalStack.push(entry);
  applyBackground();

  const isActive = () => modalStack.at(-1) === entry;
  const focusable = () => [...node.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )].filter((el) => el.tabIndex >= 0 && !el.closest('[inert]') && el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden');

  function focusFirst() {
    (focusable()[0] || node).focus({ preventScroll: true });
  }

  function onKeydown(event) {
    if (!isActive() || event.key !== 'Tab') return;
    const elements = focusable();
    const first = elements[0];
    const last = elements[elements.length - 1];
    if (!first) {
      event.preventDefault();
      node.focus({ preventScroll: true });
    } else if (!node.contains(document.activeElement)) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus();
    } else if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function onFocusin(event) {
    if (!isActive()) return;
    if (!node.contains(event.target)) focusFirst();
    else entry.focused = event.target;
  }

  document.addEventListener('keydown', onKeydown, true);
  document.addEventListener('focusin', onFocusin, true);
  (initialFocus || focusable()[0] || node).focus({ preventScroll: true });

  let released = false;
  return () => {
    if (released) return;
    released = true;
    const wasActive = isActive();
    document.removeEventListener('keydown', onKeydown, true);
    document.removeEventListener('focusin', onFocusin, true);
    modalStack.splice(modalStack.indexOf(entry), 1);
    // If a suspended modal closes first, resuming its parent must not undo
    // that close by restoring the removed surface's former inert value.
    if (inertBackground.has(node)) inertBackground.set(node, true);
    node.inert = true;
    if (wasActive) {
      applyBackground();
      const resumed = modalStack.at(-1);
      if (resumed) (resumed.focused?.isConnected ? resumed.focused : resumed.node).focus({ preventScroll: true });
    }
  };
}
