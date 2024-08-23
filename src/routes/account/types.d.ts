import type { PageLoad } from './$types';

export type PageData = Awaited<ReturnType<PageLoad>>;