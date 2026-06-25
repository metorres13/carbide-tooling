#!/usr/bin/env python3
"""
Enhance carbide-tooling.com tools with SEO content:
- 3 unique H2 sections per tool
- FAQ section with 3 Q&A items
- B2B conversion line
"""

import os, re, sys

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

# Tool-specific SEO content: H2s, paragraphs, and FAQ items
# Keyed by directory name
SEED = {
    "aluminum-alloy-table": {
        "h2s": [
            ("6061 Aluminum: Composition & Machinability", "6061 aluminum is one of the most widely used alloys in CNC machining, offering excellent corrosion resistance, weldability, and moderate strength. With a machinability rating of 70%, it produces good chip formation and surface finish at cutting speeds of 600–1,000 SFM. Its balanced composition of magnesium and silicon makes it ideal for structural components, automotive brackets, and consumer electronics enclosures where moderate strength and corrosion resistance are required."),
            ("7075 Aluminum: High-Strength Applications", "7075 aluminum is the go-to alloy for aerospace and high-stress applications, boasting tensile strength comparable to many steels. Its zinc as the primary alloying element delivers a machinability rating of 50%, requiring sharper tools and reduced speeds around 300–600 SFM. Common applications include aircraft structural parts, rock climbing equipment, and high-performance bicycle components where weight savings and strength are critical."),
            ("Selecting the Right Alloy for Your CNC Job", "The choice between 6061 and 7075 depends on your specific part requirements: 6061 offers better corrosion resistance and weldability at lower cost, while 7075 provides superior strength-to-weight ratio at a premium. For prototyping and general machining, 6061 is typically preferred. For production parts under high cyclic loading, 7075's fatigue strength justifies the additional material cost."),
        ],
        "faqs": [
            ("Which aluminum alloy is easiest to machine?", "6061 aluminum is considered the most machinable common alloy, producing consistent chip breakage and excellent surface finishes. 7075 requires more attention to tool sharpness and speeds. For complex geometries with tight tolerances, 6061 is typically the safer choice."),
            ("Can I use the same tooling for 6061 and 7075?", "Yes, with adjustments. Carbide end mills work well for both alloys. Reduce spindle speed by 30–40% when switching from 6061 to 7075, and ensure adequate coolant flow to manage the higher cutting forces of 7075."),
            ("Does heat treatment affect machinability of these alloys?", "Yes. 6061-T6 and 7075-T6 are the most common tempers for machining. The T6 condition provides good strength while maintaining acceptable machinability. Over-aged tempers may reduce strength but offer slightly better chip formation."),
        ],
    },
    "blind-hole-tapping-calculator": {
        "h2s": [
            ("Understanding Blind Hole Tap Depth Requirements", "Blind hole tapping requires precise depth control to avoid bottoming out the tap, which can cause tool breakage or thread damage. The minimum full thread depth for most applications is 1.5× the nominal thread diameter. Accounting for the tap's chamfer length (typically 3–5 threads) and adding a 2–3 mm safety clearance ensures reliable tapping without risking the tap or the workpiece."),
            ("Calculating Tap Drill Depth for Blind Holes", "The tap drill depth must account for both the thread engagement length and the tap's lead. For a standard plug chamfer tap, add 5 threads of extra depth beyond the required thread length. Using the formula: Drill Depth = Required Thread Depth + (5 × Pitch) + 1 mm, you can confidently program blind hole cycles without worrying about tap-to-bottom collision."),
            ("Common Blind Hole Tapping Mistakes to Avoid", "The most frequent errors include insufficient drill depth, using the wrong tap style (bottoming vs. plug chamfer), and inadequate chip evacuation. For blind holes deeper than 2× diameter, consider spiral flute taps that pull chips out of the hole, reducing the risk of chip packing that leads to tap breakage."),
        ],
        "faqs": [
            ("What is the minimum thread engagement for blind holes in aluminum?", "For aluminum and other non-ferrous materials, 1.5× the nominal diameter of thread engagement is sufficient for most applications. For steel and stainless steel, 1.0× diameter is typically adequate. Always verify against your engineering requirements."),
            ("Should I use a forming tap for blind holes?", "Forming (roll) taps are not recommended for blind holes because they require 40–60% more torque and generate significant radial force that can deform thin-walled features. Use cutting taps with spiral flute geometry for blind hole applications."),
            ("How do I program chip breaking for blind hole tapping?", "Use rigid tapping cycles with peck tapping if your CNC control supports it (G84.2 or M29). Otherwise, program a dwell at the bottom of the hole before reversal to allow chips to clear. Reduce tapping speed by 20% for blind holes deeper than 2× diameter."),
        ],
    },
    "brass-machining-parameters": {
        "h2s": [
            ("Optimal Cutting Speeds for Brass Alloys", "Brass alloys, particularly free-machining grades like C36000, can be cut at speeds of 800–1,500 SFM with carbide tooling — significantly faster than steel. The high zinc content creates short, broken chips that prevent built-up edge formation. For leaded brasses, surface finishes below 32 μin Ra are achievable with single-pass finishing at moderate feed rates."),
            ("Feed Rate Selection for Brass Turning and Milling", "Brass's excellent machinability allows aggressive feed rates without sacrificing surface quality. For roughing operations, use 0.008–0.015 in/rev for turning and 0.004–0.008 in/tooth for milling. Finishing passes can run at 0.003–0.006 in/rev. The low cutting forces mean you can push feed rates up to 80% higher than with 4140 steel while maintaining tool life."),
            ("Tool Geometry Recommendations for Copper Alloys", "For brass and copper alloys, use tools with positive rake angles (12–18°) and sharp cutting edges to minimize work hardening. Polished flute tools reduce chip adhesion in drilling operations. Uncoated carbide or CVD diamond-coated tools offer the best combination of edge sharpness and wear resistance for high-volume brass machining."),
        ],
        "faqs": [
            ("Why does brass machine so much easier than steel?", "Brass's high zinc content (over 30%) creates a brittle chip structure that breaks into small fragments, reducing cutting forces and heat generation. This self-chipping behavior eliminates built-up edge formation and allows much higher cutting speeds than steel."),
            ("Do I need coolant when machining brass?", "While brass can be machined dry due to its low thermal conductivity and self-lubricating properties, using coolant improves surface finish and dimensional accuracy by controlling thermal expansion. For tight tolerances (under ±0.001\"), flood coolant is recommended."),
            ("What is the best grade of brass for CNC machining?", "C36000 (free-machining brass) is the gold standard for CNC work, offering the highest machinability rating of 100%. For applications requiring lead-free material, C27400 or C26000 (cartridge brass) provide good alternatives with slightly reduced machining speeds."),
        ],
    },
    "carbide-grade-cross-ref-2": {
        "h2s": [
            ("ISO Grade Classification: P, M, K, N, S, H", "Carbide inserts are classified under ISO standard 513 into six main groups based on workpiece material. P-grades (blue) are for steel machining, M-grades (yellow) for stainless steel, K-grades (red) for cast iron, N-grades (green) for aluminum, S-grades (brown) for superalloys, and H-grades (grey) for hardened steel. Each grade balances toughness and wear resistance differently."),
            ("Cross-Referencing Top Brands: Sandvik, Iscar, Kennametal", "When switching between brands, the ISO classification provides a starting point but doesn't tell the full story. Sandvik's GC4415 roughly corresponds to Kennametal KCP25 and Iscar IC8250 for turning steel. However, coating technology and substrate differences mean that a direct replacement may perform differently in interrupted cuts or high-speed finishing."),
            ("Coating Technology and Application Matching", "Modern carbide grades use CVD (chemical vapor deposition) or PVD (physical vapor deposition) coatings. CVD coatings with multiple alumina layers excel at high-speed steel turning where crater wear is the primary failure mode. PVD-coated grades with TiAlN or AlTiN coatings are preferred for milling and drilling where edge toughness and thermal shock resistance are critical."),
        ],
        "faqs": [
            ("Can I substitute a P30 grade for a P10?", "P30 grades are tougher but less wear-resistant than P10. Substituting P30 for P10 is acceptable for roughing operations where edge strength matters more than surface finish. For finishing, use the recommended grade or a finer-grained P10 equivalent."),
            ("How do coating colors correspond to application?", ("Coating colors are manufacturer-specific and not standardized. For example, Sandvik's black coating indicates a Inveio™ layer for steel turning, while Seco's gold coating often indicates a Duratomic® layer. Always check the ISO code and application guide rather than relying on color alone.")),
            ("What does the 'GC' prefix in Sandvik grades mean?", "GC stands for 'General Carbide' and indicates a cemented carbide substrate. The letter following (e.g., GC4415) is the grade designation where higher numbers generally indicate increased wear resistance. The specific formulation and coating are proprietary to Sandvik Coromant."),
        ],
    },
    "cast-iron-machining": {
        "h2s": [
            ("Gray Iron vs. Ductile Iron: Cutting Dynamics", "Gray iron (Class 30, Class 40) contains graphite flakes that create naturally broken chips, making it highly machinable at 600–1,200 SFM with carbide. Ductile iron (60-40-18, 80-55-06) has nodular graphite structure providing greater strength but requiring 20–30% lower cutting speeds. Both materials produce abrasive wear, making coated carbide essential for production runs."),
            ("Speed and Feed Optimization for Cast Iron Milling", "For face milling gray iron, use 500–800 SFM with feed rates of 0.006–0.012 in/tooth. Ductile iron requires reduced parameters: 350–600 SFM at 0.004–0.008 in/tooth. The abrasive graphite content wears tools primarily by abrasion, so CVD-coated grades with aluminum oxide layers significantly outperform uncoated or PVD-coated alternatives."),
            ("Managing the Graphite Dust Challenge", "Cast iron machining produces fine graphite dust that is highly abrasive and conductive. Use high-volume coolant with chip flushing to prevent dust accumulation. For dry machining operations, install a dedicated mist collection system. Graphite dust can accelerate ways and leadscrew wear, so machine covers and wipers should be inspected and replaced regularly."),
        ],
        "faqs": [
            ("Is cast iron difficult to machine?", "Gray iron is one of the easiest materials to machine due to its self-breaking chip formation. Ductile iron is more challenging due to higher strength and nodular graphite structure, but both are generally easier than low-carbon steel or stainless steel."),
            ("Should I use coolant when machining cast iron?", "Cast iron is typically machined dry to avoid thermal shock and to keep the graphite dust manageable. When coolant is used for high-production operations, ensure adequate flow and filtration to prevent graphite sludge buildup in the coolant system."),
            ("What causes built-up edge when machining cast iron?", "BUE can occur at low cutting speeds (below 300 SFM) where the chip welds to the tool edge. Increase speed to at least 400 SFM for gray iron or use a sharp, positive-rake geometry. Coated tools also reduce the adhesion tendency significantly."),
        ],
    },
    "coating-selector": {
        "h2s": [
            ("PVD Coatings: TiN, TiAlN, and AlTiN Comparison", "PVD (Physical Vapor Deposition) coatings are applied at lower temperatures (400–500°C) and maintain a sharp edge profile. TiN (gold) is a general-purpose coating for speeds up to 400 SFM. TiAlN (violet-gray) offers oxidation resistance to 800°C, ideal for dry machining. AlTiN (dark gray) with higher aluminum content provides superior hardness at elevated temperatures for high-speed applications exceeding 1,000 SFM."),
            ("CVD Coatings: Thick Layers for High-Wear Applications", "CVD (Chemical Vapor Deposition) coatings are applied at higher temperatures (1,000°C) and produce thicker, more wear-resistant layers. Multi-layer CVD coatings with aluminum oxide (Al₂O₃) are the standard for cast iron and steel turning at high speeds. The thicker coating provides excellent crater wear resistance but can cause edge rounding, making CVD unsuitable for sharp-edge applications like threading."),
            ("Matching Coating to Workpiece Material", "For aluminum and non-ferrous materials, uncoated or DLC (Diamond-Like Carbon) tools prevent built-up edge formation. For steels, TiAlN CVD coatings balance wear resistance and toughness. For cast iron, Al₂O₃-coated CVD grades excel. For superalloys, AlTiN PVD coatings with high hardness and oxidation resistance deliver the best tool life in high-temperature cutting."),
        ],
        "faqs": [
            ("Can I PVD coat an already-coated carbide insert?", ("No, coating over existing coating is not recommended. The adhesion layer requires a clean substrate surface. Any existing coating must be stripped before re-coating, which can damage the carbide substrate. Always apply coatings to fresh, uncoated carbide tools.")),
            ("How does coating thickness affect tool performance?", "Thicker coatings (8–15 μm for CVD) provide better crater wear resistance for continuous cutting but can cause edge rounding that increases cutting forces. Thinner coatings (1–4 μm for PVD) maintain sharper edges for finishing and threading. Select coating thickness based on your primary wear mode — crater wear or flank wear."),
            ("Is DLC coating worth the premium for machining aluminum?", "Yes, for high-production aluminum machining, DLC coatings reduce friction and prevent built-up edge, extending tool life by 2–5× over uncoated carbide. The reduced adhesion also improves surface finish consistency across long production runs."),
        ],
    },
    "coolant-concentration": {
        "h2s": [
            ("Using a Refractometer: Brix to % Concentration", "A refractometer measures the refractive index of coolant mixed with water, displayed as Brix on the scale. Most semi-synthetic coolants have a conversion factor where 1 Brix = 1% concentration. For soluble oils, the conversion factor is typically 1.5–2.0× the Brix reading. Always calibrate your refractometer with distilled water before each use for accurate readings."),
            ("Optimal Concentration Ranges by Coolant Type", "Synthetic coolants perform best at 3–5% concentration for general machining. Semi-synthetic coolants require 4–8% for steel and stainless applications. Soluble oils need 5–10% for heavy-duty operations. Running too low accelerates tool wear and promotes bacterial growth. Running too high reduces heat transfer and can cause skin irritation."),
            ("Troubleshooting Concentration Drift", "Concentration changes over time due to water evaporation, coolant drag-out, and tramp oil contamination. After a production shift, recheck concentration and top up with pre-mixed coolant rather than water to maintain stability. A drift of more than ±1% from target indicates a need for system maintenance or coolant replacement."),
        ],
        "faqs": [
            ("How often should I check coolant concentration?", "Check coolant concentration at least once per shift in high-production environments. For job shops with moderate usage, daily checks are sufficient. After adding water or coolant concentrate, always recheck and adjust to maintain the target concentration."),
            ("What causes poor refractometer readings?", "Tramp oil contamination, dirty prisms, and temperature variation are the most common causes. Clean the prism with a soft cloth and distilled water before each reading. If the coolant appears cloudy or has visible oil sheen, take a sample from below the surface for a more accurate measurement."),
            ("Does concentration affect tool life significantly?", "Yes. A 1% deviation from optimal concentration can reduce tool life by 15–25%. Below-optimal concentration reduces lubricity and cooling capacity, while above-optimal concentration reduces heat transfer. Maintaining tight control (±0.5% of target) consistently extends tool life."),
        ],
    },
    "countersink-depth-calculator": {
        "h2s": [
            ("Calculating Countersink Depth for Standard Screw Heads", "For 82° flat head screws (ANSI/ASME standards), the countersink depth should equal the screw head height plus 0.005–0.010 inches for clearance. The formula is: Depth = (Screw Head Diameter − Screw Body Diameter) / (2 × tan(Countersink Angle / 2)). For metric 90° flat head screws, the same approach with the appropriate angle ensures proper seating."),
            ("Counterbore Depth for Socket Head Cap Screws", "Socket head cap screws require a counterbore depth equal to the screw head height plus 0.010–0.020 inches clearance. The counterbore diameter must be 0.010–0.030 inches larger than the screw head diameter to allow tool access. Using the correct pilot diameter for the socket head screw size prevents binding and ensures proper clamp load."),
            ("Avoiding Common Countersink Depth Errors", "The most common mistake is cutting the countersink too deep, which reduces screw head engagement and weakens the joint. Always test on a sample piece before production. When using combination drills and countersinks, feed rate must be controlled to prevent chatter that creates oversized, irregular countersinks."),
        ],
        "faqs": [
            ("What is the standard countersink angle for flat head screws?", "The standard ANSI/ASME countersink angle is 82° for inch-series flat head screws. For metric screws, the standard is 90°. Always verify the screw standard before programming to ensure proper seating."),
            ("How do I measure countersink depth accurately?", "Use a countersink depth gage or a ball-bearing method: place a precision ball bearing of known diameter in the countersink and measure the height above the surface. The countersink depth can be calculated from the ball diameter and measured height."),
            ("Can I use a spot drill to create a countersink?", "Spot drills are designed for starting holes, not creating countersinks. Their included angle (90° or 120°) differs from standard countersink angles (82° or 90°). Use dedicated countersink tools or chamfer mills for proper geometry and consistent results."),
        ],
    },
    "die-steel-thermal-conductivity": {
        "h2s": [
            ("Thermal Conductivity of H13 Tool Steel at Various Temperatures", "H13 hot work tool steel exhibits thermal conductivity ranging from 24 W/m·K at room temperature to 28 W/m·K at 500°C. This increase with temperature is characteristic of tool steels and affects cooling rates in die-casting and hot forging applications. Understanding these values helps mold designers optimize cooling channel placement for uniform part cooling."),
            ("Comparing P20, D2, and S7 Thermal Properties", "P20 pre-hardened mold steel shows conductivity of 29 W/m·K at 24°C, making it the most thermally responsive of common mold steels. D2 tool steel, with its high chromium content, has lower conductivity at 20 W/m·K. S7 shock-resisting steel falls in between at 25 W/m·K. These differences significantly affect mold cycle times and cavity temperature uniformity."),
            ("How Conductivity Affects Mold Cooling Channel Design", "Higher thermal conductivity allows wider cooling channel spacing while maintaining uniform temperature distribution. For H13 molds, cooling channels should be spaced 2–2.5× the channel diameter from the cavity surface. For D2 molds with lower conductivity, reduce spacing to 1.5–2× diameter to achieve equivalent cooling performance."),
        ],
        "faqs": [
            ("Does thermal conductivity of tool steel change with use?", "Yes. Repeated thermal cycling can cause microstructural changes that gradually reduce thermal conductivity. Hot work steels like H13 may show 5–10% reduction in conductivity after extended service above 600°C due to carbide coarsening and tempering effects."),
            ("How does alloy content affect thermal conductivity?", "Higher alloy content generally reduces thermal conductivity. Chromium, vanadium, and molybdenum in tool steels scatter phonons and electrons, reducing heat transfer. D2 steel's 12% chromium content explains its lower conductivity compared to low-alloy P20."),
            ("Can I use thermal conductivity data to predict cooling time?", "Yes, with validated FEA models. The thermal diffusivity (conductivity divided by density × specific heat) is the key parameter for transient cooling analysis. Using handbook values with a 10% safety factor provides reliable mold cooling time estimates."),
        ],
    },
    "drill-point-length-calculator": {
        "h2s": [
            ("Standard Drill Point Angles and Their Applications", "The standard 118° drill point angle is suitable for most materials including steel, aluminum, and plastics. A 135° point angle, often with split point web thinning, is preferred for harder materials like stainless steel and titanium. The flatter angle reduces the cutting force at the center of the drill, preventing chipping and extending tool life in difficult-to-machine materials."),
            ("Calculating Drill Point Length for Accurate Depth Control", "Drill point length equals the distance from the drill tip to the full diameter, calculated as: Point Length = (Drill Diameter / 2) / tan(Point Angle / 2). For a 118° drill, this is approximately 0.3 × diameter. For a 135° drill, approximately 0.2 × diameter. Adding this to the required hole depth ensures proper through-hole or blind-hole depth."),
            ("Adjusting for Split Point and Special Geometries", "Split point drills have a self-centering feature that reduces the chisel edge length, effectively shortening the functional point length by 10–15%. When programming depths for split point drills, reduce the calculated point length by 15% for more accurate depth control. Helical point geometries used on CNC drills can reduce thrust requirements by up to 50%."),
        ],
        "faqs": [
            ("How much extra depth should I add for a through hole?", ("For through holes, add the full drill point length plus 0.5–1.0 mm to ensure the drill breaks through cleanly. This prevents a 'ring' from remaining at the breakthrough point. For thin materials (< 3× diameter), use a reduced point angle or a specialized flat-bottom drill.")),
            ("Does drill point angle affect hole straightness?", "Yes. A flatter point angle (135°) provides better self-centering and reduces walk on uneven surfaces. For deep holes exceeding 5× diameter, a 135° split point significantly improves hole straightness compared to a standard 118° point."),
            ("How do I measure drill point length accurately?", "Use a drill point gage or optical comparator for the most accurate measurement. For shop-floor measurement, the 'witness mark' method: drill into a flat plate, measure the depth to full diameter using a depth mic on the impression, and compare with your programmed depth."),
        ],
    },
    "form-tap-drill-calculator": {
        "h2s": [
            ("Form Tap Drill Size Fundamentals", "Form taps (roll taps) displace material rather than cutting it, requiring a larger tap drill than cutting taps. The general rule is 60–65% thread engagement for form taps in aluminum and brass, and 50–55% for steel. The drill diameter should produce a minor diameter equal to the tap's pitch diameter minus 0.001–0.002 inches for proper material flow."),
            ("Material Displacement Considerations for Roll Tapping", "Each material responds differently to cold forming. Aluminum 6061-T6 requires 65–70% thread engagement for full strength. Low-carbon steel (1018) needs 55–60% thread engagement. Stainless steel, due to work hardening, requires 50–55% and slower spindle speeds. Pre-drilling with a reamer finish improves thread quality for difficult materials."),
            ("Thread Forming in Through vs. Blind Holes", "Form tapping through holes is straightforward as chips are not a concern. For blind holes, form taps require less depth margin than cutting taps (2–3 pitches vs. 5 pitches for cutting taps) since no chip clearance is needed. However, the material displacement creates a raised 'burr' at the hole entrance that may require deburring for critical sealing surfaces."),
        ],
        "faqs": [
            ("Why does form tapping produce stronger threads than cutting?", ("Form tapping cold-works the material around the thread profile, creating work-hardened thread flanks that are 15–20% stronger in pull-out tests compared to cut threads. The grain structure follows the thread contour rather than being interrupted, resulting in improved fatigue resistance.")),
            ("Can form taps be used for all materials?", "Form taps work best in materials with 15–45% elongation: aluminum, brass, low-carbon steel, and some stainless grades. Brittle materials like cast iron, hardened steel (above 40 HRC), and most aluminum castings (A380) are not suitable for form tapping due to insufficient plasticity."),
            ("How does hole size tolerance affect form tap thread quality?", "Hole size is critical for form tapping. A 0.001-inch oversized hole reduces thread engagement by approximately 5%, while an undersized hole increases torque requirements dramatically and may cause tap breakage. Maintain hole diameter tolerance within ±0.001 inches for form tapping."),
        ],
    },
    "graphite-machining": {
        "h2s": [
            ("Graphite Machining Speeds and Feeds for EDM Electrodes", "Graphite EDM electrode machining requires high spindle speeds (10,000–25,000 RPM) with light chip loads due to the material's abrasive nature. Use CVD diamond-coated end mills at 300–500 SFM with chip loads of 0.001–0.003 in/tooth for finishing. Uncoated carbide can be used for roughing at reduced speeds, but tool wear will be significantly higher."),
            ("Managing Graphite Dust for Machine Protection", "Graphite dust is conductive and highly abrasive, making dust extraction critical. Use a dedicated vacuum system with HEPA filtration connected to the machine enclosure. Seal all machine ways and ball screws with positive-pressure covers. Without proper dust management, graphite particles can destroy machine spindle bearings and linear guides within months."),
            ("Part Geometry Strategies for Graphite Components", "Graphite is brittle and prone to edge chipping, especially on thin walls and sharp corners. Design radii of at least 0.020 inches at internal corners to prevent corner breakout. Use climb milling to reduce edge chipping on external profiles. For thin features below 0.040 inches, reduce feed rates by 50% and consider using a specialized graphite machining grade tool."),
        ],
        "faqs": [
            ("Is graphite machining better performed dry or with coolant?", "Graphite is always machined dry. Coolant soaks into the porous graphite structure, causing dimensional changes and potential outgassing in EDM applications. Dry machining with proper dust extraction is the established standard for graphite electrode manufacturing."),
            ("What tool material lasts longest for graphite?", "CVD diamond-coated carbide tools offer the longest tool life, typically 10–20× that of uncoated carbide. PCD-tipped tools are also excellent but limited to simple geometries. The diamond coating provides abrasion resistance against the hard graphite particles."),
            ("Can I use standard carbide end mills for graphite?", "Yes, but expect rapid wear. Uncoated micro-grain carbide end mills can work for short-run graphite machining (50–100 electrodes). For production runs exceeding 200 parts, diamond-coated tools are more economical due to reduced tool change downtime."),
        ],
    },
    "gun-drill-calculator": {
        "h2s": [
            ("Gun Drilling Parameters for Deep Hole Applications", "Gun drilling produces high-quality holes with depth-to-diameter ratios exceeding 100:1. Typical parameters for steel: cutting speed 80–150 SFM, feed rate 0.0002–0.0006 in/rev, with coolant pressure of 800–1,500 PSI. The single-lip gun drill geometry requires precise alignment — spindle-to-bushing concentricity within 0.001 inches TIR is essential for hole straightness."),
            ("Coolant Pressure and Flow Requirements", "High-pressure coolant is critical for gun drilling, providing chip evacuation, tool cooling, and lubrication at the cutting zone. For diameters under 0.250 inches, minimum 1,000 PSI at 2–5 GPM is required. Larger diameters (0.500–1.000 inches) need 500–800 PSI at 5–15 GPM. Insufficient coolant pressure is the leading cause of gun drill failure due to chip packing."),
            ("Troubleshooting Common Gun Drilling Defects", "Common quality issues include spiral marks (check bushing alignment), bell-mouth entrance (reduce feed at entry), and drill breakage (increase coolant pressure or reduce peck increment). Exit burns can be minimized by reducing feed rate during the last 0.100 inches of breakthrough. Regular inspection of the carbide tip — looking for micro-chipping — helps prevent catastrophic failure."),
        ],
        "faqs": [
            ("What materials can be gun drilled?", "Gun drilling is suitable for most machinable materials: carbon steel, alloy steel, stainless steel, cast iron, aluminum, titanium, and nickel alloys. Materials with high abrasiveness (hard-facing alloys) or extreme brittleness (ceramics) are not suitable for conventional gun drilling."),
            ("How do I choose between gun drilling and BTA drilling?", "Gun drilling is preferred for diameters under 1.0 inch and depths under 100 inches. BTA (Boring and Trepanning Association) drilling is more efficient for larger diameters above 1.0 inch. BTA also provides faster material removal rates at the cost of higher initial tooling investment."),
            ("What causes gun drill walk (hole straightness deviation)?", "Primary causes include: dull or chipped cutting edge, worn guide pads, misaligned bushing, inconsistent coolant flow, and incorrect feed-to-speed ratio. Check bushing alignment first; it accounts for 60% of straightness issues."),
        ],
    },
    "hardness-converter": {
        "h2s": [
            ("Understanding Hardness Scales: HRC, HRB, and HRA", "Rockwell hardness is the most common method for metallic materials. HRC (Rockwell C) uses a 150-kgf load with a diamond cone indenter for hardened steel (20–70 HRC). HRB (Rockwell B) uses a 100-kgf load with a 1/16-inch ball indenter for softer materials. HRA (Rockwell A) uses a 60-kgf load for thin materials and carbides. Each scale is non-linear and cannot be directly compared without conversion tables."),
            ("Converting Brinell Hardness to Rockwell C Scale", "The Brinell test (HB) uses a 10-mm carbide ball with a 3,000-kgf load. For steel, the approximate conversion is: HRC ≈ (HB − 30) / 2.5 within the range of 200–600 HB. Above 600 HB, the relationship becomes non-linear as the carbide ball begins to deform. ASTM E140 provides standardized conversion tables for accurate comparison between scales."),
            ("Vickers to Rockwell: When to Use Each Method", "Vickers (HV) microhardness testing uses a diamond pyramid indenter and is ideal for thin coatings, case-hardened layers, and small features where a macroscopic indent would destroy the part. The conversion to HRC is roughly HV / 10 + 10 for most steels, but this approximation loses accuracy above 60 HRC. For critical applications, always use the ASTM E140 standard conversion."),
        ],
        "faqs": [
            ("Why can't hardness values be converted with a simple formula?", "Hardness tests measure different indentation geometries and material responses. HRC measures a depth differential, HB measures a diameter, and HV measures a diagonal length. The relationships between these measurements change with material modulus, yield strength, and work-hardening behavior, making universal conversion formulas inaccurate."),
            ("What hardness conversion is most accurate for tool steels?", "For tool steels (A2, D2, H13, O1), the Rockwell C scale is the standard. Conversion to HB using ASTM E140 provides accuracy within ±15 HB for most tool steels. For critical specifications, use direct measurement on the required scale rather than conversion."),
            ("Can hardness predict tensile strength?", "Yes, with reasonable accuracy for carbon and alloy steels. A general rule of thumb: tensile strength (ksi) ≈ 500 × HRC for steels below 40 HRC. Above 40 HRC, the relationship becomes non-linear. ASTM A370 provides standardized tensile-strength-to-hardness correlations for carbon and alloy steels."),
        ],
    },
    "machinability-rating": {
        "h2s": [
            ("Understanding the AISI Machinability Index", "The AISI machinability index rates materials relative to AISI 1212 steel (rated 100%). Higher values indicate easier machining. Key reference points: 1212 = 100%, 1117 = 85%, 1018 = 70%, 4140 annealed = 60%, 316 stainless = 40%, and Inconel 718 = 15%. This index provides a starting point for speed and feed adjustments when switching materials."),
            ("How Machinability Affects Speed and Feed Selection", ("A material with 50% machinability requires approximately half the cutting speed of 1212 steel at 100%. The relationship is roughly: Recommended Speed = Baseline Speed × (Material Machinability / 100). Feed rates are typically reduced by the square root of the machinability ratio. For example, switching from 1018 (70%) to 316SS (40%) suggests a 43% speed reduction and a 24% feed reduction.")),
            ("Factors That Improve or Degrade Machinability", "Free-machining additives like sulfur (up to 0.35%), lead (up to 0.35%), and calcium improve machinability by modifying chip formation. Cold work reduces machinability by increasing hardness and strength. Heat treatment can dramatically change machinability: normalized 4140 machines better than annealed, but hardened 4140 above 40 HRC becomes significantly more difficult to machine."),
        ],
        "faqs": [
            ("What is the most machinable steel grade?", ("AISI 1212 and 1215 leaded free-machining steels are the most machinable, with ratings of 100% and 130% respectively. However, these grades are not suitable for weldments or high-stress applications. For structural use, 12L14 (160% rating) offers excellent machinability with moderate strength.")),
            ("Does machinability rating apply to milling and drilling?", "The AISI machinability rating is based on turning tests. For milling and drilling operations, the relative ratings provide a useful guideline but the actual speed adjustments may differ. Drilling typically requires larger speed reductions for difficult materials than turning."),
            ("How does material condition affect machinability?", "Material condition significantly impacts machinability. Annealed materials are generally most machinable. Cold-drawn materials are 10–20% harder and correspondingly less machinable. Heat-treated materials above 40 HRC can have 50% or less of the machinability of the annealed state."),
        ],
    },
    "metal-cost-calculator": {
        "h2s": [
            ("Calculating Material Cost Per Part from Stock", "The material cost per part depends on raw material price ($/kg or $/lb), stock utilization, and scrap value. For bar stock: Cost per Part = (Bar Length per Part × Bar Weight per Inch × $/kg) − Scrap Recovery. For plate work: add nesting efficiency (typically 60–85%) to the calculation. Tracking actual material usage against estimates identifies cost-saving opportunities."),
            ("Nesting Efficiency and Its Impact on Total Cost", "Nesting efficiency measures how much of the raw material ends up in the finished part. A 70% nesting efficiency means 30% is scrap. Improving nesting by just 5% through optimized CAM programming can reduce material costs by 7% overall. For high-volume parts, investing in dedicated nesting software pays for itself through material savings alone."),
            ("Material Price Volatility and Cost Estimation", "Metal prices fluctuate significantly due to market conditions. Aluminum prices can vary ±20% annually, while steel may vary ±30% or more. Include a 15% price buffer in quotes for metals with high volatility. Use monthly price indexes from sources like London Metal Exchange (LME) to adjust cost estimates. Consider purchasing agreements that lock in material pricing for firm quotes."),
        ],
        "faqs": [
            ("What is the average scrap recovery value for steel?", "Carbon steel scrap recovers approximately 10–15% of raw material cost as scrap value. Stainless steel and high-value alloys can recover 30–50% due to their inherent metal value. Account for scrap handling and processing costs (typically 2–5% of scrap value) in your net scrap recovery calculation."),
            ("How do I account for minimum order quantities in cost?", "Material distributors charge premiums for quantities below their minimum order threshold. If your part uses less than the minimum, distribute the surplus material cost across the ordered quantity. For small lot jobs, material costs can be 40–50% higher than large production runs on a per-part basis."),
            ("Does material certification add cost?", "Yes. Material test reports (MTRs) and certifications typically add 5–15% to raw material cost. For critical aerospace, medical, or defense applications, certification is mandatory. For commercial jobs, specify 'no cert required' to save on material costs if the end use allows."),
        ],
    },
    "metal-weight-calculator": {
        "h2s": [
            ("Tungsten Carbide Density vs. Steel: Weight Comparison", "Tungsten carbide has a density of 14.5–15.5 g/cm³, approximately 2× that of steel (7.85 g/cm³). This high density gives carbide tooling significant mass for vibration damping in machining. A carbide boring bar weighs twice as much as an equivalent steel bar, providing superior dynamic stability for deep-hole and precision boring operations."),
            ("Calculating Carbide Weight for Tooling Applications", "For carbide blanks and inserts, weight = volume × density. A standard CNMG432 carbide insert weighs approximately 9.5 grams. A 10-mm round carbide blank 50-mm long weighs approximately 57 grams. Understanding accurate weights helps calculate shipping costs and tool-balancing requirements for high-speed rotating toolholders."),
            ("Material Selection: Carbide vs. Steel vs. Ceramic", "While carbide is heavier, its stiffness (Young's modulus of 600–650 GPa vs. 200 GPa for steel) provides 3× the rigidity at the same cross-section. For machining centers, using carbide toolholders can reduce vibration amplitude by 40% compared to steel. The weight penalty is offset by the performance gain in finishing operations requiring tight tolerances."),
        ],
        "faqs": [
            ("How much does a typical carbide end mill weigh?", "A 12-mm carbide end mill with 75-mm flute length weighs approximately 85–95 grams. A 6-mm end mill of same length weighs about 22–28 grams. The exact weight depends on flute geometry, shank diameter, and overall length."),
            ("Does cobalt content affect carbide density?", "Yes. Higher cobalt content (binder) reduces density slightly. Grade K10 (6% cobalt) has density ~15.0 g/cm³, while K30 (12% cobalt) has density ~14.3 g/cm³. The cobalt substitution for tungsten carbide reduces overall weight by approximately 5% across the range of common grades."),
            ("How do I calculate shipping weight for carbide tool orders?", "Count the number of inserts and their individual weights (typically 5–15 grams each), add the weight of toolholders (0.2–2.0 kg each), and packaging weight (0.1–0.5 kg). For bulk orders, factor in a 5% overage for packing materials. Carbide is dense but compact — small orders often weigh surprisingly little."),
        ],
    },
    "metric-imperial-thread-converter": {
        "h2s": [
            ("Converting Metric Thread Pitches to TPI", "Metric threads are specified by pitch (mm per thread), while imperial (UN) threads are specified by threads per inch (TPI). The conversion: TPI = 25.4 / Pitch (mm). M10×1.5 has a pitch of 1.5 mm = 16.9 TPI, closest to 5/16-18 UNC. M12×1.75 = 14.5 TPI ≈ 1/2-13 UNC. For thread milling, converting between these systems correctly avoids costly tool-path errors."),
            ("Diameter Comparisons: Metric vs. Imperial Threads", "Metric thread diameters are specified as nominal OD in mm. Common conversions: M6 ≈ 1/4 inch (6.35 mm vs. 6.0 mm), M8 ≈ 5/16 inch (7.94 mm vs. 8.0 mm), M10 ≈ 3/8 inch (9.53 mm vs. 10.0 mm), M12 ≈ 1/2 inch (12.7 mm vs. 12.0 mm). While close, these are NOT interchangeable — always use the correct fastener system."),
            ("Practical Threading: When to Use Metric vs. Imperial", "Most modern CNC machines can cut both systems equally well. Use the system specified by your customer's drawings or the fastener standard in your supply chain. Converting existing imperial designs to metric can reduce tooling inventory, as metric drills and taps are more widely available globally. However, cost and lead time of specialty thread gages should be considered."),
        ],
        "faqs": [
            ("Can I substitute a metric fastener for an imperial one?", "Not recommended. The 0.3–0.7 mm diameter differences create insufficient thread engagement or interference, which can cause joint failure. Substituting M10 for 3/8-16 may strip threads under load. Always machine parts to the specified thread system."),
            ("How do I convert thread class (6H vs. 2B)?", "ISO 6H metric tolerance approximates to UN 2B class for medium-fit applications. 4H6H (metric) ≈ 3B (UN) for precision fits, and 7H (metric) ≈ 1B (UN) for loose fits. These are approximations — for critical joints, use the standard specified by the design authority."),
            ("Are metric and imperial drills compatible for threading?", "Metric tap drills (e.g., 8.5 mm for M10×1.5) don't have exact imperial equivalents. Use the closest available drill size if needed, but preferred practice is to use the specified tap drill for the thread system being cut. For example, use a 'Q' drill (0.332 inch) for 3/8-16 UNC, not an 8.3 mm metric drill."),
        ],
    },
    "npt-pipe-thread-calculator": {
        "h2s": [
            ("Understanding NPT Thread Taper and Geometry", "NPT (National Pipe Taper) threads have a 1:16 taper (0.75 inches per foot) measured on diameter. The thread angle is 60° with a truncated crest and root. The taper means that the pitch diameter at the gaging notch determines the thread's sealing capability. NPT threads seal through deformation of the threads themselves — the interference fit creates a pressure-tight joint when properly assembled with sealant."),
            ("Calculating NPT Thread Dimensions for Machining", "The key dimensions for programming NPT threads: thread depth = 0.8 × Pitch for the truncated profile, taper angle = 1.79° included (0.895° half-angle per side). For a 1/2 NPT thread: pitch = 14 TPI (0.0714 inches), thread depth = 0.0571 inches, and the thread extends approximately 0.54 inches for the hand-tight engagement plus 0.25 inches for wrench-tight."),
            ("NPT vs. NPS vs. BSPT: What's the Difference?", "NPT (National Pipe Taper) and BSPT (British Standard Pipe Taper) are NOT interchangeable despite similar appearances. NPT has a 60° thread angle, while BSPT has 55°. BSPT also uses a different pitch series. NPS (National Pipe Straight) has parallel threads that rely on a sealing washer rather than thread interference. Always verify the standard before cutting pipe threads."),
        ],
        "faqs": [
            ("How much thread sealant should I use on NPT fittings?", "Apply sealant (pipe dope or PTFE tape) to the male threads only, starting 1–2 threads from the end. Fill the thread roots but avoid excess sealant that could enter the pipe system. For PTFE tape, wrap 2–3 turns clockwise (when viewing the pipe end) with 50% overlap."),
            ("What is the acceptable thread length for NPT connections?", "The standard specifies hand-tight engagement (L1) and wrench-tight make-up (L3). For 1/2 NPT, L1 = 0.320 inches and L3 = 0.533 inches. Maximum thread length is L1 + L3. Exceeding this indicates the thread is cut too deep or the taper is incorrect."),
            ("Can I use NPT thread gages for inspection?", "Yes. Use L1 (hand-tight) ring gages for male threads and plug gages for female threads. The thread should enter the gage by hand and stop within ±1 turn of the gage notch. Use a 6-step L2 gage for final inspection to verify the thread is not cut too deep."),
        ],
    },
    "percentage-of-thread-calculator": {
        "h2s": [
            ("What Percentage of Thread Does Your Application Need?", "Thread engagement percentage determines the tap drill size. Standard recommendations: 65% for aluminum and brass, 75% for steel and stainless steel, 55% for hardened materials (above 40 HRC), and 60% for cast iron and bronze. Higher percentages provide marginally more thread strength but significantly increase tapping torque and the risk of tap breakage."),
            ("Calculating Tap Drill Size Based on Thread Percentage", "The formula for tap drill diameter: Drill Ø = Nominal Ø − (Thread % × Pitch) / 76.98 (for imperial threads) or Drill Ø = Nominal Ø − Thread % × Pitch × 0.013 (for metric). For M10×1.5 at 70% thread: Drill = 10 − (70 × 1.5 × 0.013) = 8.64 mm. For 3/8-16 UNC at 70%: Drill = 0.375 − (70 × 0.01299) / 76.98 = 0.332 inches (about a 'Q' drill)."),
            ("Trade-offs: Thread Strength vs. Tapping Difficulty", ("Increasing thread percentage from 60% to 80% only improves pull-out strength by about 10%, but tapping torque increases by 25–30%. Above 80% engagement, the strength gain is negligible while breakage risk rises sharply. For production tapping, target 65–70% for most materials. This provides 95% of maximum thread strength with significantly lower tool stress.")),
        ],
        "faqs": [
            ("What is the minimum thread engagement for structural bolts?", ("For structural steel connections, 100% thread engagement is standard per ASTM A325/A490. However, '100%' in this context means full thread depth in the nut, not 100% of the screw thread height. For tapped holes in machine components, 65–75% is adequate for 90% of applications per machinery handbook guidelines.")),
            ("Does thread percentage affect class of fit (6H vs 6g)?", "Thread percentage is determined by the tap drill size and affects the internal thread minor diameter, which is part of the 6H classification. The 6H tolerance band has upper and lower limits — a higher thread percentage uses the lower portion of the band. The pitch diameter (which determines fit quality) is determined by the tap's geometry, not the drill size."),
            ("Why do smaller threads need higher engagement percentage?", "Small diameters (< 1/4 inch or M6) have proportionally less thread flank area. Increasing the thread percentage to 75% for small fasteners compensates for the reduced load-bearing area. For larger threads (over 1/2 inch), 60% is usually sufficient for most applications."),
        ],
    },
    "plastic-machining": {
        "h2s": [
            ("Machining POM (Delrin): Speeds, Feeds, and Best Practices", "POM (acetal/Delrin) is one of the most machinable plastics, producing clean cuts with excellent dimensional stability. Use carbide tools at 500–1,000 SFM with feed rates of 0.003–0.008 in/rev for turning. Sharp tooling with positive rake (10–15°) prevents melting and produces optically clear surfaces. For thin-walled parts, reduce speeds to prevent heat buildup that causes dimensional expansion."),
            ("Nylon Machining: Managing Moisture and Heat", "Nylon (PA6, PA66) absorbs moisture from the air, which affects dimensional stability during machining. Pre-drying at 80°C for 2–4 hours is recommended for precision parts. Use coolant or air blast to manage heat — nylon has poor thermal conductivity and heat buildup can cause localized melting. Maintain sharp tools and climb mill to reduce frictional heating."),
            ("Machining PTFE (Teflon): Deformation Prevention", "PTFE's low coefficient of friction and high thermal expansion makes it challenging to hold tight tolerances. Use extremely sharp tools with high rake angles (15–20°). Light cuts (0.010–0.030 inches depth) with high feed rates minimize heat generation. The material's softness means clamping pressure must be carefully controlled to prevent deformation during machining."),
        ],
        "faqs": [
            ("Do plastics require coolant during machining?", "Generally, yes for production work. Coolant prevents heat buildup that causes melting, dimensional expansion, and poor surface finish. For prototype or short runs, air blast can suffice for materials like Delrin. Nylon and acrylic benefit significantly from flood coolant to prevent heat-related issues."),
            ("What is the best tool coating for plastic machining?", ("Uncoated polished carbide is generally preferred for plastic machining. The polished surface reduces friction and prevents material adhesion. DLC (Diamond-Like Carbon) coatings further reduce friction but add cost. Avoid TiAlN coatings for plastics — they increase friction and generate more heat.")),
            ("How do I prevent white lines or stress marks in machined acrylic?", "White lines occur from micro-cracking caused by tool exit stresses. Use sharp, polished tools with zero or slightly negative rake. Reduce feed rate on the final pass by 50%. Annealing the acrylic after machining at 80°C for 2 hours can relieve internal stresses and reduce visible stress marks."),
        ],
    },
    "reaming-allowance-calculator": {
        "h2s": [
            ("Recommended Reaming Allowances by Material", "Reaming allowance (stock removal) must balance between removing enough material to achieve roundness and surface finish, while not exceeding the reamer's capacity. For steel: 0.005–0.015 inches (0.13–0.38 mm) for diameters up to 1 inch. For aluminum: 0.008–0.020 inches. For cast iron: 0.004–0.012 inches. For stainless steel: 0.006–0.015 inches. Allowing too much stock causes chatter and oversize holes."),
            ("Pre-reaming Drill Size Selection for Optimal Finish", "The drilled hole should be 1–2% undersize of the nominal reamer diameter. For a 0.500-inch reamed hole, drill 0.490–0.495 inches. Undersize drilling reduces reamer cutting forces and improves hole geometry. For materials that work-harden (stainless, titanium), stay at the lower end of the allowance range to minimize work-hardened layer thickness."),
            ("Reamer Speed and Feed for Different Hole Sizes", "Reamer speeds should be 50–60% of drill speeds for the same material. Feed rates: 0.001–0.003 in/rev for diameters under 0.250 inches, 0.003–0.006 in/rev for 0.250–0.500 inches, and 0.005–0.010 in/rev for larger diameters. Using too high a speed causes rapid reamer wear and bell-mouthing of the hole entrance."),
        ],
        "faqs": [
            ("Can I ream a hole to correct location drift?", "Reaming will follow the existing hole centerline within the reamer's guidance capability. For location correction, the pre-hole must be within ±0.005 inches of target location. Reaming corrects size and finish, not position — use boring for location correction."),
            ("What causes a reamed hole to be bell-mouthed?", "Bell-mouthing (enlarged entrance) is typically caused by misalignment between the reamer and the pre-hole axis. Use a floating reamer holder to allow self-alignment. Other causes: excessive feed rate at entry, worn guide pads, or reamer overhang beyond 4× diameter."),
            ("How many passes should I use for reaming?", "A single reaming pass is standard for 90% of applications. Two passes (rough and finish) can improve surface finish by 15–25% but increase cycle time. For tight tolerances under ±0.0002 inches, consider a rough ream leaving 0.002–0.004 inches followed by a finish ream pass."),
        ],
    },
    "round-bar-weight": {
        "h2s": [
            ("Calculating Round Bar Weight Per Foot/Meter", "Standard formula: Weight (lbs/ft) = (D² × 0.222) for steel, where D is diameter in inches. For metric: Weight (kg/m) = (D² × 0.00617) for steel with D in mm. Example: 2-inch steel round bar weighs 2² × 0.222 = 0.888 lbs/ft. For 50-mm steel bar: 50² × 0.00617 = 15.43 kg/m. Account for the continuous casting tolerance (±0.5% on diameter) which affects actual weight by approximately ±1%."),
            ("Weight Differences Across Steel Grades", "Carbon steel: 7.85 g/cm³. Stainless 304/316: 7.93 g/cm³ (~1% heavier). Aluminum 6061: 2.70 g/cm³ (34% of steel weight). Brass: 8.53 g/cm³ (9% heavier than steel). Titanium: 4.43 g/cm³ (56% of steel weight). These density differences significantly impact shipping costs and structural design. A stainless component weighs 11% more than the same carbon steel component."),
            ("Estimating Bar Length from Weight", "When you know the total weight and bar size, you can estimate length: Length (ft) = Total Weight (lbs) / Weight per Foot. For plate and sheet: use thickness × width × length × density. This is valuable for inventory management — weighing a cut piece quickly confirms the remaining stock length without measuring it physically."),
        ],
        "faqs": [
            ("How accurate are calculated round bar weights?", "Theoretical weights assume nominal diameter and standard density. Actual mill tolerances introduce ±2–3% variation. For inventory valuation, theoretical weight is acceptable. For shipping or load calculation, use actual weigh scale reading."),
            ("Does hex bar use the same formula?", "No. Hex bar weight = (Width across flats² × 0.866 × 0.222) for steel, per foot. The 0.866 factor accounts for the hexagonal cross-section being 86.6% of the circumscribed circle area. Always use the specific hex formula rather than approximating as round bar."),
            ("How do I account for cut-off and saw kerf in length estimates?", "Subtract 0.125–0.250 inches per cut for saw kerf plus an additional 0.5–1.0 inch for end cleanup from the original bar length. For high-value materials like stainless or brass, marking and tracking cut-off drops can recover 2–5% of material cost."),
        ],
    },
    "stainless-properties": {
        "h2s": [
            ("304 Stainless Steel: Composition and Machinability", "Type 304 (18-8) stainless steel contains 18% chromium and 8% nickel, providing excellent corrosion resistance in food processing, chemical equipment, and architectural applications. Its machinability is rated at approximately 40% of AISI 1212 steel. Machining at 200–400 SFM with sharp, positive-rake carbide tools and generous coolant flow produces acceptable results. The material work-hardens rapidly, so consistent feed rates are essential."),
            ("316 Stainless Steel: Corrosion Resistance and Machining Differences", "Type 316 adds 2–3% molybdenum to the 304 base, dramatically improving pitting resistance in chloride environments (marine, pharmaceutical). The molybdenum content reduces machinability to approximately 35% of 1212 steel and requires 15–20% slower cutting speeds than 304. 316 also exhibits higher work-hardening rates — any hesitation during cutting creates a hardened layer that is difficult to penetrate on subsequent passes."),
            ("304 vs. 316: Application Selection Guide", "Choose 304 for general-purpose corrosion resistance in food, dairy, and interior architectural applications. Choose 316 when the component will be exposed to seawater, road salts, or chemical processing. The 40–60% cost premium of 316 is justified by its superior pitting resistance. For high-temperature applications (above 500°C), both grades lose corrosion resistance — consider 321 or 347 stabilized grades."),
        ],
        "faqs": [
            ("Is 304 or 316 easier to machine?", "304 is easier to machine due to lower work-hardening rate and lower cutting forces. 316's higher strength and molybdenum content reduce tool life by approximately 20% under identical machining parameters. Adjust speeds down by 15–20% when switching from 304 to 316."),
            ("Can stainless steel be heat treated for better machinability?", "Austenitic stainless (304, 316) cannot be heat treated for hardness changes. However, solution annealing at 1,040°C followed by rapid quenching can soften material that has been cold-worked. Avoid purchasing cold-drawn 304/316 bar for machining-intensive work."),
            ("What causes built-up edge when machining stainless steel?", "BUE is common in stainless due to its high ductility and work-hardening. Increase cutting speed to above 250 SFM for 304 and 200 SFM for 316. Use TiAlN-coated tools with polished flutes to reduce material adhesion. Maintain chip load above 0.003 in/tooth to ensure clean shearing."),
        ],
    },
    "step-drill-design-calculator": {
        "h2s": [
            ("Step Drill Geometry: Diameter and Length Specifications", "Step drills combine multiple diameters in a single tool, reducing tool changes and cycle times. Each step has three critical dimensions: diameter (D), step length (L), and transition radius (R). Standard practice: maintain a minimum 0.015-inch transition radius to reduce stress concentration and prevent step breakage. The overall flute length must accommodate the deepest step plus 20% clearance."),
            ("Step Spacing and Transition Angle Design", "The transition between steps should include a chamfer or radius rather than a sharp 90° corner. Recommended transition angle: 30–45° chamfer for stepped holes in steel, 15–30° for aluminum to reduce burr formation. For through-hole steps, the transition can be more aggressive. For blind hole steps, ensure the step length includes clearance for the pilot diameter's point length."),
            ("Tool Material Selection for Multi-Step Operations", "Step drills experience higher torsional loads than single-diameter drills due to the varying cutting action along the tool. For step drills, use micro-grain carbide grades (K20–K30) for toughness. For high-production step drilling in steel, TiAlN-coated carbide extends tool life 2–3× over uncoated. In aluminum, DLC-coated step drills prevent built-up edge on the step transitions."),
        ],
        "faqs": [
            ("Can I grind a standard drill into a step drill?", "Yes, on a universal tool and cutter grinder. Use a diamond wheel for carbide and avoid overheating during grinding. The step transitions must be concentric within 0.002 inches TIR. For critical step dimensions, use a CNC tool grinder for repeatable geometry."),
            ("What is the maximum number of steps for a single tool?", "Practical limit is 3–4 steps for manual tool grinding and 5–7 steps for CNC-ground tools. Beyond this, chip evacuation becomes ineffective, and the tool's cross-sectional rigidity is compromised. For holes requiring more than 4 steps, consider using a step reamer instead."),
            ("How do I prevent step drill chattering?", "Chatter at step transitions is caused by interrupted cut forces. Reduce feed rate by 30% during step transitions. Ensure the toolholder has minimal runout (under 0.0005 inches TIR). Use a stub-length step drill where possible — a shorter tool is exponentially more rigid."),
        ],
    },
    "superalloy-tool-life": {
        "h2s": [
            ("Estimating Tool Life in Inconel 718 Machining", "Inconel 718 is notorious for rapid tool wear due to its high-temperature strength, work-hardening rate, and carbide-forming tendencies. With carbide tooling at 80–120 SFM, expect tool life of 15–30 minutes cutting time before flank wear exceeds 0.012 inches. Using ceramic (SiAlON) tools at 300–500 SFM extends tool life to 45–60 minutes but requires rigid setups and negative rake geometries."),
            ("Hastelloy Machining: Speeds, Feeds, and Tool Selection", "Hastelloy C-276 presents similar challenges to Inconel with additional work-hardening due to its higher nickel content. Surface speeds of 60–100 SFM with carbide tools provide tool life of 10–20 minutes. TiAlN-coated carbide end mills with variable helix geometry reduce chatter and extend tool life by 25–40% compared to standard geometry. Climb milling is mandatory for surface finish and tool life."),
            ("Waspaloy and Rene 41: Advanced Alloy Machining", "Waspaloy and Rene 41 precipitation-hardenable superalloys require the most conservative parameters: 30–60 SFM with carbide and 200–350 SFM with ceramic. Tool life drops to 5–15 minutes even with optimal parameters. Use high-pressure coolant (1,000+ PSI) directed at the cutting zone to manage heat and extend tool life. Consider CBN (Cubic Boron Nitride) tooling for finishing operations where surface integrity is critical."),
        ],
        "faqs": [
            ("Why do superalloys wear tools so quickly?", "Superalloys maintain high strength at elevated cutting temperatures (800–1,000°C), causing abrasive wear and diffusion wear simultaneously. Additionally, the materials work-harden rapidly during cutting, creating a hardened layer that accelerates edge breakdown. The combination of thermal, abrasive, and chemical wear mechanisms destroys tool edges 5–10× faster than steel."),
            ("What tool material lasts longest in Inconel?", "For roughing: SiAlON ceramics provide the best tool life at high speeds. For finishing: CBN (BZN 6000 grade) offers the longest life but at higher cost. For general-purpose superalloy work, TiAlN-coated carbide with micro-grain substrate provides the best value-to-life ratio."),
            ("Does high-pressure coolant significantly improve tool life?", "Yes. Coolant at 1,000+ PSI directed precisely at the chip-tool interface can extend tool life by 50–150% by reducing cutting temperature and improving chip breakage. Through-spindle coolant is ideal. For machines without HPC, external coolant nozzles at 300+ PSI still provide meaningful improvement."),
        ],
    },
    "tap-drill-size-calculator": {
        "h2s": [
            ("Metric Tap Drill Sizes: M3 to M24 Chart", "Standard tap drill sizes for 70–75% thread engagement: M3×0.5 = 2.50 mm, M4×0.7 = 3.30 mm, M5×0.8 = 4.20 mm, M6×1.0 = 5.00 mm, M8×1.25 = 6.80 mm, M10×1.5 = 8.50 mm, M12×1.75 = 10.25 mm, M16×2.0 = 14.00 mm, M20×2.5 = 17.50 mm, M24×3.0 = 21.00 mm. For fine-pitch metric threads, add 0.2–0.3 mm to the drill diameter due to shallower thread depth."),
            ("Imperial Tap Drill Sizes: #0 to 1-1/2 Inch", "For UNC threads at 70–75% thread: #4-40 = 43 (0.089 in), #6-32 = 36 (0.106 in), #8-32 = 29 (0.136 in), #10-24 = 25 (0.149 in), 1/4-20 = 7 (0.201 in), 5/16-18 = F (0.257 in), 3/8-16 = Q (0.332 in), 1/2-13 = 27/64 (0.422 in), 3/4-10 = 21/32 (0.656 in), 1-8 = 7/8 (0.875 in). For fine threads (UNF), use the next larger fractional drill size."),
            ("Thread Engagement Percentage: Choosing the Right Drill", "The tap drill size determines thread engagement percentage. For general machining: use 70–75% thread. For hardened materials (above 40 HRC): 55–60%. For thin-wall applications: 50–55% to reduce expansion stress. For aluminum and brass: 65–70%. The formula for metric threads: Drill Ø = Nominal Ø − (0.013 × Thread % × Pitch). Use this formula when your specific thread size isn't in the standard chart."),
        ],
        "faqs": [
            ("What happens if I use the wrong tap drill size?", "An undersized drill increases tapping torque, causes oversized threads, and risks tap breakage. An oversized drill reduces thread engagement below the acceptable minimum, risking thread stripping under load. A ±0.1 mm error in tap drill for M10 changes thread engagement by approximately 5%."),
            ("Should I use a letter, number, or fractional drill for tapping?", "For inch-series threads, letter drills are specified for most sizes (e.g., 'Q' for 3/8-16). Number drills are specified for small sizes (e.g., #7 for 1/4-20). Fractional drills are used for larger diameters. Always check the Machinery's Handbook for the recommended drill size when converting between systems."),
            ("Why do some tap drill charts recommend different sizes?", "Different charts may target different thread engagement percentages. Commercial production charts often target 65% for ease of tapping, while military or aerospace charts target 75% for maximum strength. Always verify the target engagement before selecting a drill size from any chart."),
        ],
    },
    "tapping-feed-rate-calculator": {
        "h2s": [
            ("Calculating Tapping Feed Rate from RPM", "For rigid tapping, the feed rate is directly tied to spindle RPM: Feed (in/min) = RPM / TPI (Threads Per Inch). For metric threads: Feed (mm/min) = RPM × Pitch (mm). Example: 1/2-13 UNC at 400 RPM = 400 / 13 = 30.8 in/min. M10×1.5 at 400 RPM = 400 × 1.5 = 600 mm/min. The feed overrides must be set to 100% for rigid tapping — the control synchronizes Z-axis movement with spindle rotation."),
            ("Optimal Tapping Speeds by Material", "Recommended tapping speeds for high-speed steel (HSS) taps: aluminum: 500–1,000 RPM, brass: 400–700 RPM, low-carbon steel: 200–400 RPM, alloy steel (4140, 4340): 100–200 RPM, stainless steel (304): 50–100 RPM, titanium: 30–60 RPM. For carbide taps, multiply speeds by 2–3×. For thread mills, running at higher RPM with reduced chip loads is acceptable."),
            ("Peck Tapping vs. Single-Pass Tapping", "Peck tapping (incremental depth with retraction) is used for blind holes exceeding 1.5× diameter in materials with poor chip formation (stainless, aluminum). Each peck depth should be 2–3× the pitch. Single-pass tapping is suitable for through holes and blind holes in materials with good chip breaking (cast iron, brass). Peck tapping adds 20–40% to cycle time but significantly reduces tap breakage risk."),
        ],
        "faqs": [
            ("What is the difference between rigid tapping and synchronized tapping?", "Rigid tapping and synchronized tapping refer to the same process: the CNC control electronically synchronizes the spindle rotation and Z-axis feed. Compensating tapping uses a floating tap holder to account for minor synchronization errors. Rigid tapping requires CNC controls with this capability (standard on most machines since 2000)."),
            ("Can I tap without a floating holder in a CNC?", "Yes, if your control supports rigid tapping (G84.2 or M29 on Fanuc). For machines without rigid tapping capability, use a compression-type tap holder with axial float of 0.5–1.0 mm to prevent tap breakage from feed/speed mismatch."),
            ("How do I calculate safe tapping depth for thread mills?", "Thread milling feed rate depends on the tool's path, not spindle RPM. Use the formula: Feed (in/min) = RPM × Feed per Tooth × Number of Flutes. For a 3-flute thread mill at 2,000 RPM with 0.001 in/tooth: Feed = 2,000 × 0.001 × 3 = 6.0 in/min. The helical interpolation rate is calculated separately based on the thread pitch."),
        ],
    },
    "tensile-strength-converter": {
        "h2s": [
            ("PSI to MPa: Understanding the Conversion Factor", "1 PSI = 0.00689476 MPa. To convert PSI to MPa, divide by 145. To convert MPa to PSI, multiply by 145. For common reference: 30,000 PSI (typical low-carbon steel) = 207 MPa. 100,000 PSI (common alloy steel) = 690 MPa. 150,000 PSI (high-strength steel) = 1,034 MPa. 200,000 PSI (maraging steel) = 1,379 MPa. Understanding both units is essential for global engineering specifications."),
            ("Tensile Strength Ranges for Common Engineering Materials", "Aluminum 6061-T6: 42,000 PSI (290 MPa). 7075-T6: 83,000 PSI (572 MPa). Mild steel (A36): 58,000 PSI (400 MPa). 4140 quenched & tempered: 140,000 PSI (965 MPa). 316 stainless: 75,000 PSI (517 MPa). Titanium Ti-6Al-4V: 130,000 PSI (896 MPa). Inconel 718: 180,000 PSI (1,241 MPa). These benchmarks help engineers quickly assess relative material strength."),
            ("Yield Strength vs. Ultimate Tensile Strength", "Yield strength (YS) is the stress at which permanent deformation begins. Ultimate tensile strength (UTS) is the maximum stress before fracture. The YS/UTS ratio indicates the safety margin: low-carbon steel: 0.5–0.6 (excellent warning before failure). High-strength steel: 0.8–0.9 (limited plastic deformation before fracture). For design, always use yield strength; UTS is used for ultimate failure analysis."),
        ],
        "faqs": [
            ("What is the tensile strength of carbide cutting tool material?", "Tungsten carbide grades used for cutting tools have transverse rupture strength (TRS) of 350,000–450,000 PSI (2,400–3,100 MPa). Unlike steel, carbide has negligible ductility and fails suddenly under tensile load. This high compressive-to-tensile strength ratio is why carbide tools are designed for compression."),
            ("How does temperature affect tensile strength?", "Tensile strength decreases with increasing temperature. Steel at 400°C retains approximately 70% of room-temperature strength. Aluminum at 300°C retains about 20% of room-temperature strength. Superalloys like Inconel maintain 80–90% of strength at 600°C, which is why they're specified for high-temperature applications."),
            ("Does hardness predict tensile strength accurately?", "Yes, for carbon and alloy steels. A common approximation: UTS (ksi) ≈ 500 × HRC for steels between 20–40 HRC. Above 40 HRC, use 490 + (HRC − 40) × 300 as a better approximation. ASTM E140 provides the most accurate conversion tables for hardness to tensile strength across different material families."),
        ],
    },
    "thread-depth-torque-calculator": {
        "h2s": [
            ("Minimum Thread Engagement for Maximum Joint Strength", "Thread engagement length determines the load capacity of a threaded joint. General rule: internal thread engagement should be at least 1.0× the screw diameter for steel-on-steel, 1.5× for aluminum, 2.0× for cast iron, and 1.25× for stainless. For tapped holes in materials softer than the screw (e.g., steel screw in aluminum), increase engagement to 2.0× diameter."),
            ("Calculating Internal Thread Strip Strength", "Internal thread strip strength depends on shear area, which is calculated as: Shear Area = π × Pitch Diameter × Length of Engagement × Thread Shear Factor. For metric threads at 70% engagement, the shear factor is approximately 0.88. A 1/2-13 UNC thread in 6061 aluminum with 0.75 inches engagement provides approximately 4,800 lbs of thread strip strength."),
            ("Torque-to-Tension Relationships in Threaded Assemblies", "Applied torque relates to clamp load through: T = K × D × F, where K = nut factor (0.15–0.20 for lubricated, 0.20–0.30 for dry), D = nominal diameter, F = clamp load. Only 10–15% of applied torque generates clamp load; the rest overcomes friction under the head and in the threads. For critical joints, torque + angle control provides more accurate preload than torque-only methods."),
        ],
        "faqs": [
            ("What is the maximum thread engagement for strength?", ("Beyond 2.0× diameter of engagement, the screw will typically break before the internal threads strip. Extending engagement beyond 2.5× provides no meaningful strength increase but may be required for sealing (NPT) or adjustment purposes. Design for 1.5× diameter engagement as a practical maximum for most applications.")),
            ("How do thread lubricants affect torque-to-tension?", "Thread lubricants reduce the nut factor (K) from ~0.22 dry to ~0.12 with moly-based lubricants. For the same torque value, a lubricated joint generates approximately 80% more clamp load. Calibrate torque values specifically for lubricated or dry assembly conditions."),
            ("Does thread coating affect torque requirements?", "Yes. Zinc-plated threads have a K factor of approximately 0.19, while phosphate-coated threads are around 0.22. Cadmium-plated threads (now restricted) had a K factor of 0.15. Always use the K factor specific to your thread coating for accurate torque calculations."),
        ],
    },
    "thread-lead-angle-calculator": {
        "h2s": [
            ("Thread Lead Angle Formula and Its Significance", "The lead angle (helix angle) is calculated as: Lead Angle = arctan(Lead / (π × Pitch Diameter)). For a single-start M10×1.5 thread: Lead = 1.5 mm, Pitch Diameter ≈ 9.026 mm, Lead Angle = arctan(1.5 / (π × 9.026)) ≈ 3.03°. The lead angle affects thread milling tool path generation, tapping torque requirements, and the axial force component in threaded assemblies."),
            ("How Lead Angle Affects Thread Milling", "When thread milling, the tool's helical interpolation angle must match the thread's lead angle for correct thread form. A mismatch causes the tool flanks to rub rather than cut, producing ragged threads and accelerating tool wear. For large-diameter threads with steep lead angles (e.g., multi-start threads), thread mills with specialized edge geometry are recommended."),
            ("Lead Angle in Power Screws and Ball Screws", "In power transmission screws, the lead angle determines efficiency and self-locking behavior. Lead angles below 6° generally produce self-locking threads (friction holds the load without braking). Lead angles above 10° provide higher efficiency (80–90% for ball screws) but require braking mechanisms for vertical loads. The lead angle also affects the radial vs. axial load distribution on screw threads."),
        ],
        "faqs": [
            ("What is a typical lead angle for standard fasteners?", ("Standard UNC/UNF and metric threads have lead angles of 2–5° for single-start threads. A 1/4-20 UNC (pitch diameter ≈ 0.217 inches) has a lead angle of approximately 4.2°. Smaller diameter threads have larger lead angles — #4-40 UNC (pitch diameter ≈ 0.096 inches) has a lead angle of approximately 3.8°.")),
            ("How does lead angle affect thread gaging?", "Thread gages are designed for specific lead angles. Using a gage designed for a slow helix (small lead angle) on a fast helix thread can produce incorrect acceptance. Adjustable thread gages must be calibrated for the specific lead angle and pitch diameter of the thread being inspected."),
            ("Can lead angle cause thread loosening under vibration?", "Threads with lead angles above 5° are more susceptible to vibrational loosening because the helix angle creates a lateral force component that can rotate the nut. This is why fine-pitch threads (smaller lead angles) are preferred for high-vibration applications despite their lower strength."),
        ],
    },
    "thread-pitch-diameter-calculator": {
        "h2s": [
            ("The Three-Wire Method for Pitch Diameter Measurement", "The three-wire method is the most accurate way to measure thread pitch diameter. Three precision wires of calculated diameter are placed in the thread grooves, and the measurement over wires (M) is taken. The pitch diameter (E) is: E = M − (3 × Wire Diameter) + (Wire Diameter / (2 × sin(30°))) for 60° threads. The optimal wire size contacts the thread flanks at the pitch line for maximum accuracy."),
            ("Thread Wire Size Selection for Accurate Measurement", "The correct wire diameter contacts the thread flanks at the pitch diameter. Formula: Wire Diameter = Pitch / (2 × cos(30°)) for 60° threads. For imperial threads: Wire Diameter = 0.57735 × Pitch. For M10×1.5: Wire = 1.5 × 0.57735 = 0.866 mm. Using undersized wires requires compensation calculations. Using oversized wires compromises contact point accuracy."),
            ("Pitch Diameter Tolerances and Class of Fit", "Pitch diameter tolerance determines the class of fit (1A/2A/3A for external, 1B/2B/3B for internal). Class 2 provides 75% of the tolerance of Class 1. Class 3A/3B provides the tightest fit, typically used for aerospace and precision applications where zero slop is required. The pitch diameter tolerance for a Class 2A 1/2-13 UNC thread is approximately 0.0058 inches."),
        ],
        "faqs": [
            ("What is the difference between pitch diameter and major diameter?", "Major diameter is the largest diameter of the thread (crest for external threads). Pitch diameter is the diameter where the thread width and space width are equal. For thread fit and strength, pitch diameter is the critical dimension — it determines how the internal and external threads engage."),
            ("Can I use a thread micrometer instead of three wires?", "Yes, thread micrometers with specialized anvils that contact the thread flanks provide direct pitch diameter measurement. They're faster than three-wire but less accurate (±0.0005 inches vs. ±0.0002 inches for three-wire). Thread micrometers are adequate for shop-floor inspection, while three-wire is preferred for calibration and certification."),
            ("How do I measure pitch diameter on a thread mill?", "Threads produced by thread milling can be measured by the three-wire method. However, the cut thread will follow the tool path, so check at both ends and middle of the thread length. CMM with thread probes offers the most comprehensive inspection for thread-milled features."),
        ],
    },
    "titanium-machining-guide": {
        "h2s": [
            ("Ti-6Al-4V Machining Parameters: Speeds and Feeds", "Ti-6Al-4V (Grade 5) is the most common titanium alloy for aerospace and medical applications. Recommended parameters with carbide tooling: 80–150 SFM for roughing, 150–200 SFM for finishing. Chip load: 0.002–0.005 in/tooth for milling. Use climb milling exclusively to prevent work hardening. Feed rate should never drop below 0.001 in/rev — dwell or hesitation work-hardens the surface immediately."),
            ("Coolant Strategies for Titanium Machining", "Titanium has low thermal conductivity (7.5 W/m·K vs. 50 W/m·K for steel), causing most cutting heat to concentrate at the tool edge. Flood coolant is mandatory at 100+ PSI. High-pressure through-spindle coolant (800–1,500 PSI) extends tool life 3–5× by improving heat evacuation from the cutting zone. Never machine titanium dry — the heat causes immediate tool failure and risks titanium chip fires."),
            ("Tool Geometry Selection for Titanium Components", "Use sharp tools with positive rake (8–12°) and generous relief angles (8–12°) to reduce cutting forces and heat generation. Variable-helix end mills reduce chatter common in titanium machining. For deep pockets, use end mills with corner radius (0.030–0.060 inches) to prevent corner chipping. Avoid indexable tools where possible — solid carbide provides better edge strength for titanium."),
        ],
        "faqs": [
            ("Why is titanium so difficult to machine compared to steel?", "Titanium combines low thermal conductivity (heat stays at the cutting edge), low elastic modulus (springs away from the tool causing chatter), and chemical reactivity (welds to tool edges). The combination of these factors creates a uniquely challenging material that requires specific strategies not needed for steel machining."),
            ("Can I use conventional (non-climb) milling for titanium?", "Not recommended. Conventional milling work-hardens the surface and causes rapid tool edge breakdown. Always use climb milling for titanium. If the machine has excessive backlash, fix the mechanical issue before attempting titanium machining."),
            ("What is the best tool coating for titanium?", "AlTiN (Aluminum Titanium Nitride) coatings with high aluminum content (60–70%) provide the best performance in titanium due to their high oxidation temperature (900+°C) and low thermal conductivity. TiAlN coatings are also effective. Avoid TiN coatings — they perform poorly in titanium's high-temperature cutting zone."),
        ],
    },
    "tool-steel-heat-treat": {
        "h2s": [
            ("Dimensional Changes During Tool Steel Heat Treatment", "Tool steel undergoes volumetric dimensional changes during heat treatment due to phase transformations. Typical growth ranges: A2: +0.001 in/in, D2: +0.002 in/in, O1: +0.0015 in/in, S7: +0.0005 in/in. These predictable changes can be compensated for by machining oversized and then finishing after heat treatment to the final dimensions."),
            ("Pre-heat Treat Machining: Allowances and Strategies", "Leave 0.010–0.020 inches per surface for post-heat treat grinding for most tool steels. For A2 and D2, add 0.003 inches per inch for anticipated growth. For precision components, machine a test coupon of the same material and heat treat it with the production parts to verify actual dimensional change. EDM machining is best performed in the hardened state for maximum stability."),
            ("Stabilization Cycles for Minimizing Distortion", "Thermal stabilization cycles (sub-zero treatment + tempering) reduce retained austenite and stabilize dimensions. For A2 and D2, a cryogenic treatment at −75°C to −120°C after hardening, followed by double tempering, reduces dimensional drift during service. Precision gages and tooling benefit from triple tempering cycles to ensure absolute dimensional stability over years of use."),
        ],
        "faqs": [
            ("How much does tool steel shrink or grow during hardening?", "Most tool steels grow 0.0005–0.002 inches per inch during hardening due to the transformation of ferrite to martensite. High-speed steels (M2, M42) may shrink slightly. Always consult the steel manufacturer's data sheet for your specific grade, as growth varies with hardening temperature and section thickness."),
            ("Can I machine tool steel in the hardened state?", "Yes, using CBN or ceramic tooling for turned surfaces and EDM for complex geometries. Hard machining (45–68 HRC) is an established process for mold and die manufacture. Modern machines with sufficient rigidity can achieve surface finishes below 16 μin Ra on hardened tool steel."),
            ("Does stress relief annealing reduce distortion?", "Yes. Stress relief annealing at 600–700°C before rough machining reduces residual stresses from mill processing. Rough machine, then stress relieve again at 600°C before finish machining and heat treatment. This double stress relief cycle can reduce final distortion by 50–70%."),
        ],
    },
    "tube-weight-calculator": {
        "h2s": [
            ("Hollow Bar Weight Calculation: (OD² − ID²) Formula", "The weight of a tube/hollow bar is calculated as: Weight per unit length = (π/4) × (OD² − ID²) × Density. For steel: Weight (lbs/ft) = (OD² − ID²) × 2.672, where dimensions are in inches. For metric: Weight (kg/m) = (OD² − ID²) × 0.00617, where dimensions are in mm. A 3-inch OD × 2-inch ID steel tube weighs (9 − 4) × 2.672 = 13.36 lbs/ft."),
            ("Schedule Pipe Weights: Standard vs. Extra Strong vs. Double Extra Strong", "Pipe schedules define wall thickness for a given nominal pipe size (NPS). Schedule 40 (standard): 3-inch NPS has 0.216-inch wall × 8.63 lbs/ft. Schedule 80 (XS): 3-inch NPS has 0.300-inch wall × 11.68 lbs/ft. Schedule 160 (XXS): 3-inch NPS has 0.438-inch wall × 17.22 lbs/ft. Use the schedule table when working with standard pipe rather than calculating from nominal dimensions."),
            ("Material Density Differences in Tube Weight", "Carbon steel tube: 0.284 lbs/in³ (default factor). Stainless 304/316: 0.289 lbs/in³ (+1.8%). Aluminum 6061: 0.098 lbs/in³ (−65.5%). Brass: 0.307 lbs/in³ (+8.1%). When calculating tube weight for cost estimation, using the correct density factor is critical — a 50% error in density causes a 50% error in material cost. Always verify the material specification before calculating."),
        ],
        "faqs": [
            ("How do I account for tube wall thickness tolerance?", "ASTM specifications allow ±10% wall thickness variation. For conservative weight estimates, use nominal wall thickness. For maximum weight (shipping), use nominal wall + 10%. For minimum weight (structural design), use nominal wall − 10%. Request mill test reports for actual measured wall thickness on critical orders."),
            ("Does tube weight affect machining parameters?", "Yes. Heavy tubes require more support to prevent chatter during turning. As a rule of thumb, tubes with wall thickness below 1/8 of OD require steady rests or filler material during machining to prevent vibration. Light-gauge tubes (wall < 1/16 inch) are particularly challenging for thread cutting due to radial deflection."),
            ("How do I calculate remaining tube length from weight?", "Weigh the tube, subtract the weight of any attachments or end caps, and divide by the weight per foot for the specific OD and wall thickness. A 5-ft piece of 2-inch Schedule 40 steel pipe weighs approximately 5 × 3.65 = 18.25 lbs. If you have 12.4 lbs remaining: 12.4 / 3.65 = 3.4 feet remaining."),
        ],
    },
}

def fix_placeholder(title, desc, tool_name):
    """Fix PLACEHOLDER_TITLE and TOOL_TITLE in description and title"""
    friendly_name = tool_name.replace("-", " ").title()
    # Clean up specific title mappings
    title_map = {
        "brass-machining-parameters": "Brass Machining Parameters",
        "cast-iron-machining": "Cast Iron Machining",
        "graphite-machining": "Graphite Machining",
        "plastic-machining": "Plastic Machining",
        "tube-weight-calculator": "Tube Weight Calculator",
    }
    proper_name = title_map.get(tool_name, friendly_name)
    title = title.replace("PLACEHOLDER_TITLE", "and").replace("TOOL_TITLE", "")
    title = title.replace("  ", " ")
    desc = desc.replace("PLACEHOLDER_TITLE", "and").replace("TOOL_TITLE", "")
    desc = desc.replace("  ", " ")
    return title, desc


def generate_footer_section(content):
    """Generate the complete footer block"""
    h2s = content["h2s"]
    faqs = content["faqs"]

    seo_inner = ""
    for title, para in h2s:
        seo_inner += f'<h2>{title}</h2><p>{para}</p>\n'
    seo_inner += '<h2>Frequently Asked Questions</h2>\n'
    for q, a in faqs:
        seo_inner += f'<p><strong>{q}</strong> {a}</p>\n'
    seo_inner += '<p style="text-align:center;font-size:12px;color:#86868b;margin:14px 0">⚡ Calculated for Carbide-Tooling.com High-Performance Series. <a href="/products/end-mills.html" style="color:#0066cc;font-weight:600">View Catalog →</a></p>\n'

    toolbox_links = """
<a href="/tools/step-drill-design-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Step Drill Design Calculator</a><a href="/tools/engineering-interest-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Engineering Interest Calculator</a><a href="/tools/percentage-of-thread-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Percentage Of Thread Calculator</a><a href="/tools/production-efficiency-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Production Efficiency Calculator</a><a href="/tools/surface-roughness-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Surface Roughness Calculator</a><a href="/tools/countersink-depth-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Countersink Depth Calculator</a><a href="/tools/tapping-feed-rate-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Tapping Feed Rate Calculator</a><a href="/tools/coolant-lifecycle-cost/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Coolant Lifecycle Cost</a><a href="/tools/automation-vs-manual-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Automation Vs Manual Calculator</a><a href="/tools/heat-expansion-calculator/" style="font-size:12px;color:#1d1d1f;text-decoration:none;padding:6px 10px;background:#f5f5f7;border-radius:8px;transition:background .15s">Heat Expansion Calculator</a>"""

    footer_html = f"""
<footer><div class="container"><p style="margin-bottom:4px"><a href="/tools/" style="color:#0066cc">All Tools</a></p><p style="font-size:11px;margin-bottom:6px">Results are for reference only. Consult tool manufacturers for specific applications.</p><p style="font-size:11px">© 2026 Carbide Tooling</p></div><div style="padding:24px 0;margin:32px 0;border-top:1px solid #e8e8ed;border-bottom:1px solid #e8e8ed"><h3 style="font-size:14px;font-weight:700;margin-bottom:10px">🔧 Precision Engineering Toolbox</h3><div style="display:flex;flex-wrap:wrap;gap:6px">{toolbox_links}</div></div>
<section class="seo"><div class="container">
{seo_inner}
</div></section>
</footer>"""
    return footer_html


def insert_seo_section(filepath, tool_name):
    """Insert SEO content into a tool file"""
    content = SEED.get(tool_name)
    if not content:
        print(f"  SKIP: No seed content for {tool_name}")
        return False

    with open(filepath, "r") as f:
        html = f.read()

    h2s = content["h2s"]
    faqs = content["faqs"]

    # Generate SEO HTML
    seo_html = '\n<section class="seo"><div class="container">\n'
    for title, para in h2s:
        seo_html += f'<h2>{title}</h2><p>{para}</p>\n'
    seo_html += '<h2>Frequently Asked Questions</h2>\n'
    for q, a in faqs:
        seo_html += f'<p><strong>{q}</strong> {a}</p>\n'
    seo_html += '<p style="text-align:center;font-size:12px;color:#86868b;margin:14px 0">⚡ Calculated for Carbide-Tooling.com High-Performance Series. <a href="/products/end-mills.html" style="color:#0066cc;font-weight:600">View Catalog →</a></p>\n'
    seo_html += '</div></section>\n'

    # Check if already has SEO section
    if '<section class="seo">' in html:
        print(f"  Already has SEO section")
        return False

    count_footer = html.count("</footer>")

    if count_footer > 0:
        # Has footer: insert SEO before </footer>
        html = html.replace("</footer>", seo_html + "</footer>", 1)
        print(f"  DONE: Inserted SEO content into existing footer")
    else:
        # No footer: generate complete footer with SEO
        footer_block = generate_footer_section(content)
        html = html.replace("</body>", footer_block + "\n</body>", 1)
        print(f"  DONE: Added footer + SEO content")

    with open(filepath, "w") as f:
        f.write(html)

    return True


def main():
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    tools_missing_faq = []

    # Find tools without FAQ
    for d in sorted(os.listdir(tools_dir)):
        if d == "index.html":
            continue
        fpath = os.path.join(tools_dir, d, "index.html")
        if not os.path.isfile(fpath):
            continue
        with open(fpath) as f:
            content = f.read()
        if "Frequently Asked Questions" not in content:
            tools_missing_faq.append(d)

    print(f"Tools needing SEO: {len(tools_missing_faq)}")
    for t in tools_missing_faq:
        print(f"  {t}")

    # Fix placeholder issues
    print("\n--- Fixing placeholder issues ---")
    for t in tools_missing_faq:
        fpath = os.path.join(tools_dir, t, "index.html")
        with open(fpath) as f:
            html = f.read()
        orig = html
        # Fix title
        match = re.search(r'<title>(.*?)</title>', html)
        if match and ("PLACEHOLDER_TITLE" in match.group(1) or "TOOL_TITLE" in match.group(1)):
            new_title, _ = fix_placeholder(match.group(1), "", t)
            html = html.replace(match.group(0), f'<title>{new_title}</title>')
            print(f"  {t}: Fixed title")
        # Fix meta description
        match = re.search(r'<meta name="description" content="([^"]*)"', html)
        if match and ("PLACEHOLDER_TITLE" in match.group(1) or "TOOL_TITLE" in match.group(1)):
            _, new_desc = fix_placeholder("", match.group(1), t)
            html = html.replace(match.group(0), f'<meta name="description" content="{new_desc}"')
            print(f"  {t}: Fixed description")
        # Fix H1
        match = re.search(r'<h1[^>]*>.*?TOOL_TITLE.*?</h1>', html)
        if match:
            friendly = t.replace("-", " ").title()
            html = html.replace(match.group(0), match.group(0).replace("TOOL_TITLE", friendly))
            print(f"  {t}: Fixed h1")
        if html != orig:
            with open(fpath, "w") as f:
                f.write(html)

    # Insert SEO content
    print("\n--- Inserting SEO content ---")
    success = 0
    for t in tools_missing_faq:
        fpath = os.path.join(tools_dir, t, "index.html")
        print(f"Processing {t}...")
        if insert_seo_section(fpath, t):
            success += 1

    print(f"\nTotal: {success}/{len(tools_missing_faq)} tools enhanced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
