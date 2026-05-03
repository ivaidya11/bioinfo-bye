# Broaden Your Experience Project:
This is documentation about what the project is aiming to accomplish.

## Case 1. Sequence Alignment
During this puzzle, we want the students to compare virus genomes from different individuals infected with the same virus. In the first part of the game, the students have already seen the concept of genome assembly to obtain a “reference genome” to compare to. The goal of this case is to identify mutations in the virus genome (“variant calling”) using genome sequencing data.

Through step-by-step assignments, the students can become familiar with the concepts of **genome indexing** and **exact matching**. A common strategy is to break the reference genome into shorter sequences (k-mers) and build a data structure (“index”) that allows quick identification of all locations where a specific sequence occurs. When a read needs to be aligned, the aligner does not scan the entire genome linearly. Instead, it uses the index to find candidate regions where part of the read matches the genome exactly. Once those regions are identified, the aligner performs a more detailed check to find the best match across the whole read, even allowing for a few mismatches or gaps if necessary. This two-stage process balances speed and accuracy. Once alignment is complete, the resulting data is stored in a format that includes each read’s location and how well it fits there.

After read alignment, the next step is **variant calling**, where the aligned reads are analyzed to find positions in the genome where the sample differs from the reference. The process checks how many reads support each DNA base at a given position. If the evidence is strong that a different base is present in the sample compared to the reference, it is recorded as a variant. These variants include single base changes (SNPs) as well as small insertions and deletions (indels).

## Brainstorming session:
**Sequence clustering**
- Drop sequence into frame, choose bin to put it in.
    A bit like tetris, they pile up if you don't choose fast enough
- As you level up in game, the “algorithm” highlights the relevant group region, so it becomes easier to do it fast
- Pile them in bins horizontally stacked so they align.

### - Class 3: shorter and more different sequences (or less number of clusters?)
### - Class 5: more similar clusters (more clusters?)

**Identifying conserved regions**
- Have them add the sequences from a bin into an “analyzer tool”. This creates a graph like this:
- They can stretch the sequence (for cases of insertion) or move the bin they put it in, to try to get the conserved region correct.

### - Class 3 would already have easier clusters, but maybe have them not need to adjust their sequence, just put it in and choose the conserved part

**Predicting and comparing protein structures**
This I’m the most unsure about… what part of this are we meant to be testing?

**If testing the identifying of vaccine candidates:**
- Click the structures to pop in 3D. Click a light switch to color the conserved region
- Select candidate
- If conserved reg is on the outside, and they select it, they win

- Or Same thing as before, but show animation of the antibodies, (magnet for pink?)

**If testing protein structure understanding:**
- from sequence of shapes, originally play to see what they “like” to do (ex. left click or right click for helix or sheet, or arrow keys, at a point)
- As they level up, regions of helixes and sheets get automatically converted, you just need to move them (like a little to the left)
- Next level would be “domain” recognition, entire sections are automatically generated

Or like 1024, you get tiles that when met with your sequence “evolve” to the next level of complexity:
- primary → sec folding → ternary

Unlock “longer” tiles the more you play

## Objective for now:
Develop a version of tetris, where the (DNA) sequences fall into the screen, and the students drag them into one of four "boxes" (clusters). If wrong cluster (aka, cluster already has a sequence that is not of the same group) sequence should not "latch" (maybe sound/visual effect). Sequences stay in their cluster until the end of the game.

Then, add "analysis" tool, where a certain time passes where the student can't drag anything, but the sequences are "analysed" so they get a bit of the color of their supposed cluster.

### Requirements:
**MUSTS**
1. There is a frame that sequences appear into and accumulate (tetris)
2. Student can drag sequences to a cluster
3. Sequence gets added to cluster, remains on screen
4. Game signals that sequence is in wrong cluster.

**SHOULDS**
1. There is a point based system. Students can improve score
2. There are 2 modes (3rd grade and 5th grade), WOULD: teacher can add a new set of sequences
3. There is an analysis mode that accelerates performance, and comes at a time cost from doing it manually (tune to make it good to use)