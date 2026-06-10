// Score and grade. Formula shape adapted from Autoseed Tycoon.

export function computeScore(s) {
	const daysRemaining = Math.max(0, s.maxDay - s.day);
	const cashBonus = Math.floor(Math.max(0, s.cash) / 100);
	const resourceBonus = Math.floor((s.water + s.power) / 10);
	const efficiencyBonus = Math.max(0, 20 - s.haulUses - s.generatorUses);
	const eventSurvival = s.eventsTriggered * 3;
	return daysRemaining * 5 + cashBonus + resourceBonus + efficiencyBonus + eventSurvival;
}

export function computeGrade(score) {
	if (score >= 130) return 'S';
	if (score >= 100) return 'A';
	if (score >= 70) return 'B';
	if (score >= 40) return 'C';
	return 'D';
}

export const GRADE_LABELS = {
	S: 'Perfect build.',
	A: 'Excellent work.',
	B: 'Solid build.',
	C: 'You scraped by.',
	D: 'Barely made it.'
};
