import { writable } from 'svelte/store';

function createDownloadStats() {
    const initialStats = {
        totalDownloads: 1287,
        recentDownloads: 0,
        startTime: Date.now()
    };

    const { subscribe, update } = writable(initialStats);

    return {
        subscribe,
        incrementDownloads: () => update(stats => {
            const currentTime = Date.now();
            const timePassed = (currentTime - stats.startTime) / 1000; // in seconds
            const totalNewDownloads = Math.floor(timePassed / 5) * 2; // Assume average of 2 downloads every 5 seconds
            const recentDownloads = Math.min(3, totalNewDownloads - (stats.totalDownloads - initialStats.totalDownloads));

            return {
                totalDownloads: initialStats.totalDownloads + totalNewDownloads,
                recentDownloads,
                startTime: stats.startTime
            };
        })
    };
}

export const downloadStats = createDownloadStats();