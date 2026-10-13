// Bound the complete request, including a response body that stalls after its
// headers arrive. A timeout describes an unknown outcome, not a failed write.
export class RequestTimeoutError extends Error {
  constructor() {
    super('The request timed out before its result could be confirmed.');
    this.name = 'RequestTimeoutError';
  }
}

export async function requestJson(url, options = {}, timeoutMs = 30_000) {
  const controller = new AbortController();
  let timedOut = false;
  const timer = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, timeoutMs);

  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    let data;
    try {
      data = await response.json();
    } catch (error) {
      if (controller.signal.aborted) throw error;
      data = {};
    }
    return { response, data: data && typeof data === 'object' ? data : {} };
  } catch (error) {
    if (timedOut) throw new RequestTimeoutError();
    throw error;
  } finally {
    clearTimeout(timer);
  }
}
