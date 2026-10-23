---
title: Notes from My FDM 3D Printing Adventures
description: A complete tinkering log of getting into FDM 3D printing over the summer, covering printer selection, first prints, getting started with Fusion 360 modeling, multi-color printing, a phone stand project, and a detailed troubleshooting summary of PETG material and process preset tuning.

date: 2026-10-23T00:00:00+08:00
lastmod: 2026-10-23T21:51:19+08:00

categories:
  - Tech
  - Tinkering
tags:
  - 3D Printing
  - FDM
  - Fusion 360
  - PETG
---

## Before Print

In mid-July 2026, during summer vacation, Xiaodeng had just completed a change of major and transferred to a new college. As a rising sophomore, life during the summer break was wonderfully laid-back. This impulsive shopaholic with a three-minute attention span stumbled by accident into a brand-new hobby: 3D printing.

For a 3D printing newcomer, FDM printers are the obvious choice — first, because FDM precision is more than sufficient for beginners, and second, because there was absolutely no desire to be poisoned by all the various resins involved in resin printing.

After binge-watching videos on Bilibili for a few days, the choice came down to the Bambu Lab A1, the Creality i7, and the ANYCUBIC Kobra X. The ANYCUBIC Kobra X ultimately won out, mainly because achieving multi-color printing with that setup costs the least among the three options.

## First Attempts

On 2026-7-20, the package arrived. The very first model printed was the "3D Benchy Dragon" — a fairly classic model that takes advantage of 3D printing's self-assembly properties.
![Print Log 1](image.png)

Over the following days, attempts were made to design a way to mount the filament rack on the back of a chair — a plan that was ultimately abandoned. The initial approach was to use GPT-5.6-sol for modeling, but after getting frustrated and rage-quitting several times, it was time to head back to Bilibili and actually learn how to model properly.

## Modeling

For a complete beginner, the first step in learning 3D modeling is naturally choosing the right software. The first attempt was with the only modeling software known at the time: Blender. It's open-source, which is great, but the biggest issue is that the goal was to design engineering test parts rather than artistic models, so it wasn't really a good fit. SolidWorks is supposedly very powerful, but since the primary machine is a MacBook, that was a non-starter. In the end, Fusion (free for students — what a civilized policy!) was chosen as the gateway into modeling.

Following this Bilibili creator's tutorial series: https://www.bilibili.com/video/BV1xX4y1E7nG/?spm_id_from=333.788.videopod.episodes&vd_source=ccc9945c4f1f3370dd60b4bd9d2429a6, Fusion modeling was learned in a fairly systematic way — watching and practicing simultaneously. Of course, since there was no need for surface modeling at the time, the learning stopped at the assembly section.
![Modeling Tutorial](image-1.png)

During this period, a few small gadgets were modeled and printed to test what had been learned.

![Radish Tower Bracket](image-2.png)

## BUG

😠 The white PLA filament included in the ANYCUBIC bundle is defective — every print fails halfway through with a clog error 😠. After trying every fix imaginable for a long time, it was sent back and a spool of gray filament was shipped in return. Every other filament used on this machine has printed without incident — it's only that one official white PLA spool that causes this 😡.

## First Attempts at Multi-Color Printing

On 2026-7-21, an attempt was made to print a slug model of Kaguya-hime from Beyond Time. At the time, it wasn't known that you could open a `*.3mf` file directly in modeling software to edit parameters and slice it, so the STL was imported manually and colored by hand — an incredibly painful process with mediocre results. It was only later discovered that `*.3mf` files can be opened directly and parameters modified before slicing.

## Phone Stand Project

After spotting a wireless-charging phone stand project for iPhone on Bilibili, the corresponding project was found on MakerWorld — but it was designed for newer iPhone models and wasn't compatible with the iPhone SE3. Attempts were made to have GPT-5.6-sol modify the model, but after several iterations the dimensions were still off. In the end, a roughly equivalent stand was modeled from scratch.
![iPhone Stand](image-3.png)

## Building Custom Material and Process Presets

Beyond the projects mentioned above, many other things were printed along the way. Gradually, dissatisfaction with print speed grew, and experimentation began on how to push speeds higher and refine the relevant presets.

The first attempt was to reuse the official configuration provided by the filament manufacturer (Dasimple). It turned out that configuration was quite incomplete and had a number of issues. Eventually, Bambu Lab's and ANYCUBIC's configurations were referenced extensively to build a custom PETG profile.

AI tools were used extensively throughout this process as well.

After a great deal of experimentation, a fairly solid configuration was achieved — acceleration was pushed to the machine's upper limit, and volumetric flow was increased to approximately 20 mm³/s.

### A summary of pitfalls encountered during the process (ANYCUBIC's official slicer is based on OrcaSlicer):

1. Cubic infill slices faster but at high speed the nozzle crashes into already-printed infill. Cubic infill offers relatively high strength and slices quickly, but under high-speed printing conditions the nozzle collides with already-printed portions of the current layer's infill and destroys it completely. The recommended approach is to use gyroid or a similar infill pattern that prevents the nozzle from striking the infill.

2. The speed settings in process adjustments cannot always actually be reached. The true maximum speed is limited by the volumetric flow rate of the filament, and accelerating to top speed typically requires several centimeters of travel distance (depending on the acceleration value set in the printer settings).

3. "Infill combination 2" does not simply make infill more solid — it actually increases the top-span of sparse infill, which in turn raises the minimum required infill density (because an excessively large sparse infill top-span means the solid top layers face too large a bridging gap, so infill density must be increased to reduce that span).

4. When printing a volumetric flow rate test tower, always use the line width that will be used in production. The maximum flow rate obtained should also be multiplied by a safety factor (e.g., 0.8) to ensure stable printing.

5. Measuring the extrusion multiplier is fairly tedious, and getting it wrong causes severe and unstable layer-line artifacts. It is recommended to use the flow rate calibration function built into the slicer.
![Flow Rate Calibration](image-4.png)

6. Enabling bed leveling during a print has a bug — it is recommended to perform leveling before starting the print, verify the first layer, and then leave the leveling switch off for subsequent prints.

7. Changing the layer count does not always actually take effect. The number of solid top and bottom layers also depends on the minimum thickness setting — the actual value will not be less than the number of layers corresponding to the top/bottom shell thickness.

8. PETG + PLA dissolvable/dissimilar-material supports are easy to remove but also difficult to bond. This is especially true when trying to use one or two layers of PLA directly on the build plate as a raft layer — PETG, and particularly its support structures, will barely stick at all.

9. A profile setting of "no fan for the first three layers" may still result in the fan running at full speed. This was consistently reproduced when using dissimilar-material supports and is suspected to be a machine firmware bug.

10. Bed temperature must balance adhesion and part removal. Cooling is not a universal solution — as long as the print sticks, lower is better.

11. General presets handle the common baseline; model-specific issues should be handled individually. Infill density, wall count, and top/bottom layer counts all need to be adjusted based on the actual situation.

12. PETG bonds quite firmly to the build plate — consider skipping the brim to make part removal easier.

### Key settings for dissimilar-material supports

1. Choose tree or normal support type based on the actual geometry.

2. Set the support body material to automatic, so it follows the model material — PETG for PETG models (or PLA for PLA models).

3. Set the contact interface material to a different material from the model body (remember to add the new material to the filament list first).

4. Set both top and bottom interface layer counts to two layers.

5. Set both top and bottom interface line spacing to 0 mm to form a solid interface.

6. Set both top and bottom Z-gap to 0 mm so the interface layers make direct contact with the model and support, improving bond strength.

7. Disable "use interface material for support body" to restrict the dissimilar material to the contact interface only.

8. Set raft layers to 0. Raft layers are layers printed directly on the build plate and are unrelated to supports — they can actually cause insufficient adhesion and bed-sticking failures in areas where the model has a small contact footprint.

9. Support XY distance from model and support first-layer distance from model: leave a small gap of 0.x mm to prevent them from fusing together.

10. Generate supports from build plate only: enable based on actual geometry.

**The intent of these settings is to make the interface adhere tightly to the model and minimize bottom-surface overhangs, while exploiting the material difference between PLA and PETG to make removal easy.**

#### On purge towers and flushing

**Because insufficient flushing when using dissimilar-material supports can easily cause excessive Z-direction strength loss near the support interface, it is recommended to maximize flushing volume and purge tower usage as much as possible.**

That's all for now — will pick this back up whenever the mood strikes 🐱
