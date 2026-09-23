# APPENDIX E: THE CYBERDECK

*Chapter 17 gave you the workbench. This is the machine that can come off it. A cyberdeck is a personal computer you build yourself, from parts you understand, to run without a cloud, a subscription, or anyone's permission. It's optional. Everything here starts with the device already in your pocket.*

![A homemade cyberdeck: a rugged hard case holding a mechanical keyboard, an amber map-lit screen, and a stub antenna](/book-images/appe-cyberdeck.png)

*A computer you understand all the way down, that answers to nobody's server.*

## The word, and where it came from

The word is older than the hardware. William Gibson coined "cyberspace deck" in 1984, in *Neuromancer*, for the machine his console cowboys jacked into the matrix with. He never described it in much detail, so for almost thirty years a cyberdeck was a hole in a novel, shaped exactly like the machine you wished you owned.

The hole started filling in around 2012, when the Raspberry Pi put a whole Linux computer on a credit-card board for thirty-five dollars. Suddenly the fictional deck had a plausible brain. Hobbyists began building physical versions and posting them, and a scene formed around community sites and Hackaday's cyberdeck contests. For a decade it stayed a maker subculture.

Then, in 2026, it stopped being niche.

## The 2026 return

Newsweek ran an explainer calling cyberdecks Gen Z's new DIY obsession. [Newsweek, What is a cyberdeck](https://www.newsweek.com/what-is-a-cyberdeck-gen-zs-new-custom-computing-obsession-11787017) TechCrunch covered the same wave from a different door: communities that had exploded thanks largely to women on social media, building artistic, hyper-personal machines and documenting every step, including one builder's seashell that hides a small computer and a local AI. [TechCrunch, Cyberdecks are having a moment](https://techcrunch.com/2026/06/02/cyberdeck-tiktok-trend-reject-big-tech/)

The interesting part isn't the look. It's the stated reason. Ask the people building these why, and a lot of them give you the argument this book has been making: they want a device that's theirs, that isn't quietly watching them, that nobody can meter or brick from a server, and that they can fix with parts from a thrift store.

That's the smart-home trap from Chapter 17, understood from the inside and answered with a soldering iron. It's Create Over Consume wearing a case somebody printed at two in the morning. And it's worth an appendix because it's one of the few places in consumer culture where lots of ordinary people are voluntarily walking back out of the walled garden, on their own. That's a signal. Signals like that are why you watch culture and not just earnings calls.

## Why this belongs in a survival book

Strip the aesthetics and a cyberdeck bundles four capabilities that keep working when the network doesn't:

1. **Local knowledge.** An offline copy of the reference material you'd otherwise search for. The open-source Kiwix project packages all of Wikipedia, plus medical libraries, repair guides, and more, into files that live on the device. When the towers drop, as they do in the Chapter 17 storm, the librarian is still in your pack.
2. **Local intelligence.** A small language model running on the device itself, no network required: a pocket version of the Crucible from Chapter 11. Its answers still need checking, like any model's.
3. **Local communication.** A mesh radio, the same LoRa and Meshtastic hardware as the co-op's network, so two devices can pass short messages across a valley with no carrier in the middle.
4. **Spectrum awareness.** A cheap receive-only software-defined radio, to listen to the world that's still broadcasting when the internet isn't: weather, aircraft, emergency nets.

Here's the honest part: a phone can do a surprising amount of this too. Kiwix runs on phones. A Meshtastic radio pairs with one over Bluetooth. Small models run on recent phones. What a phone usually can't do is let you open it, repair it, swap its parts, or run it for years without an account somewhere. That's the gap a deck fills. Neither one is required to take part in anything in this book.

## The anatomy

There's no official parts list, which is the point. But most decks have the same five organs.

- **The brain.** A single-board computer. The Raspberry Pi dominates because of price, community, and software; the newest models run hot enough to need real cooling and a real battery. Compute Module versions drop the same brain into slimmer custom bodies.
- **The body.** More and more people start from an integrated handheld kit, like the ClockworkPi uConsole or the community-built Hackberry Pi, which ship with a screen, keyboard, and battery sled already solved. They turn a weekend of wiring into an afternoon.
- **The eyes and hands.** A small display and a physical keyboard you can read in a field and type on with cold fingers.
- **The loadout.** The four capabilities above, chosen for your life. A caregiver leans toward medical libraries. A ham operator leans toward the radio. Nobody carries everything; the deck is a statement about what you refuse to be without.
- **The shell.** A printed enclosure, a repurposed case, or a waterproof box. That's where the personality lives, and where the weatherproofing lives.

Power ties it together. Most decks run on low-voltage DC, from a packaged battery with its own protection circuit or a small power station, which makes them a natural first load for the DC corner in Chapter 17. Don't build lithium packs from salvaged cells unless you've been properly taught; buy a protected pack.

## The three tiers

Don't start with the seashell that runs a local AI. Build capability in order, and let each tier work before you add the next.

**Tier 0, the phone you have.** Save one non-sensitive reference you're allowed to copy, turn off the network, and confirm you can open it and find what you need. Write down its source and date so you'll know when it's stale. That's the offline habit, for free.

**Tier 1, the Communicator.** A Meshtastic node on a cheap Heltec or LilyGO board, flashed from your browser, paired to your phone. Off-grid text messaging with no carrier and no bill, for about the price of a pizza. It's the highest-value thing you can build in an afternoon.

**Tier 2, the Librarian.** A Raspberry Pi, a screen, a protected battery, and Kiwix loaded with the libraries you'd actually reach for. Now you have a machine that answers questions with no signal. Add a small local model when the hardware allows.

**Tier 3, the Field Station.** Start from a handheld kit so the screen, keyboard, and battery are solved, then add a receive-only software-defined radio for weather and aircraft. Fold in your mesh radio and your library, encrypt the storage, and you're holding all four capabilities in one case.

## Owning the stack means securing it, and staying legal

Two warnings, because the cyberdeck world runs right up against lines this book won't cross with you.

First, the honest part. A deck holds your life: notes, keys, maps, your questions. A machine you carry is a machine that can get lost or taken. Encrypt the storage; Linux full-disk encryption is free and built in, and it turns a stolen deck from a confession into a brick. And a local machine isn't automatically safe: it still needs updates from sources you've verified, sensible passwords, and a clear idea of what it's connected to.

Second, the boundary. The same hardware skills overlap with offensive security work, and a lot of cyberdeck content online is really about getting into other people's networks. This book's use is defensive and personal, never offensive, and there are two hard lines with real penalties behind them:

- **Access.** Touching a computer or network you aren't authorized to touch is a crime in most places, including under the US Computer Fraud and Abuse Act. A deck doesn't change that.
- **Spectrum.** Listening is broad and mostly legal. Transmitting isn't. Receiving weather, aircraft, and broadcast signals is generally fine; transmitting on frequencies you aren't licensed for, jamming, or intercepting private communications is illegal. Listen freely. Transmit only where you're allowed to.

Build the deck to keep yourself free, not to reach into anyone else's life. The tool doesn't decide that for you. You do.

## The practice

In 1968 Stewart Brand put three words on the cover of the *Whole Earth Catalog*: Access to Tools (P-21). The cyberdeck is that catalog collapsed into one object: not a computer you're allowed to use, but a computer you understand, can repair, and can't be locked out of.

1. **Build the Communicator this month.** One Meshtastic node, flashed from your browser, paired to your phone. It's the fastest way to feel the difference between a rented network and one that's yours.
2. **Load a Librarian.** Put Kiwix and one offline library, medical, repair, or all of Wikipedia, onto a Raspberry Pi or an old phone. Now you own an answer machine that works with the towers down.
3. **Run one model with the network unplugged.** Get a small language model answering on a device with the Wi-Fi physically off. The first time it works, you'll understand the Crucible from Chapter 11 in your hands instead of on the page.

Three weekends. At the end of them you're not only carrying a phone that belongs to someone else. You're carrying something that belongs to you.
