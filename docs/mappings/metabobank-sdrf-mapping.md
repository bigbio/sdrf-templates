# MetaboBank ↔ SDRF Metabolomics Column Mapping

This document maps every column from the MetaboBank LC-MS and GC-MS Excel metadata templates to its equivalent column in the SDRF metabolomics templates (`ms-metabolomics`, `lc-ms-metabolomics`, `gc-ms-metabolomics`).

The mapping target is **lossless** for all columns that carry experimental data. ISA-graph intermediate node columns (`Sample Name`, `Extract Name`, `Labeled Extract Name`, `Protocol REF`) collapse into row identity and `comment[...]` payload — they do not survive as columns in the SDRF flat row model. `Unit` columns are dropped because SDRF embeds units inline in the value cell (e.g. `30 NCE`, `0.4 mL/min`).

MetaboBank source: <https://www.ddbj.nig.ac.jp/metabobank/metadata-e.html> (LC-MS and GC-MS Excel templates).

## Conventions

- MetaboBank uses MAGE-TAB style: capitalised column names, `Comment[...]` brackets, and an ISA-Tab graph of named nodes (`Source Name`, `Sample Name`, `Extract Name`, `Labeled Extract Name`, `Assay Name`).
- SDRF metabolomics uses lower-case names, `comment[...]` / `characteristics[...]` brackets, and a flat row model where each row is one `(source name × acquisition)` tuple.
- A column listed as **dropped** has no SDRF-side counterpart because the information either:
  - is conveyed by row identity (graph-node columns), or
  - is denormalised into the value cell itself (`Unit`), or
  - belongs to project-level / IDF metadata, not the per-row SDRF.

## Identifier and graph nodes

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Source Name` | `source name` | Identical, lowercased. Unique per biological sample. |
| `Sample Name` | (collapsed into `source name`) | Flat row model; no separate Sample node. |
| `Extract Name` | (collapsed into row + `comment[extraction method]`) | Extract identity is the row; the protocol that produced it is the `comment[extraction method]` payload. |
| `Labeled Extract Name` | (collapsed into row) | If isotopic labels are used, encode in `comment[label]` (proteomics-style); otherwise drop. |
| `Assay Name` | `assay name` | Identical, lowercased. Unique per acquisition run. |
| `Protocol REF` | (dropped) | SDRF describes protocols inline as `comment[*]` columns rather than as graph-edge references. |

## Sample characteristics

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Characteristics[Organism]` | `characteristics[organism]` | Identical, lowercased. NCBI Taxonomy. |
| `Characteristics[Organism part]` | `characteristics[organism part]` | UBERON / BTO. |
| `Characteristics[Sex]` | `characteristics[sex]` | PATO / EFO. |
| `Characteristics[Disease]` | `characteristics[disease]` | DOID / MONDO. |
| `Characteristics[Cell type]` | `characteristics[cell type]` | CL. |
| `Characteristics[Sample type]` | `characteristics[sample matrix]` (close fit) | If the value is a tissue or biofluid, map to `sample matrix`; otherwise consider `characteristics[analyte class]` or drop with a note. |
| `Characteristics[Material type]` | `characteristics[sample matrix]` (close fit) | Same as above. |
| `Characteristics[Biological replicate]` | `characteristics[biological replicate]` | Integer starting from 1. |

## Acquisition (LC-MS and GC-MS shared)

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Instrument]` | `comment[instrument]` | PSI-MS ontology. |
| `Comment[Ion source]` / `Comment[Ionization]` | `comment[ion source]` | PSI-MS MS:1000008 child. |
| `Comment[MS polarity]` / `Polarity` / `Comment[Scan polarity]` | `comment[scan polarity]` | Values: `positive scan`, `negative scan`, `polarity switching`. See polarity rule below. |
| `Comment[Mass analyzer]` | `comment[ms2 mass analyzer]` | Lowercased; PSI-MS ontology. |
| `Comment[Acquisition method]` | `comment[acquisition method]` | DDA / DIA / SIM / MRM / full scan. |
| `Comment[Mass range]` | `comment[ms1 scan range]` | If MS1 only; otherwise split into `comment[ms2 scan range]`. |
| `Comment[Resolution]` | (no direct equivalent — drop or extend) | Optional per-row resolution field could be added in a future template iteration. |
| `Comment[Collision energy]` | `comment[collision energy]` | Format: `30 NCE` or `25 eV`. |

## Files

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Raw Data File]` | `comment[data file]` (inherited from `base`) | Renamed for proteomics-SDRF consistency. |
| `Comment[Raw Data File md5]` | `comment[raw data file md5]` | Verbatim, lowercased. 32-character hex. |
| `Comment[Processed Data File]` | `comment[processed data file]` | Verbatim, lowercased. |
| `Comment[Processed Data File md5]` | `comment[processed data file md5]` | Verbatim, lowercased. |
| `Comment[Metabolite Assignment File]` | `comment[metabolite assignment file]` | Verbatim, lowercased. Per-assay constant. |
| `Comment[Metabolite Assignment File md5]` | `comment[metabolite assignment file md5]` | Verbatim, lowercased. |
| `Comment[Acquisition Parameter Data File]` | (no direct equivalent — drop or use `comment[data file]`) | Vendor parameter exports are usually bundled with the raw file in MS-based metabolomics; consider extending in a future iteration if needed. |
| `Image Data File` | (out of scope — MSI not yet templated) | Will be addressed by a future `msi-metabolomics` template. |
| `Free Induction Decay Data File` | (out of scope — NMR not yet templated) | Will be addressed by a future `nmr-metabolomics` template. |

## Sample preparation

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Extraction method]` | `comment[extraction method]` | Free-text; CHMO-style ontology term recommended. |
| `Comment[Extraction solvent]` | `comment[extraction solvent]` | ChEBI when possible. |
| `Comment[Internal standard]` | `comment[internal standard]` | ChEBI when possible. Multiple cardinality. |
| `Comment[Analyte class]` / `Comment[Polarity of analytes]` | `characteristics[analyte class]` | Values: `polar metabolites`, `lipids`, etc. |

## LC-MS specific

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Chromatography type]` | `comment[chromatography type]` | CHMO ontology (e.g. `NT=reversed-phase chromatography;AC=CHMO:0002302`). |
| `Comment[Chromatography column]` / `Comment[LC column]` | `comment[chromatography column]` | Free-text manufacturer / model. |
| `Comment[Mobile phase A]` | `comment[mobile phase a]` | Lowercased. |
| `Comment[Mobile phase B]` | `comment[mobile phase b]` | Lowercased. |
| `Comment[Gradient]` | `comment[gradient]` | Free-text. |
| `Comment[Flow rate]` | `comment[flow rate]` | `nL/min` / `µL/min` / `mL/min`. Unit embedded in cell. |

## GC-MS specific

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Derivatization]` | `comment[derivatization]` | Free-text protocol (e.g. `MSTFA`, `MOX + MSTFA`). Required for `gc-ms-metabolomics`. |
| `Comment[Derivatization agent]` | `comment[derivatization agent]` | ChEBI when possible. Multiple cardinality. |
| `Comment[GC column]` | `comment[gc column]` | Free-text. |
| `Comment[Carrier gas]` | `comment[carrier gas]` | `helium` / `hydrogen` / `nitrogen`. |
| `Comment[Oven program]` / `Comment[GC oven program]` | `comment[oven program]` | Free-text. |

## QC / batch

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Comment[Sample preparation batch]` / `Comment[Batch]` | `comment[sample preparation batch]` | Free-text identifier. |
| `Comment[LC batch]` / `Comment[Acquisition batch]` | `comment[lc batch]` | Free-text identifier. |
| `Comment[Acquisition date]` / `Comment[Acquisition Date]` | `comment[acquisition date]` | ISO-8601 recommended. |
| `Comment[Technical replicate]` | `comment[technical replicate]` (inherited from `base`) | Integer starting from 1. |

## Factor values

| MetaboBank | SDRF metabolomics | Notes |
|---|---|---|
| `Factor Value[X]` | `factor value[x]` | Lowercased. |
| `Unit` | (dropped) | SDRF embeds units in the value cell (e.g. `0.4 mL/min`, `30 NCE`). |

## Polarity-switching annotation rule

When a sample is acquired in **both** positive and negative ion modes producing two distinct raw files, the SDRF uses **two rows per sample** — one row per `(source name × scan polarity)` combination, each with its own `comment[data file]`. The `polarity switching` value of `comment[scan polarity]` is reserved for true in-method polarity switching that produces a single combined file.

If a MetaboBank xlsx encodes split-polarity acquisitions as two rows (one per file), the conversion is direct. If a single row carries multiple raw files (e.g. comma-separated), the converter should expand it into one row per file.

## Round-tripping

A future converter (out of scope for the initial template release) can take a MetaboBank LC-MS or GC-MS xlsx and emit a valid `lc-ms-metabolomics` or `gc-ms-metabolomics` SDRF using the mappings above. The reverse direction (SDRF → MetaboBank xlsx) requires materialising the ISA graph nodes (`Sample Name`, `Extract Name`) by deduplicating on `source name` and `comment[extraction method]`, and adding `Protocol REF` columns whose values are protocol identifiers from the IDF half of the MetaboBank submission.

## Out of scope (future iterations)

- NMR, CE-MS, DI-MS, FIA-MS, MALDI-MS, MSI templates and their MetaboBank columns.
- A bidirectional MetaboBank xlsx ↔ SDRF converter script.
- Strict CHMO ontology validation (the current `comment[chromatography type]` validator is a pattern check; full ontology hook is a follow-up).
