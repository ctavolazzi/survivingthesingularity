/**
 * White Rabbit — Diagnostic Trace System
 *
 * "Follow the rabbit." A passable trace object that records execution flow.
 * Drop a rabbit into any component, route, or server hook — it hops through
 * your code and records everything it sees. Pass it around. Follow it later.
 *
 * Usage:
 *   import { createRabbit, getRabbit } from '$lib/debug/white-rabbit.js';
 *
 *   // Release a rabbit into your code
 *   const rabbit = createRabbit('homepage-load');
 *
 *   // It records what it sees
 *   rabbit.info('Component mounted', { name: 'Hero' });
 *   rabbit.warn('Slow render detected', { ms: 450 });
 *   rabbit.error('API call failed', { status: 500 });
 *   rabbit.mark('hero-visible');  // Performance checkpoint
 *
 *   // Pass it to child components — follow the rabbit
 *   childComponent.init(rabbit);
 *
 *   // When you're ready, read the rabbit's journal
 *   const report = rabbit.report();
 *
 *   // Spawn baby rabbits for sub-operations
 *   const baby = rabbit.spawn('fetch-data');
 */

import { browser } from '$app/environment';
import { writable } from 'svelte/store';

// The Warren — global registry of all rabbits
const warren = new Map();

// Store for reactive UI access
export const activeRabbits = writable([]);

// Severity levels
const LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };

// Config
const CONFIG = {
  enabled: true,
  minLevel: 'debug',
  consoleOutput: true,
  maxEntries: 1000,
  persistToStorage: true,
  storageKey: 'sts-rabbit-traces'
};

let burrowCount = 0;

/**
 * Generate a unique rabbit ID
 */
function generateRabbitId() {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `rabbit-${timestamp}-${random}-${++burrowCount}`;
}

/**
 * Release a new White Rabbit into your code
 * @param {string} name - Human-readable name for this trace
 * @param {object} metadata - Optional metadata to attach
 * @returns {WhiteRabbit}
 */
export function createRabbit(name, metadata = {}) {
  const rabbit = new WhiteRabbit(name, metadata);
  warren.set(rabbit.id, rabbit);
  activeRabbits.update(rabbits => [...rabbits, rabbit.summary()]);
  return rabbit;
}

/**
 * Find a rabbit by ID
 */
export function getRabbit(id) {
  return warren.get(id) || null;
}

/**
 * Get all rabbits in the warren
 */
export function getAllRabbits() {
  return Array.from(warren.values());
}

/**
 * Clear rabbits that have finished their journey
 */
export function clearFinishedRabbits() {
  for (const [id, rabbit] of warren) {
    if (rabbit.returned) {
      warren.delete(id);
    }
  }
  activeRabbits.set(Array.from(warren.values()).map(r => r.summary()));
}

/**
 * Export all rabbit journals as JSON
 */
export function exportJournals() {
  const journals = Array.from(warren.values()).map(rabbit => rabbit.report());
  return JSON.stringify(journals, null, 2);
}

class WhiteRabbit {
  constructor(name, metadata = {}) {
    this.id = generateRabbitId();
    this.name = name;
    this.metadata = metadata;
    this.journal = [];       // The rabbit's log of everything it saw
    this.checkpoints = {};   // Performance marks — places the rabbit stopped
    this.startTime = Date.now();
    this.endTime = null;
    this.returned = false;   // Has the rabbit come back from its journey?
    this.parentId = metadata.parentId || null;
    this.litter = [];        // Child rabbit IDs

    this._record('info', `🐇 Rabbit "${name}" released`, { id: this.id });
  }

  /**
   * Spawn a baby rabbit for a sub-operation
   */
  spawn(name, metadata = {}) {
    const baby = createRabbit(name, { ...metadata, parentId: this.id });
    this.litter.push(baby.id);
    this._record('debug', `Spawned: ${name}`, { childId: baby.id });
    return baby;
  }

  /**
   * Record observations at different severity levels
   */
  debug(message, data) { this._record('debug', message, data); }
  info(message, data) { this._record('info', message, data); }
  warn(message, data) { this._record('warn', message, data); }
  error(message, data) { this._record('error', message, data); }

  /**
   * Drop a checkpoint — the rabbit pauses here and notes the time
   */
  mark(label) {
    const now = Date.now();
    const elapsed = now - this.startTime;
    this.checkpoints[label] = { timestamp: now, elapsed };
    this._record('debug', `CHECKPOINT: ${label}`, { elapsed: `${elapsed}ms` });
    return elapsed;
  }

  /**
   * Measure distance between two checkpoints
   */
  measure(label, startCheckpoint, endCheckpoint) {
    const start = this.checkpoints[startCheckpoint];
    const end = this.checkpoints[endCheckpoint];
    if (!start || !end) {
      this._record('warn', `Cannot measure "${label}": missing checkpoint`, { startCheckpoint, endCheckpoint });
      return null;
    }
    const duration = end.elapsed - start.elapsed;
    this._record('info', `MEASURE: ${label} = ${duration}ms`, { startCheckpoint, endCheckpoint, duration });
    return duration;
  }

  /**
   * Time an async operation — the rabbit watches and waits
   */
  async time(label, fn) {
    this.mark(`${label}-start`);
    try {
      const result = await fn();
      this.mark(`${label}-end`);
      const duration = this.checkpoints[`${label}-end`].elapsed - this.checkpoints[`${label}-start`].elapsed;
      this._record('info', `TIMED: ${label} = ${duration}ms`);
      return result;
    } catch (err) {
      this.mark(`${label}-error`);
      this._record('error', `TIMED: ${label} failed`, { error: err.message });
      throw err;
    }
  }

  /**
   * Watch a component's lifecycle
   */
  watchComponent(name) {
    const mountTime = Date.now();
    this._record('debug', `Component mount: ${name}`);

    return {
      rendered: () => {
        const renderTime = Date.now() - mountTime;
        this._record(renderTime > 100 ? 'warn' : 'debug', `Component render: ${name}`, { renderTime: `${renderTime}ms` });
      },
      destroyed: () => {
        const lifetime = Date.now() - mountTime;
        this._record('debug', `Component destroy: ${name}`, { lifetime: `${lifetime}ms` });
      }
    };
  }

  /**
   * Watch a navigation event
   */
  watchNavigation(from, to) {
    this._record('info', `Navigate: ${from} → ${to}`);
    this.mark(`nav-${to}`);
  }

  /**
   * Watch an API call
   */
  watchApiCall(method, url, status, duration) {
    const level = status >= 500 ? 'error' : status >= 400 ? 'warn' : 'info';
    this._record(level, `API ${method} ${url}`, { status, duration: `${duration}ms` });
  }

  /**
   * The rabbit returns — trace complete
   */
  returned_home(summary) {
    this.endTime = Date.now();
    this.returned = true;
    const duration = this.endTime - this.startTime;
    this._record('info', `🐇 Rabbit "${this.name}" returned home`, { totalDuration: `${duration}ms`, summary });

    if (CONFIG.persistToStorage && browser) {
      this._persist();
    }

    activeRabbits.update(rabbits =>
      rabbits.map(r => r.id === this.id ? this.summary() : r)
    );
  }

  /**
   * Quick summary of the rabbit's journey
   */
  summary() {
    const errorCount = this.journal.filter(e => e.level === 'error').length;
    const warnCount = this.journal.filter(e => e.level === 'warn').length;
    return {
      id: this.id,
      name: this.name,
      entries: this.journal.length,
      errors: errorCount,
      warnings: warnCount,
      duration: (this.endTime || Date.now()) - this.startTime,
      returned: this.returned,
      parentId: this.parentId,
      litter: this.litter
    };
  }

  /**
   * Full report — the rabbit's complete journal
   */
  report() {
    return {
      id: this.id,
      name: this.name,
      metadata: this.metadata,
      startTime: new Date(this.startTime).toISOString(),
      endTime: this.endTime ? new Date(this.endTime).toISOString() : null,
      duration: (this.endTime || Date.now()) - this.startTime,
      returned: this.returned,
      parentId: this.parentId,
      litter: this.litter,
      checkpoints: this.checkpoints,
      journal: this.journal,
      summary: this.summary()
    };
  }

  /**
   * Internal — the rabbit writes in its journal
   */
  _record(level, message, data) {
    if (!CONFIG.enabled) return;
    if (LEVELS[level] < LEVELS[CONFIG.minLevel]) return;
    if (this.journal.length >= CONFIG.maxEntries) return;

    const entry = {
      timestamp: Date.now(),
      elapsed: Date.now() - this.startTime,
      level,
      message,
      data: data || null
    };

    this.journal.push(entry);

    if (CONFIG.consoleOutput && browser) {
      const prefix = `[🐇 ${this.name}]`;
      const style = {
        debug: 'color: #64748b',
        info: 'color: #3b82f6',
        warn: 'color: #f59e0b',
        error: 'color: #ef4444; font-weight: bold'
      }[level];

      console[level === 'debug' ? 'log' : level](
        `%c${prefix} ${message}`,
        style,
        data || ''
      );
    }
  }

  /**
   * Persist the journal to localStorage
   */
  _persist() {
    if (!browser) return;
    try {
      const existing = JSON.parse(localStorage.getItem(CONFIG.storageKey) || '[]');
      existing.push(this.report());
      const trimmed = existing.slice(-50);
      localStorage.setItem(CONFIG.storageKey, JSON.stringify(trimmed));
    } catch {
      // Storage full or unavailable — the rabbit drops its journal
    }
  }
}

/**
 * Load persisted rabbit journals from localStorage
 */
export function loadJournals() {
  if (!browser) return [];
  try {
    return JSON.parse(localStorage.getItem(CONFIG.storageKey) || '[]');
  } catch {
    return [];
  }
}

/**
 * Clear all persisted journals
 */
export function clearJournals() {
  if (!browser) return;
  localStorage.removeItem(CONFIG.storageKey);
}

/**
 * Server-side rabbit — for hooks.server.js and +server.js
 */
export function createServerRabbit(name, metadata = {}) {
  const rabbit = new WhiteRabbit(name, { ...metadata, environment: 'server' });
  return rabbit;
}
