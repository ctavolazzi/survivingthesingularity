# APPENDIX E: THE CYBERDECK

*Chapter 17 gave you the workbench. This is the machine that comes off it. A cyberdeck is a personal computer you build yourself, from parts you understand, to run without a cloud, a subscription, or anyone's permission. In 2026 the culture around them stopped being niche. This appendix is a field guide: what a cyberdeck is, why it came back, and how to build one that survives the transition instead of depending on it.*

## The Word, and Where It Came From

The word is older than the hardware. William Gibson coined "cyberspace deck" in 1984, in *Neuromancer*, for the machine his console cowboys jacked into the matrix with. He never described it in detail. He has since admitted he had no clear picture of what it should look like, so he left the picture to the reader. For almost thirty years that was all a cyberdeck was: a hole in a novel, shaped exactly like the machine you wished you owned.

The hole started filling in around 2012, when the Raspberry Pi put a whole Linux computer on a credit-card board for thirty-five dollars. Suddenly the fictional deck had a plausible brain. Hobbyists began building physical versions and posting them, and a scene formed around sites like the Cyberdeck Cafe and, in 2022 and 2023, Hackaday's Cyberdeck Contests, which pulled in over a hundred builds apiece. For a decade it stayed a maker subculture: a few thousand people soldering cyberpunk props in their garages.

Then, in the spring of 2026, it stopped being niche.

## The 2026 Return

Forbes and Newsweek both ran explainers inside a few weeks of each other, describing cyberdecks as Gen Z's new DIY obsession. TechCrunch covered the same wave from a different door: a largely women-led movement teaching each other to build hyper-personal machines on TikTok and Instagram, documenting every step, turning the build itself into the content. The r/cyberDeck community was drawing tens of thousands of weekly visitors and thousands of weekly posts. The builds got stranger and more personal: a Meshtastic radio deck housed in an old clarinet case, a machine grown into wood and moss, a seashell that hides an e-reader and a local AI, an EMP-hardened "Fallout" deck loaded with offline Wikipedia and a software radio.

The interesting part is not the aesthetic. It is the stated reason. Ask the people building these why, and you do not hear "because it looks cool." You hear the argument this entire book has been making. They are building cyberdecks as a deliberate rejection of sealed, surveilled, rented consumer technology. They want a device nobody can reach into, nobody can meter, and nobody can brick from a server. One builder's line, quoted in the TechCrunch piece, could have come out of Chapter 17: no one can surveil you there, and you can get the parts at a thrift store.

That is the Smart Home Trap, understood from the inside and answered with a soldering iron. The cyberdeck movement is the Create Over Consume protocol wearing a case someone printed at two in the morning. It is worth an appendix because it is one of the few places in consumer culture where large numbers of ordinary people are voluntarily walking back out of the walled garden, on their own, without being told to. That is a signal. Signals like that are the whole reason to watch culture instead of just watching earnings calls.

## Why This Belongs in a Survival Book

Strip the aesthetics and a cyberdeck is a single object that bundles the four capabilities that keep working after the cloud goes dark:

1. **Local knowledge.** An offline copy of the reference material you would otherwise Google. The open-source Kiwix project packages all of Wikipedia, plus medical libraries, repair guides, and survival references, into files that live on the device. When the towers drop, as they do in the Chapter 17 storm, the librarian is still in your pack.
2. **Local intelligence.** A small language model running on the device itself, no network required. This is the personal-scale version of the Crucible from Chapter 11: the open-weights descendant of a public model, running air-gapped, answering to you and logging to nobody.
3. **Local communication.** A mesh radio, the same LoRa and Meshtastic hardware you built into the co-op's lattice in Chapter 17, so two decks can talk to each other across a valley on watts you can count on your fingers, with no carrier in the middle.
4. **Spectrum awareness.** A software-defined radio to listen to the world that is still broadcasting when the internet is not: weather, aircraft, marine traffic, emergency nets.

A phone does none of these once the account is suspended or the network is down. A cyberdeck does all four with the battery Chapter 17 taught you to build. The deck is not nostalgia. It is a portable, owned, offline second brain, and it is the most literal object in this book: own the tools, own the output, in a case you can open with a screwdriver.

## The Anatomy: What Actually Goes In One

There is no official parts list, which is the point. But almost every deck has the same five organs.

- **The brain.** A single-board computer. The Raspberry Pi 4 and 5 dominate because of price, community, and software support, though the Pi 5 runs hot and thirsty enough to need real cooling and a serious battery. Compute Module variants (the CM4 and CM5) let builders drop the same brain into slimmer custom bodies.
- **The body.** Increasingly, people skip the loose-parts approach and start from an integrated handheld. The ClockworkPi uConsole and the community's Hackberry Pi CM5 both ship as a screen, a real keyboard, and a battery sled built around a Compute Module. They are, essentially, cyberdecks in kit form, and they collapse a weekend of wiring into an afternoon.
- **The eyes and hands.** A small display and a physical keyboard. Mechanical, thumb, salvaged laptop, it does not matter, as long as you can read it in a field and type on it with cold fingers.
- **The loadout.** The four capabilities above, chosen for your life. A caretaker weights it toward Kiwix medical libraries. A ham operator weights it toward the radio. Nobody carries everything; the deck is a statement about what you refuse to be without.
- **The shell.** A 3D-printed enclosure, a repurposed case, or a ruggedized waterproof box. This is where the personality lives, and it is also where the survival engineering lives: a deck you actually carry into weather has to survive the weather.

Power ties it together, and it ties back to the chapter before this one. A cyberdeck is a direct-current device. It wants to run off the same 12-volt battery, the same salvaged cells, the same small solar panel you wired into your microgrid in Chapter 17. The deck is not a new dependency. It is the microgrid's first and most useful load.

## The Three Tiers: A Build Path

Do not try to build the seashell with the local AI first. Build capability in order, and let each tier work before you add the next. Every step here is something the maker community has documented to death, with parts you can buy for the price of a night out.

**Tier 1, the Communicator.** You may already own this: a Meshtastic node on a cheap Heltec or LilyGO board, flashed from your browser, paired to your phone over Bluetooth. This is the mesh from Chapter 17 in your pocket. It is off-grid text messaging with no carrier, no SIM, and no bill, and it is the single highest-value thing you can build in an afternoon.

**Tier 2, the Librarian.** A Raspberry Pi, a screen, a battery, and a copy of Kiwix loaded with the offline libraries you would actually reach for. Now you have a machine that answers questions with no signal. Add a small local language model when the hardware allows, and the librarian starts to reason, not just retrieve. Everything on it is yours, stored locally, private by construction.

**Tier 3, the Field Station.** Start from a uConsole or Hackberry Pi so the screen, keyboard, and battery are solved, then add the radio: an inexpensive receive-only RTL-SDR dongle to pull weather satellites, aircraft, and broadcast traffic out of the air. Fold in your Tier 1 mesh and your Tier 2 library, encrypt the storage, and you are holding all four survival capabilities in one case. This is the deck the Chapter 17 co-op would build for the person who walks the ridge.

## Owning the Stack Means Securing It, and Staying Legal

Two warnings, because the cyberdeck world runs right up against a line this book will not cross with you.

First, the honest part. A deck holds your life: your notes, your keys, your maps, your local model's memory of your questions. A machine you carry is a machine that gets lost or taken. Encrypt the storage. Linux full-disk encryption (LUKS) is free, built in, and turns a stolen deck from a confession into a brick. Owning your stack is not finished until you have secured it against the day it leaves your hands.

Second, the boundary. The same hardware skills that build a survival deck overlap heavily with offensive security work: the maker scene and the penetration-testing scene share parts, forums, and vocabulary, and a lot of cyberdeck content online is really about network intrusion. This book's use of a cyberdeck is defensive and sovereign, never offensive, and there are two hard lines with real prison behind them:

- **Access.** Touching a computer or network you are not authorized to touch is a federal crime under the Computer Fraud and Abuse Act, not a hobby. Authorization is binary and it is written down. A deck does not change that; it just makes it easier to break by accident.
- **Spectrum.** Listening is broad and mostly legal. Transmitting is not. Under the FCC's rules, receiving weather, aircraft, and broadcast signals with an SDR is fine. Transmitting on licensed frequencies, jamming, or intercepting private communications is illegal, tracked, and enforced. Listen freely. Transmit only where you are licensed to.

Build the deck to keep yourself free. Not to reach into anyone else's life. The whole moral architecture of this book is the difference between those two, and the tool does not decide it for you. You do.

## The Precedent

In 1968 Stewart Brand put three words on the cover of the *Whole Earth Catalog*: Access to Tools (Precedent P-20). The catalog was a map of possible selves, a list of the machines that would let an ordinary person educate themselves, feed themselves, and build their own world. The cyberdeck is that catalog collapsed into a single object. It is what Brand's black paperback was pointing at all along: not a computer you are allowed to use, but a computer you understand, can repair, and cannot be locked out of.

The culture rediscovered this in 2026, ten of thousands of people at a time, and mostly by feel, because sealed consumer technology had finally gotten frightening enough to push them back to the soldering iron. You do not have to wait to be pushed.

**The practice.**

1. **Build the Communicator this month.** One Meshtastic node, flashed from your browser, paired to your phone. Off-grid messaging you own, for the price of a pizza. It is the fastest way to feel the difference between a rented network and one that is yours.
2. **Load a Librarian.** Put Kiwix and one offline library, medical, repair, or the full Wikipedia, onto a Raspberry Pi or even an old phone. Now you own an answer machine that works with the towers down.
3. **Run one model with the network unplugged.** Get a small language model answering on a device with the Wi-Fi physically off. The first time it works, you will understand the Crucible from Chapter 11 in your hands instead of on the page: intelligence that is local, private, and cannot be revoked.

Three weekends. At the end of them you are not carrying a phone that belongs to someone else. You are carrying a deck that belongs to you.
