# Evaluation results

- Agent model: `gpt-6-luna`
- Judge model: `gpt-6-luna`
- Questions scored: 25 of 25
- Generated: 2026-10-20

| Slice | n | Citations exist | Citations grounded | Citations supported (judge) | Key paper retrieved | Required facts | Fully correct (judge) | Mean accuracy (0-1) |
|---|---|---|---|---|---|---|---|---|
| all | 25 | 100% (25/25) | 100% (25/25) | 88% (22/25) | 75% (12/16) | 86% | 76% (19/25) | 0.82 |
| literature | 16 | 100% (24/24) | 100% (24/24) | 88% (21/24) | 75% (12/16) | 81% | 62% (10/16) | 0.72 |
| model | 3 | n/a | n/a | n/a | n/a | 100% | 100% (3/3) | 1.00 |
| negative | 2 | n/a | n/a | n/a | n/a | 100% | 100% (2/2) | 1.00 |
| taxonomy | 4 | 100% (1/1) | 100% (1/1) | 100% (1/1) | n/a | 92% | 100% (4/4) | 1.00 |

## Per question

| id | cited | exist | grounded | supported | key paper | facts | accuracy | judge reason |
|---|---|---|---|---|---|---|---|---|
| lit01 | 2 | 2 | 2 | 0/2 | yes | 100% | 2 | Correctly identifies the DGRP as a sequenced inbred-line resource from one Raleigh natural population, used to study genetic variation and traits, and notes its 205 lines. |
| lit02 | 2 | 2 | 2 | 2/2 | yes | 100% | 2 | Correctly states that about half of DGRP lines are infected and infection effects on quantitative traits are rarely significant. |
| lit03 | 0 | 0 | 0 |  | no | 0% | 0 | The answer does not provide the requested counts, which are available in the reference. |
| lit04 | 1 | 1 | 1 | 1/1 | no | 100% | 0 | Does not answer the general finding: both lipid and carbohydrate stores correlate with resistance, and their combined energy content explains it best; it overgeneralizes from one study. |
| lit05 | 1 | 1 | 1 | 1/1 | yes | 50% | 2 | Correctly identifies bmm as the ATGL homolog and states that loss causes excess fat accumulation; added details do not conflict with the reference. |
| lit06 | 1 | 1 | 1 | 1/1 | yes | 50% | 1 | Correctly reports increased starvation survival, but omits the key loss of starvation-induced hyperactivity; the precise 50% claim is not in the reference. |
| lit07 | 3 | 3 | 3 | 3/3 | no | 50% | 1 | Identifies increased energy storage, but omits energy conservation and starvation tolerance as distinct routes; its cited studies do not cover the reference’s key selected-line findings. |
| lit08 | 1 | 1 | 1 | 1/1 | yes | 100% | 2 | Gives the reference estimate and correctly states prediction was modest and BayesB was no better; added details are consistent. |
| lit09 | 4 | 4 | 4 | 4/4 | yes | 100% | 2 | Correctly reports the lab-colony age-structure result and 82.6% species accuracy from the reference; extra details do not contradict it. |
| lit10 | 2 | 2 | 2 | 2/2 | no | 50% | 0 | It does not give the reference’s key finding or remedy: poor cross-population transfer and improvement using PCA/t-SNE with transfer learning; it discusses different studies instead. |
| lit11 | 1 | 1 | 1 | 1/1 | yes | 100% | 2 | Accurately reports the species and age identification rates, including the distinction between field-collected and lab-reared mosquitoes. |
| lit12 | 1 | 1 | 1 | 1/1 | yes | 100% | 2 | Correctly lists all six indices, both diets, significant genetic variation, and correlations with starvation resistance, oxidative stress, and ER stress. |
| lit13 | 2 | 2 | 2 | 2/2 | yes | 100% | 2 | Correctly says resistance was not linked to total hydrocarbon amount, but to a higher proportion of desaturated hydrocarbons. |
| lit14 | 1 | 1 | 1 | 0/1 | yes | 100% | 1 | Correctly defines micro-environmental plasticity and reports substantial DGRP genetic variation and heritabilities, but omits the reference’s candidate-gene finding, Hsp90. |
| lit15 | 1 | 1 | 1 | 1/1 | yes | 100% | 2 | Correctly reports no replication in either direction and notes that many Flyland-associated SNPs participated in DGRP epistatic interactions. |
| lit16 | 1 | 1 | 1 | 1/1 | yes | 100% | 2 | Accurately captures the survival-mode trade-offs, associated stress resistance and life-history traits, and the poorly understood ecological significance. |
| tax01 | 0 | 0 | 0 |  |  | 100% | 2 | Correctly gives TaxID 7227 and subgenus Sophophora. |
| tax02 | 1 | 1 | 1 | 1/1 |  | 67% | 2 | Correctly identifies both as members of the melanogaster subgroup and gives the accurate NCBI taxids 7240 and 7227. |
| tax03 | 0 | 0 | 0 |  |  | 100% | 2 | Correctly gives TaxID 7173, family Culicidae, and the Anopheles gambiae species complex. |
| tax04 | 0 | 0 | 0 |  |  | 100% | 2 | Flags the ambiguity and correctly gives taxid 7227 for the usual model organism, Drosophila melanogaster. |
| mod01 | 0 | 0 | 0 |  |  | 100% | 2 | Correctly predicts about 4.82, identifies the positive triglyceride ester C=O band near 1740–1760 cm⁻¹ as the main driver, and notes model limitations. |
| mod02 | 0 | 0 | 0 |  |  | 100% | 2 | Gives the three matching predictions and appropriately cautions that within-line single-fly variation is substantial, training used line means, and cross-lab transfer failed. |
| mod03 | 0 | 0 | 0 |  |  | 100% | 2 | Correctly identifies most_resistant as more resistant and gives predictions and difference matching the reference. |
| neg01 | 0 | 0 | 0 |  |  |  | 2 | The answer correctly says it could not verify a relevant study and does not invent a paper or findings. |
| neg02 | 0 | 0 | 0 |  |  | 100% | 2 | Correctly declines to predict human BMI and explains that the model predicts Drosophila starvation resistance, not human BMI. |
