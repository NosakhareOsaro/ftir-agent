# Judge audit: citation support

Judge: `gpt-6-luna` (OpenAI), **judge v1** (the archived `*.judge-v1.json` verdicts; see README for v2 and v3). **Second reviewer:** a second LLM, from a different model family than the judge, reviewed every verdict. This is a cross-model check, **not** a human audit.

Rule for grouped citations (`[PMID:a] [PMID:b]`): each paper must support part of the sentence, and together they must support all of it.

**Result: second reviewer agrees on 21/25 (84%).** Judge too strict on 3 (#1, #12, #15), too lenient on 1 (#6). With the second reviewer's verdicts, support is 23/25 (92%).

**Human spot-check (10 verdicts: the 4 disagreements plus #3, #7, #11, #13, #20, #22):** sided with the second reviewer on all 4 disagreements, and agreed with both on the other 6. Human agreement with the judge: 6/10; with the second reviewer: 10/10. Unchecked items keep `?`.

## 1. lit01, PMID 22318601

**Claim:** The **Drosophila melanogaster Genetic Reference Panel (DGRP)** is a community resource of **205 inbred fly lines**, each with a whole-genome sequence, used to study natural genetic variation and its relationship to traits. The lines were derived from **a single wild population collected in Raleigh, North Carolina**, then inbred to create strains that can be compared across studies. [PMID:22318601] [PMID:28834395] / In other words, the panel represents genetic variation sampled from one natural population—not a set of lines produced by crossing different laboratory strains. The 2012 abstract describes the lines as “fully sequenced inbred lines derived from a natural population”; the review specifies the population’s location and the panel’s size. [PMID:22318601] [PMID:28834395]

**Abstract:** *The Drosophila melanogaster Genetic Reference Panel.* A major challenge of biology is understanding the relationship between molecular genetic variation and variation in quantitative traits, including fitness. This relationship determines our ability to predict phenotypes from genotypes and to understand how evolutionary forces shape variation within and between species. Previous efforts to dissect the genotype-phenotype map were based on incomplete genotypic information. Here, we describe the Drosophila melanogaster Genetic Reference Panel (DGRP), a community resource for analysis of population genomics and quantitative traits. The DGRP consists of fully sequenced inbred lines derived from a natural population. Population genomic analyses reveal reduced polymorphism in centromeric autosomal regions and the X chromosome, evidence for positive and negative selection, and rapid evolution of the X chromosome. Many variants in novel genes, most at low frequency, are associated with quantitative traits and explain a large fraction of the phenotypic variance. The DGRP facilitates genotype-phenotype mapping using the power of Drosophila genetics.

**Judge:** PARTIAL: Supports a community resource of fully sequenced inbred lines from a natural population, but not 205 lines or Raleigh location.

**Second reviewer (second LLM):** disagree. SUPPORTED. Grouped citation: this paper supports 'sequenced inbred lines from a natural population'; the co-cited review supplies 205 lines and Raleigh, and the answer says so explicitly.

**Human:** SUPPORTED: sides with the second reviewer. Grouped citation; the co-cited review supplies 205 lines and Raleigh.

---

## 2. lit01, PMID 28834395

**Claim:** The **Drosophila melanogaster Genetic Reference Panel (DGRP)** is a community resource of **205 inbred fly lines**, each with a whole-genome sequence, used to study natural genetic variation and its relationship to traits. The lines were derived from **a single wild population collected in Raleigh, North Carolina**, then inbred to create strains that can be compared across studies. [PMID:22318601] [PMID:28834395] / In other words, the panel represents genetic variation sampled from one natural population—not a set of lines produced by crossing different laboratory strains. The 2012 abstract describes the lines as “fully sequenced inbred lines derived from a natural population”; the review specifies the population’s location and the panel’s size. [PMID:22318601] [PMID:28834395]

**Abstract:** *Charting the genotype-phenotype map: lessons from the Drosophila melanogaster Genetic Reference Panel.* Understanding the genetic architecture (causal molecular variants, their effects, and frequencies) of quantitative traits is important for precision agriculture and medicine and predicting adaptive evolution, but is challenging in most species. The Drosophila melanogaster Genetic Reference Panel (DGRP) is a collection of 205 inbred strains with whole genome sequences derived from a single wild population in Raleigh, NC, USA. The large amount of quantitative genetic variation, lack of population structure, and rapid local decay of linkage disequilibrium in the DGRP and outbred populations derived from DGRP lines present a favorable scenario for performing genome-wide association (GWA) mapping analyses to identify candidate causal genes, polymorphisms, and pathways affecting quantitative traits. The many GWA studies utilizing the DGRP have revealed substantial natural genetic variation for all reported traits, little evidence for variants with large effects but enrichment for variants with low P-values, and a tendency for lower frequency variants to have larger effects than more common variants. The variants detected in the GWA analyses rarely overlap those discovered using mutagenesis, and often are the first functional annotations of computationally predicted genes. Variants implicated in GWA analyses typically have sex-specific and genetic background-specific (epistatic) effects, as well as pleiotropic effects on other quantitative traits. Studies in the DGRP reveal substantial genetic control of environmental variation. Taking account of genetic architecture can greatly improve genomic prediction in the DGRP. These features of the genetic architecture of quantitative traits are likely to apply to other species, including humans. WIREs Dev Biol 2018, 7:e289. doi: 10.1002/wdev.289 This article is categorized under: Invertebrate Organogenesis > Flies.

**Judge:** SUPPORTED: Specifies 205 sequenced inbred strains from one wild Raleigh population and their use in quantitative-trait mapping.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 3. lit02, PMID 24714809

**Claim:** About **half of DGRP lines** are infected with *Wolbachia*. Across quantitative traits, infection effects were **rarely statistically significant**, though that does not mean every trait is unaffected; one study, for example, reported a weak effect on recombination rate. [PMID:24714809] [PMID:27035832]

**Abstract:** *Natural variation in genome architecture among 205 Drosophila melanogaster Genetic Reference Panel lines.* The Drosophila melanogaster Genetic Reference Panel (DGRP) is a community resource of 205 sequenced inbred lines, derived to improve our understanding of the effects of naturally occurring genetic variation on molecular and organismal phenotypes. We used an integrated genotyping strategy to identify 4,853,802 single nucleotide polymorphisms (SNPs) and 1,296,080 non-SNP variants. Our molecular population genomic analyses show higher deletion than insertion mutation rates and stronger purifying selection on deletions. Weaker selection on insertions than deletions is consistent with our observed distribution of genome size determined by flow cytometry, which is skewed toward larger genomes. Insertion/deletion and single nucleotide polymorphisms are positively correlated with each other and with local recombination, suggesting that their nonrandom distributions are due to hitchhiking and background selection. Our cytogenetic analysis identified 16 polymorphic inversions in the DGRP. Common inverted and standard karyotypes are genetically divergent and account for most of the variation in relatedness among the DGRP lines. Intriguingly, variation in genome size and many quantitative traits are significantly associated with inversions. Approximately 50% of the DGRP lines are infected with Wolbachia, and four lines have germline insertions of Wolbachia sequences, but effects of Wolbachia infection on quantitative traits are rarely significant. The DGRP complements ongoing efforts to functionally annotate the Drosophila genome. Indeed, 15% of all D. melanogaster genes segregate for potentially damaged proteins in the DGRP, and genome-wide analyses of quantitative traits identify novel candidate genes. The DGRP lines, sequence data, genotypes, quality scores, phenotypes, and analysis and visualization tools are publicly available.

**Judge:** SUPPORTED: Reports approximately 50% infection and says Wolbachia effects on quantitative traits are rarely significant.

**Second reviewer (second LLM):** agree

**Human:** SUPPORTED: agree. The recombination effect comes from the co-cited paper.

---

## 4. lit02, PMID 27035832

**Claim:** About **half of DGRP lines** are infected with *Wolbachia*. Across quantitative traits, infection effects were **rarely statistically significant**, though that does not mean every trait is unaffected; one study, for example, reported a weak effect on recombination rate. [PMID:24714809] [PMID:27035832]

**Abstract:** *The Genetic Architecture of Natural Variation in Recombination Rate in Drosophila melanogaster.* Meiotic recombination ensures proper chromosome segregation in many sexually reproducing organisms. Despite this crucial function, rates of recombination are highly variable within and between taxa, and the genetic basis of this variation remains poorly understood. Here, we exploit natural variation in the inbred, sequenced lines of the Drosophila melanogaster Genetic Reference Panel (DGRP) to map genetic variants affecting recombination rate. We used a two-step crossing scheme and visible markers to measure rates of recombination in a 33 cM interval on the X chromosome and in a 20.4 cM interval on chromosome 3R for 205 DGRP lines. Though we cannot exclude that some biases exist due to viability effects associated with the visible markers used in this study, we find ~2-fold variation in recombination rate among lines. Interestingly, we further find that recombination rates are uncorrelated between the two chromosomal intervals. We performed a genome-wide association study to identify genetic variants associated with recombination rate in each of the two intervals surveyed. We refined our list of candidate variants and genes associated with recombination rate variation and selected twenty genes for functional assessment. We present strong evidence that five genes are likely to contribute to natural variation in recombination rate in D. melanogaster; these genes lie outside the canonical meiotic recombination pathway. We also find a weak effect of Wolbachia infection on recombination rate and we confirm the interchromosomal effect. Our results highlight the magnitude of population variation in recombination rate present in D. melanogaster and implicate new genetic factors mediating natural variation in this quantitative trait.

**Judge:** SUPPORTED: Explicitly reports a weak effect of Wolbachia infection on recombination rate.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 5. lit04, PMID 8641052

**Claim:** The abstracts I found do not establish which stored reserves explain evolved starvation-resistance differences among selected Drosophila populations. In one study of lines selected for early versus delayed reproduction, the authors specifically found that a lipid–starvation-resistance mechanism did not explain their long-lived strains; the study does not show that lipid or glycogen explains evolved starvation resistance generally. [PMID:8641052] / “Comparative biochemical and stress analysis of genetically selected Drosophila strains with different longevities.” [PMID:8641052]

**Abstract:** *Comparative biochemical and stress analysis of genetically selected Drosophila strains with different longevities.* We have performed a comparative analysis of the effects of age of reproduction on the biochemical (protein, lipid, and glycogen content) and stress resistance (ability to survive starvation, desiccation, and exogenous paraquat) parameters on 10 sister lines of five different Drosophila strains. Four pairs of these sister lines were selected under different regimens for either early or delayed reproduction; the fifth pair was maintained in a nonselected state and served as the baseline strain to which all others were compared. It is generally accepted that the early regimens give rise to short-lived phenotypes, whereas the delayed regimens give rise to long-lived phenotypes. Our results suggest that a mechanism involving lipid and starvation resistance is not operative in our long-lived strains. In addition, a mechanism involving glycogen content and desiccation resistance is only weakly supported. Finally, there is strong support for a mechanism that gives rise to enhanced paraquat resistance and therefore may involve regulatory changes in the pattern of ADS gene expression. In addition, the 15-day early age of reproduction regimen (M type) shows qualitatively similar responses to that of the late age at reproduction regimen (L type). These results suggest that correlations between biochemical traits and longevity must be interpreted with caution. We discuss possible reasons for these results, including the possibility of multiple mechanisms, each leading to a different extended longevity phenotype.

**Judge:** SUPPORTED: The study found lipid-linked starvation resistance was not operative in its long-lived strains; it does not establish a general reserve mechanism.

**Second reviewer (second LLM):** agree. The citation supports its claim, although the answer as a whole missed the question (cited a longevity-selection study).

**Human:** ?

---

## 6. lit05, PMID 17488184

**Claim:** The Drosophila homolog of human ATGL is **Brummer (bmm)**. Flies lacking Brummer accumulate excess body fat because they cannot mobilize stored fat normally; Brummer is important for both ongoing fat regulation and acute fat mobilization. [PMID:17488184]

**Abstract:** *Dual lipolytic control of body fat storage and mobilization in Drosophila.* Energy homeostasis is a fundamental property of animal life, providing a genetically fixed balance between fat storage and mobilization. The importance of body fat regulation is emphasized by dysfunctions resulting in obesity and lipodystrophy in humans. Packaging of storage fat in intracellular lipid droplets, and the various molecules and mechanisms guiding storage-fat mobilization, are conserved between mammals and insects. We generated a Drosophila mutant lacking the receptor (AKHR) of the adipokinetic hormone signaling pathway, an insect lipolytic pathway related to ss-adrenergic signaling in mammals. Combined genetic, physiological, and biochemical analyses provide in vivo evidence that AKHR is as important for chronic accumulation and acute mobilization of storage fat as is the Brummer lipase, the homolog of mammalian adipose triglyceride lipase (ATGL). Simultaneous loss of Brummer and AKHR causes extreme obesity and blocks acute storage-fat mobilization in flies. Our data demonstrate that storage-fat mobilization in the fly is coordinated by two lipocatabolic systems, which are essential to adjust normal body fat content and ensure lifelong fat-storage homeostasis.

**Judge:** SUPPORTED: Identifies Brummer as the mammalian ATGL homolog and links its loss to obesity and impaired fat mobilization.

**Second reviewer (second LLM):** disagree. PARTIAL. The abstract states that Brummer is the ATGL homolog and matters for fat storage and mobilization, but obesity is reported only for the double Brummer + AKHR loss. 'Flies lacking Brummer accumulate excess fat' is not stated here.

**Human:** PARTIAL: sides with the second reviewer. Obesity is reported only for the double Brummer + AKHR loss, and the cause ('cannot mobilize stored fat normally') is not given in the abstract.

---

## 7. lit06, PMID 15374818

**Claim:** The authors suggest this is because the ablated flies mobilize energy reserves more slowly; they also become progressively less active [PMID:15374818].

**Abstract:** *AKH-producing neuroendocrine cell ablation decreases trehalose and induces behavioral changes in Drosophila.* Adipokinetic hormone (AKH) is a metabolic neuropeptide principally known for its mobilization of energy substrates, notably lipid and trehalose during energy-requiring activities, such as flight and locomotion. Drosophila melanogaster AKH cell localization in corpora cardiaca, as in other insect species, was confirmed by immunoreactivity and by a genetic approach using the UAS/GAL4 system. To assess AKH general physiological rules, we ablated AKH endocrine cells by specifically driving the expression of apoptosis transgenes in AKH cells. Trehalose levels were decreased in larvae and starved adults, when the stimulation by AKH of the production of trehalose from fat body glycogen is no longer possible. Moreover, we show that these adults without AKH cells become progressively hypoactive. Finally, under starvation conditions, those hypoactive AKH-knockout cell flies survived approximately 50% longer than control wild-type flies, suggesting that the slower rate at which AKH-ablated flies mobilize their energy resources extends their survival.

**Judge:** SUPPORTED: The abstract reports progressive hypoactivity and suggests slower energy-resource mobilization explains extended survival.

**Second reviewer (second LLM):** agree

**Human:** SUPPORTED: agree. 'This' refers to ~50% longer starvation survival in the preceding (uncited) sentence, which the abstract states; confirmed against the full answer.

---

## 8. lit07, PMID 9754535

**Claim:** In one comparison of 43 populations evolved under different selection protocols, total stored energy was very strongly associated with starvation resistance (R² = 0.99); the authors concluded that genetically increased storage of both lipids and carbohydrates underlay the response [PMID:9754535].

**Abstract:** *Metabolic reserves and evolved stress resistance in Drosophila melanogaster.* We have examined starvation and desiccation resistance in 43 outbred populations of Drosophila melanogaster that have diverged from a common ancestral population as a result of a variety of defined selection protocols. The populations differ up to 8.5-fold in desiccation resistance and up to 10-fold in starvation resistance. We used these populations to search for evolved physiological changes that might explain the differences in stress resistance. We examined two hypotheses for increased stress resistance that had been proposed previously in the literature: (1) that increments in starvation resistance are principally the result of differential lipid accumulation, and (2) that changes in glycogen accumulation play a role in evolved increases in resistance to desiccation stress. By quantifying desiccation resistance, starvation resistance, lipid content, and carbohydrate content in each of our populations of flies, we were able to demonstrate strong correlations between the capacity of the flies to resist starvation and the quantity of lipid or carbohydrate that the flies had stored. The strongest correlation (R2 = 0.99) was observed when the total energy content of both the lipid and carbohydrate stores was regressed against starvation resistance. These results demonstrate that the flies responded to selection for starvation resistance through a genetically determined increase in both lipid and carbohydrate storage. Similar analyses of the correlation between lipid storage or total energy storage and desiccation resistance revealed no significant correlations. Carbohydrate storage was significantly correlated with desiccation resistance in female but not in male flies. These results suggest that different forms of stress are resisted with distinct physiological mechanisms and that the evolutionary response of the flies to stress selection is specific to the stress imposed.

**Judge:** SUPPORTED: The abstract reports R² = 0.99 for total energy and starvation resistance, and increased storage of both lipids and carbohydrates.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 9. lit07, PMID 21983144

**Claim:** The route need not be identical in every population: studies of wild-derived flies associate greater starvation resistance with lipid storage and use, while other lines show variation in carbohydrate as well as lipid reserves [PMID:21983144].

**Abstract:** *Trade-off of energy metabolites as well as body color phenotypes for starvation and desiccation resistance in montane populations of Drosophila melanogaster.* Storage of energy metabolites has been investigated in different sets of laboratory selected desiccation or starvation resistant lines but few studies have examined such changes in wild-caught populations of Drosophila melanogaster. In contrast to parallel selection of desiccation and starvation tolerance under laboratory selection experiments, opposite clines were observed in wild populations of D. melanogaster. If resistance to desiccation and starvation occurs in opposite directions under field conditions, we may expect a trade-off for energy metabolites but such correlated changes are largely unknown. We tested whether there is a trade-off for storage as well as actual utilization of carbohydrates (trehalose and glycogen), lipids and proteins in D. melanogaster populations collected from different altitudes (512-2500 m). For desiccation resistance, darker flies (>50% body melanization) store more body water content and endure greater loss of water (higher dehydration tolerance) as compared to lighter flies (<30% body melanization). Based on within population analysis, we found evidence for coadapted phenotypes i.e. darker flies store and actually utilize more carbohydrates to confer greater desiccation resistance. In contrast, higher starvation resistance in lighter flies is associated with storage and actual utilization of greater lipid amount. However, darker and lighter flies did not vary in the rate of utilization of carbohydrates under desiccation stress; and of lipids under starvation stress. Thus, we did not find support for the hypothesis that a lower rate of utilization of energy metabolites may contribute to greater stress resistance. Further, for increased desiccation resistance of darker flies, about two-third of total energy budget is provided by carbohydrates. By contrast, lighter flies derive about 66% of total energy content from lipids which sustain higher starvation tolerance. Our results support evolutionary trade-off for storage as well as utilization of energy metabolites for desiccation versus starvation resistance in D. melanogaster.

**Judge:** SUPPORTED: Wild-derived populations linked starvation resistance with lipid storage and use; carbohydrate and lipid patterns varied across stress phenotypes.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 10. lit07, PMID 16033550

**Claim:** Artificial selection also produced starvation resistance as a correlated response to selection on several other stress traits, suggesting that different selection histories can reach it through partly distinct mechanisms; that study did not identify the physiological basis of each response [PMID:16033550].

**Abstract:** *Correlated responses to selection for stress resistance and longevity in a laboratory population of Drosophila melanogaster.* Laboratory studies on Drosophila have revealed that resistance to one environmental stress often correlates with resistance to other stresses. There is also evidence on genetic correlations between stress resistance, longevity and other fitness-related traits. The present work investigates these associations using artificial selection in Drosophila melanogaster. Adult flies were selected for increased survival after severe cold, heat, desiccation and starvation stresses as well as increased heat-knockdown time and lifespan (CS, HS, DS, SS, KS and LS line sets, respectively). The number of selection generations was 11 for LS, 27 for SS and 21 for other lines, with selection intensity being around 0.80. For each set of lines, the five stress-resistance parameters mentioned above as well as longevity (in a nonstressful environment) were estimated. In addition, preadult developmental time, early age productivity and thorax length were examined in all lines reared under nonstressful conditions. Comparing the selection lines with unselected control revealed clear-cut direct selection responses for the stress-resistance traits. Starvation resistance increased as correlated response in all sets of selection lines, with the exception of HS. Positive correlated responses were also found for survival after cold shock (HS and DS) and heat shock (KS and DS). With regard to values of resistance across different stress assays, the HS and KS lines were most similar. The resistance values of the SS lines were close to those of the LS lines and tended to be the lowest among all selection lines. Developmental time was extended in the SS and KS lines, whereas the LS lines showed a reduction in thorax length. The results indicate a possibility of different multiple-stress-resistance mechanisms for the examined traits and fitness costs associated with stress resistance and longevity.

**Judge:** PARTIAL: Starvation resistance rose across most selection lines, but the abstract does not establish distinct mechanisms or say physiological bases were unidentified.

**Second reviewer (second LLM):** agree. Borderline: 'possibility of different multiple-stress-resistance mechanisms' supports most of the claim.

**Human:** ?

---

## 11. lit08, PMID 22570636

**Claim:** GBLUP predicted DGRP starvation resistance **modestly**: the cross-validated correlation between predicted genetic values and observed phenotypes was **0.239 ± 0.008**. Using BayesB or selecting SNPs by effect size or variance explained did not improve prediction; performance declined only when fewer than 150,000 SNPs were used. The authors suggested prediction relied mainly on subtle relatedness captured by the SNP data, rather than directly tagging causal variants. [PMID:22570636]

**Abstract:** *Using whole-genome sequence data to predict quantitative trait phenotypes in Drosophila melanogaster.* Predicting organismal phenotypes from genotype data is important for plant and animal breeding, medicine, and evolutionary biology. Genomic-based phenotype prediction has been applied for single-nucleotide polymorphism (SNP) genotyping platforms, but not using complete genome sequences. Here, we report genomic prediction for starvation stress resistance and startle response in Drosophila melanogaster, using ∼2.5 million SNPs determined by sequencing the Drosophila Genetic Reference Panel population of inbred lines. We constructed a genomic relationship matrix from the SNP data and used it in a genomic best linear unbiased prediction (GBLUP) model. We assessed predictive ability as the correlation between predicted genetic values and observed phenotypes by cross-validation, and found a predictive ability of 0.239±0.008 (0.230±0.012) for starvation resistance (startle response). The predictive ability of BayesB, a Bayesian method with internal SNP selection, was not greater than GBLUP. Selection of the 5% SNPs with either the highest absolute effect or variance explained did not improve predictive ability. Predictive ability decreased only when fewer than 150,000 SNPs were used to construct the genomic relationship matrix. We hypothesize that predictive power in this population stems from the SNP-based modeling of the subtle relationship structure caused by long-range linkage disequilibrium and not from population structure or SNPs in linkage disequilibrium with causal variants. We discuss the implications of these results for genomic prediction in other organisms.

**Judge:** SUPPORTED: The abstract reports the stated correlation, methods, SNP threshold, and authors’ hypothesis about subtle relatedness rather than causal-variant tagging.

**Second reviewer (second LLM):** agree

**Human:** SUPPORTED: agree. Minor: 'selecting SNPs by effect size' slightly broadens 'the top 5% of SNPs'.

---

## 12. lit09, PMID 31544155

**Claim:** - In laboratory-reared female *An. gambiae* and *An. arabiensis*, species classification accuracy was **82.6%**. Predicted age distributions were statistically indistinguishable from the modeled true distributions. The authors noted that larger datasets were needed to improve accuracy and extend the approach to wild mosquitoes. [PMID:31544155] / So, the method is promising, but a model trained in one setting may not transfer reliably to another; field-relevant validation and consistent sample handling matter. [PMID:31544155] [PMID:41957079] [PMID:35933384]

**Abstract:** *Prediction of mosquito species and population age structure using mid-infrared spectroscopy and supervised machine learning.* Despite the global efforts made in the fight against malaria, the disease is resurging. One of the main causes is the resistance that Anopheles mosquitoes, vectors of the disease, have developed to insecticides. Anopheles must survive for at least 10 days to possibly transmit malaria. Therefore, to evaluate and improve malaria vector control interventions, it is imperative to monitor and accurately estimate the age distribution of mosquito populations as well as their population sizes. Here, we demonstrate a machine-learning based approach that uses mid-infrared spectra of mosquitoes to characterise simultaneously both age and species identity of females of the African malaria vector species Anopheles gambiae and An. arabiensis, using laboratory colonies. Mid-infrared spectroscopy-based prediction of mosquito age structures was statistically indistinguishable from true modelled distributions. The accuracy of classifying mosquitoes by species was 82.6%. The method has a negligible cost per mosquito, does not require highly trained personnel, is rapid, and so can be easily applied in both laboratory and field settings. Our results indicate this method is a promising alternative to current mosquito species and age-grading approaches, with further improvements to accuracy and expansion for use with wild mosquito vectors possible through collection of larger mid-infrared spectroscopy data sets.

**Judge:** PARTIAL: Accuracy and age-distribution results are stated; larger datasets may improve accuracy and enable wild use, but transfer concerns are not directly tested.

**Second reviewer (second LLM):** disagree. SUPPORTED. The paper's own claims (82.6%, age structure, need for larger/wild datasets) are exact; the transfer caveat is a grouped claim supported by the co-cited papers.

**Human:** SUPPORTED: sides with the second reviewer. Wording point: the abstract says improvements are *possible* with larger datasets, not *needed*, and says the method 'can be easily applied in both laboratory and field settings'. The answer makes the authors sound more cautious than they are (#16 repeats this).

---

## 13. lit09, PMID 41957079

**Claim:** - A study of male *An. gambiae* complex mosquitoes reported **86% species** and **85% age-group** accuracy in laboratory data. In semi-field samples, accuracy fell to **64%** and **50%**, respectively; including semi-field samples through transfer learning improved it to **73%** and **70%**. [PMID:41957079] / So, the method is promising, but a model trained in one setting may not transfer reliably to another; field-relevant validation and consistent sample handling matter. [PMID:31544155] [PMID:41957079] [PMID:35933384]

**Abstract:** *Age-grading and species identification of male mosquito Anopheles gambiae s.l. using mid-infrared spectroscopy and machine learning.* Most malaria vector control strategies target female Anopheles mosquitoes that transmit parasites, but emerging approaches such as gene drive, sterile insect technique, or Wolbachia require the release of males. Successful deployment depends on reliable knowledge of the species composition and age structure of male populations to overcome potential barriers to mating. Although approaches including near-infrared spectroscopy have been explored for male species identification and age grading, these methods remain constrained by limited validation, scalability, and accuracy under operational field conditions. Here we tested mid-infrared spectroscopy (MIRS) coupled with machine learning (ML) as a rapid and cost-effective approach for classifying species and age of male mosquitoes within the Anopheles gambiae complex. We used male mosquitoes from two laboratory-reared colonies in Burkina Faso (Anopheles coluzzii and An. gambiae) to develop a MIRS-ML model for species and age group (1–4, 5–10, 11–17 days) prediction under controlled conditions. This model was tested against a genetic and environmentally variable dataset consisting of male offspring obtained from gravid or blood fed Anopheles coluzzii and An. gambiae females collected from houses from two villages, Vallée du Kou and Soumousso and reared to adulthood in a semi-field system. The MIRS spectra from 2,120 males, representing both species, all age groups and both laboratory and semi-field backgrounds, were analysed using an extreme gradient boosting (XGBoost) algorithm to assess the ability to correctly predict age group and species. The XGBoost model classified mosquito species (86%) and age groups (85%) accurately in laboratory data, but performance declined under semi-field conditions (64% for species, 50% for age), reflecting environmental variability. Incorporating semi-field samples through transfer learning improved accuracy to 73% for species and 70% for age, underscoring both the limits of laboratory-only models and the value of transfer learning for enhancing generalisability in field settings. Our results demonstrate that mid-infrared spectroscopy with supervised machine learning (MIRS-ML) holds potential as a rapid tool for identifying the species and age group of cryptic male malaria vectors and represent one of the first applications of this approach to male Anopheles gambiae s.l. evaluated under semi-field conditions. However, before the approach can be used, larger datasets are needed to improve the classification algorithms and validate them for prediction in field populations.

**Judge:** SUPPORTED: The abstract reports the stated laboratory, semi-field, and transfer-learning accuracies and cautions about laboratory-only generalisability.

**Second reviewer (second LLM):** agree

**Human:** SUPPORTED: agree. All six accuracy figures match.

---

## 14. lit09, PMID 37898634

**Claim:** - A non-destructive approach using mosquito legs reported **73%** accuracy for distinguishing *An. gambiae* from *An. coluzzii* and **77%** for distinguishing 3- and 10-day-old mosquitoes, under laboratory conditions. [PMID:37898634]

**Abstract:** *Evaluation of diffuse reflectance spectroscopy for predicting age, species, and cuticular resistance of Anopheles gambiae s.l under laboratory conditions.* Mid-infrared spectroscopy (MIRS) combined with machine learning analysis has shown potential for quick and efficient identification of mosquito species and age groups. However, current technology to collect spectra is destructive to the sample and does not allow targeting specific tissues of the mosquito, limiting the identification of other important biological traits such as insecticide resistance. Here, we assessed the use of a non-destructive approach of MIRS for vector surveillance, micro diffuse reflectance spectroscopy (µDRIFT) using mosquito legs to identify species, age and cuticular insecticide resistance within the Anopheles gambiae s.l. complex. These mosquitoes are the major vectors of malaria in Africa and the focus on surveillance in malaria control programs. Legs required significantly less scanning time and showed more spectral consistence compared to other mosquito tissues. Machine learning models were able to identify An. gambiae and An. coluzzii with an accuracy of 0.73, two ages groups (3 and 10 days old) with 0.77 accuracy and we obtained accuracy of 0.75 when identifying cuticular insecticide resistance. Our results highlight the potential of different mosquito tissues and µDRIFT as tools for biological trait identification on mosquitoes that transmit malaria. These results can guide new ways of identifying mosquito traits which can help the creation of innovative surveillance programs by adapting new technology into mosquito surveillance and control tools.

**Judge:** SUPPORTED: The abstract reports leg-based accuracy of 0.73 for species and 0.77 for age groups under laboratory conditions.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 15. lit09, PMID 35933384

**Claim:** So, the method is promising, but a model trained in one setting may not transfer reliably to another; field-relevant validation and consistent sample handling matter. [PMID:31544155] [PMID:41957079] [PMID:35933384]

**Abstract:** *Effects of sample preservation methods and duration of storage on the performance of mid-infrared spectroscopy for predicting the age of malaria vectors.* BACKGROUND: Monitoring the biological attributes of mosquitoes is critical for understanding pathogen transmission and estimating the impacts of vector control interventions on the survival of vector species. Infrared spectroscopy and machine learning techniques are increasingly being tested for this purpose and have been proven to accurately predict the age, species, blood-meal sources, and pathogen infections in Anopheles and Aedes mosquitoes. However, as these techniques are still in early-stage implementation, there are no standardized procedures for handling samples prior to the infrared scanning. This study investigated the effects of different preservation methods and storage duration on the performance of mid-infrared spectroscopy for age-grading females of the malaria vector, Anopheles arabiensis.
METHODS: Laboratory-reared An. arabiensis (N = 3681) were collected at 5 and 17 days post-emergence, killed with ethanol, and then preserved using silica desiccant at 5 °C, freezing at - 20 °C, or absolute ethanol at room temperature. For each preservation method, the mosquitoes were divided into three groups, stored for 1, 4, or 8 weeks, and then scanned using a mid-infrared spectrometer. Supervised machine learning classifiers were trained with the infrared spectra, and the support vector machine (SVM) emerged as the best model for predicting the mosquito ages.
RESULTS: The model trained using silica-preserved mosquitoes achieved 95% accuracy when predicting the ages of other silica-preserved mosquitoes, but declined to 72% and 66% when age-classifying mosquitoes preserved using ethanol and freezing, respectively. Prediction accuracies of models trained on samples preserved in ethanol and freezing also reduced when these models were applied to samples preserved by other methods. Similarly, models trained on 1-week stored samples had declining accuracies of 97%, 83%, and 72% when predicting the ages of mosquitoes stored for 1, 4, or 8 weeks respectively.
CONCLUSIONS: When using mid-infrared spectroscopy and supervised machine learning to age-grade mosquitoes, the highest accuracies are achieved when the training and test samples are preserved in the same way and stored for similar durations. However, when the test and training samples were handled differently, the classification accuracies declined significantly. Protocols for infrared-based entomological studies should therefore emphasize standardized sample-handling procedures and possibly additional statistical procedures such as transfer learning for greater accuracy.

**Judge:** PARTIAL: The abstract directly supports consistent sample handling; it studies preservation and storage, not field-relevant validation or setting transfer.

**Second reviewer (second LLM):** disagree. SUPPORTED. Grouped citation: this paper supports the sample-handling part; the co-cited papers cover setting transfer.

**Human:** SUPPORTED: sides with the second reviewer. Supports the sample-handling part directly, and partly the transfer point (95% → 66-72% across preservation methods).

---

## 16. lit10, PMID 31544155

**Claim:** **Not reliably established.** In the 2019 study, age-structure predictions matched the *modelled* age distributions in laboratory-colony data, but the authors identified larger datasets and testing with wild mosquitoes as necessary next steps—not as demonstrated solutions to population transfer [PMID:31544155]. / The earlier study proposed collecting larger spectroscopy datasets and expanding evaluation to wild vectors [PMID:31544155].

**Abstract:** *Prediction of mosquito species and population age structure using mid-infrared spectroscopy and supervised machine learning.* Despite the global efforts made in the fight against malaria, the disease is resurging. One of the main causes is the resistance that Anopheles mosquitoes, vectors of the disease, have developed to insecticides. Anopheles must survive for at least 10 days to possibly transmit malaria. Therefore, to evaluate and improve malaria vector control interventions, it is imperative to monitor and accurately estimate the age distribution of mosquito populations as well as their population sizes. Here, we demonstrate a machine-learning based approach that uses mid-infrared spectra of mosquitoes to characterise simultaneously both age and species identity of females of the African malaria vector species Anopheles gambiae and An. arabiensis, using laboratory colonies. Mid-infrared spectroscopy-based prediction of mosquito age structures was statistically indistinguishable from true modelled distributions. The accuracy of classifying mosquitoes by species was 82.6%. The method has a negligible cost per mosquito, does not require highly trained personnel, is rapid, and so can be easily applied in both laboratory and field settings. Our results indicate this method is a promising alternative to current mosquito species and age-grading approaches, with further improvements to accuracy and expansion for use with wild mosquito vectors possible through collection of larger mid-infrared spectroscopy data sets.

**Judge:** SUPPORTED: The abstract reports laboratory-colony testing and says larger datasets and wild-vector expansion are possible future improvements.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 17. lit10, PMID 38500231

**Claim:** The study used mosquitoes reared from larvae collected in one Tanzanian region, so the abstract does not establish that these improvements generalize to other populations [PMID:38500231].

**Abstract:** *Rapid classification of epidemiologically relevant age categories of the malaria vector, Anopheles funestus.* BACKGROUND: Accurately determining the age and survival probabilities of adult mosquitoes is crucial for understanding parasite transmission, evaluating the effectiveness of control interventions and assessing disease risk in communities. This study was aimed at demonstrating the rapid identification of epidemiologically relevant age categories of Anopheles funestus, a major Afro-tropical malaria vector, through the innovative combination of infrared spectroscopy and machine learning, instead of the cumbersome practice of dissecting mosquito ovaries to estimate age based on parity status.
METHODS: Anopheles funestus larvae were collected in rural south-eastern Tanzania and reared in an insectary. Emerging adult females were sorted by age (1-16 days old) and preserved using silica gel. Polymerase chain reaction (PCR) confirmation was conducted using DNA extracted from mosquito legs to verify the presence of An. funestus and to eliminate undesired mosquitoes. Mid-infrared spectra were obtained by scanning the heads and thoraces of the mosquitoes using an attenuated total reflection-Fourier transform infrared (ATR-FT-IR) spectrometer. The spectra (N = 2084) were divided into two epidemiologically relevant age groups: 1-9 days (young, non-infectious) and 10-16 days (old, potentially infectious). The dimensionality of the spectra was reduced using principal component analysis, and then a set of machine learning and multi-layer perceptron (MLP) models were trained using the spectra to predict the mosquito age categories.
RESULTS: The best-performing model, XGBoost, achieved overall accuracy of 87%, with classification accuracy of 89% for young and 84% for old An. funestus. When the most important spectral features influencing the model performance were selected to train a new model, the overall accuracy increased slightly to 89%. The MLP model, utilizing the significant spectral features, achieved higher classification accuracy of 95% and 94% for the young and old An. funestus, respectively. After dimensionality reduction, the MLP achieved 93% accuracy for both age categories.
CONCLUSIONS: This study shows how machine learning can quickly classify epidemiologically relevant age groups of An. funestus based on their mid-infrared spectra. Having been previously applied to An. gambiae, An. arabiensis and An. coluzzii, this demonstration on An. funestus underscores the potential of this low-cost, reagent-free technique for widespread use on all the major Afro-tropical malaria vectors. Future research should demonstrate how such machine-derived age classifications in field-collected mosquitoes correlate with malaria in human populations.

**Judge:** SUPPORTED: Mosquito larvae were collected in rural south-eastern Tanzania; the abstract reports no evaluation across other populations.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 18. lit11, PMID 19815877

**Claim:** In the original study, near-infrared spectroscopy (NIRS) identified **field-collected mosquitoes’ species with about 80% accuracy**, rising to **almost 100% for laboratory-reared mosquitoes**. For age, it classified young versus old females with **about 80% accuracy**; when the comparison was simply young versus old insects, accuracy was **at least 90%**. [PMID:19815877]

**Abstract:** *Non-destructive determination of age and species of Anopheles gambiae s.l. using near-infrared spectroscopy.* Determining malaria vector species and age is crucial to measure malaria risk. Although different in ecology and susceptibility to control, the African malaria vectors Anopheles gambiae sensu stricto and An. arabiensis are morphologically similar and can be differentiated only by molecular techniques. Furthermore, few reliable methods exist to estimate the age of these vectors, which is a key predictor of malaria transmission intensity. We evaluated the use of near-infrared spectroscopy (NIRS) to determine vector species and age. This non-destructive technique predicted the species of field-collected mosquitoes with approximately 80% accuracy and predicted the species of laboratory-reared insects with almost 100% accuracy. The relative age of young or old females was predicted with approximately 80% accuracy, and young and old insects were predicted with > or = 90% accuracy. For applications where rapid assessment of the age structure and species composition of wild vector populations is needed, NIRS offers a valuable alternative to traditional methods.

**Judge:** SUPPORTED: The abstract reports approximately 80% field species accuracy, almost 100% laboratory accuracy, and the stated age accuracies.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 19. lit12, PMID 25583649

**Claim:** Unckless et al. measured six nutritional indices across DGRP lines: **glucose, glycogen, glycerol, protein, triglycerides, and wet weight**. Flies were reared on either a **low-glucose** or **high-glucose** diet. The study found significant genetic variation in these measures and reported significant correlations between nutritional phenotypes and previously published measures of **starvation resistance, oxidative-stress sensitivity, and endoplasmic-reticulum stress**. The abstract does not specify which individual indices correlated with which stress phenotypes. [PMID:25583649]

**Abstract:** *A genome-wide association study for nutritional indices in Drosophila.* Individuals are genetically variable for the way in which they process nutrients and in the effects of dietary content on reproductive success, immunity, and development. Here, we surveyed genetic variation for nutrient stores (glucose, glycogen, glycerol, protein, triglycerides, and wet weight) in the Drosophila Genetic Reference Panel (DGRP) after rearing the flies on either a low-glucose or high-glucose diet. We found significant genetic variation for these nutritional phenotypes and identified candidate genes that underlie that variation using genome-wide associations. In addition, we found several significant correlations between the nutritional phenotypes measured in this study and other previously published phenotypes, such as starvation stress resistance, oxidative stress sensitivity, and endoplasmic reticulum stress, which reinforce the notion that these lines can be used to robustly measure related phenotypes across distinct laboratories.

**Judge:** SUPPORTED: The abstract lists all six indices, both diets, genetic variation, and correlations with the three named stress phenotypes.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 20. lit13, PMID 29456884

**Claim:** No. In the studies retrieved, increased desiccation resistance was **not linked to a greater total amount of cuticular hydrocarbons**. One study instead associated it with a higher proportion of desaturated hydrocarbons, while another found no difference in total surface lipids between selected resistant flies and controls; the resistant flies had longer-chain hydrocarbons. [PMID:29456884] [PMID:9225453]

**Abstract:** *Desiccation resistance: effect of cuticular hydrocarbons and water content in Drosophila melanogaster adults.* BACKGROUND: The insect cuticle covers the whole body and all appendages and has bi-directionnal selective permeability: it protects against environmental stress and pathogen infection and also helps to reduce water loss. The adult cuticle is often associated with a superficial layer of fatty acid-derived molecules such as waxes and long chain hydrocarbons that prevent rapid dehydration. The waterproofing properties of cuticular hydrocarbons (CHs) depend on their chain length and desaturation number. Drosophila CH biosynthesis involves an enzymatic pathway including several elongase and desaturase enzymes.
METHODS: The link between desiccation resistance and CH profile remains unclear, so we tested (1) experimentally selected desiccation-resistant lines, (2) transgenic flies with altered desaturase expression and (3) natural and laboratory-induced CH variants. We also explored the possible relationship between desiccation resistance, relative water content and fecundity in females.
RESULTS: We found that increased desiccation resistance is linked with the increased proportion of desaturated CHs, but not with their total amount. Experimentally-induced desiccation resistance and CH variation both remained stable after many generations without selection. Conversely, flies with a higher water content and a lower proportion of desaturated CHs showed reduced desiccation resistance. This was also the case in flies with defective desaturase expression in the fat body.
DISCUSSION: We conclude that rapidly acquired desiccation resistance, depending on both CH profile and water content, can remain stable without selection in a humid environment. These three phenotypes, which might be expected to show a simple relationship, turn out to have complex physiological and genetic links.

**Judge:** SUPPORTED: The abstract reports increased desiccation resistance with more desaturated hydrocarbons, but not greater total hydrocarbon amount.

**Second reviewer (second LLM):** agree

**Human:** SUPPORTED: agree. The answer correctly says 'total surface lipids' for the second paper.

---

## 21. lit13, PMID 9225453

**Claim:** No. In the studies retrieved, increased desiccation resistance was **not linked to a greater total amount of cuticular hydrocarbons**. One study instead associated it with a higher proportion of desaturated hydrocarbons, while another found no difference in total surface lipids between selected resistant flies and controls; the resistant flies had longer-chain hydrocarbons. [PMID:29456884] [PMID:9225453]

**Abstract:** *Physiological mechanisms of evolved desiccation resistance in Drosophila melanogaster.* We investigated physiological characters associated with water balance in laboratory populations of Drosophila melanogaster selected for resistance to desiccating conditions for over 100 generations. Five replicate, outbred, desiccation-selected (D) populations were compared with their control (C) populations. Water loss rates of female D flies were approximately 40% lower than those of C females. Although excretory water loss was reduced in desiccation-selected flies, it comprised less than 10% of total water loss, indicating that the D populations have evolved reduced cuticular and/or respiratory water loss rates. Total surface lipid amounts did not differ between the C and D flies. Cuticular hydrocarbons from D flies were longer than those from C flies and melted at slightly higher temperatures, possibly contributing to reduced water loss rates. Desiccation-selected flies contained approximately 30% more bulk water than controls, as well as more glycogen. However, total metabolic water stores did not differ between the stocks owing to higher lipid levels in the C populations. The ability to tolerate water loss, as measured by water content at the time of death, did not differ between D and C flies. Thus, evolution of increased desiccation resistance has occurred by multiple physiological mechanisms, but some potential adaptive differences have not evolved.

**Judge:** SUPPORTED: Selected resistant flies had unchanged total surface lipids and longer-chain cuticular hydrocarbons than controls.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 22. lit14, PMID 25943032

**Claim:** In other words, it describes how much small-scale environmental differences or stochastic effects contribute to variation within a genotype [PMID:25943032]. / The extent of plasticity was trait-specific [PMID:25943032].

**Abstract:** *Genetic Architecture of Micro-Environmental Plasticity in Drosophila melanogaster.* Individuals of the same genotype do not have the same phenotype for quantitative traits when reared under common macro-environmental conditions, a phenomenon called micro-environmental plasticity. Genetic variation in micro-environmental plasticity is assumed in models of the evolution of phenotypic variance, and is important in applied breeding and personalized medicine. Here, we quantified genetic variation for micro-environmental plasticity for three quantitative traits in the inbred, sequenced lines of the Drosophila melanogaster Genetic Reference Panel. We found substantial genetic variation for micro-environmental plasticity for all traits, with broad sense heritabilities of the same magnitude or greater than those of trait means. Micro-environmental plasticity is not correlated with residual segregating variation, is trait-specific, and has genetic correlations with trait means ranging from zero to near unity. We identified several candidate genes associated with micro-environmental plasticity of startle response, including Drosophila Hsp90, setting the stage for future genetic dissection of this phenomenon.

**Judge:** SUPPORTED: Defines within-genotype variation under common macro-environments as micro-environmental plasticity.

**Second reviewer (second LLM):** agree. 'Stochastic effects' is a light paraphrase. Note the judge rated this same citation PARTIAL in its first run and SUPPORTED in its second.

**Human:** SUPPORTED: agree, but the most borderline of the six: 'stochastic effects' is not in the abstract.

---

## 23. lit15, PMID 22949659

**Claim:** No. In a comparison of three life-history traits, **none of the SNPs associated with the traits in Flyland replicated in the DGRP, and none of the DGRP-associated SNPs replicated in Flyland**. The study reported that the traits were highly polygenic in both populations; many Flyland-associated SNPs nevertheless participated in epistatic interactions in the DGRP. [PMID:22949659]

**Abstract:** *Epistasis dominates the genetic architecture of Drosophila quantitative traits.* Epistasis-nonlinear genetic interactions between polymorphic loci-is the genetic basis of canalization and speciation, and epistatic interactions can be used to infer genetic networks affecting quantitative traits. However, the role that epistasis plays in the genetic architecture of quantitative traits is controversial. Here, we compared the genetic architecture of three Drosophila life history traits in the sequenced inbred lines of the Drosophila melanogaster Genetic Reference Panel (DGRP) and a large outbred, advanced intercross population derived from 40 DGRP lines (Flyland). We assessed allele frequency changes between pools of individuals at the extremes of the distribution for each trait in the Flyland population by deep DNA sequencing. The genetic architecture of all traits was highly polygenic in both analyses. Surprisingly, none of the SNPs associated with the traits in Flyland replicated in the DGRP and vice versa. However, the majority of these SNPs participated in at least one epistatic interaction in the DGRP. Despite apparent additive effects at largely distinct loci in the two populations, the epistatic interactions perturbed common, biologically plausible, and highly connected genetic networks. Our analysis underscores the importance of epistasis as a principal factor that determines variation for quantitative traits and provides a means to uncover genetic networks affecting these traits. Knowledge of epistatic networks will contribute to our understanding of the genetic basis of evolutionarily and clinically important traits and enhance predictive ability at an individualized level in medicine and agriculture.

**Judge:** SUPPORTED: The abstract reports no SNP replication between populations, high polygenicity, and most associated SNPs participating in DGRP epistatic interactions.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 24. lit16, PMID 17714282

**Claim:** The review’s main conclusion is that starvation resistance in *Drosophila* reflects a broader “survival mode”: flies can evolve or induce greater resistance, typically through increased lipid storage and altered metabolism, alongside reduced reproduction. These shifts often coincide with greater resistance to desiccation and oxidative stress and with longer development and lifespan. The authors emphasize that although the genetic and physiological mechanisms were becoming clearer, the ecological reasons for natural variation in starvation resistance remained poorly understood. [PMID:17714282]

**Abstract:** *Evolutionary biology of starvation resistance: what we have learned from Drosophila.* Most animals face periods of food shortage and are thus expected to evolve adaptations enhancing starvation resistance (SR). Most of our knowledge of the genetic and physiological bases of those adaptations, their evolutionary correlates and trade-offs, and patterns of within- and among-population variation, comes from studies on Drosophila. In this review, we attempt to synthesize the various facets of evolutionary biology of SR emerging from those studies. Heritable variation for SR is ubiquitous in Drosophila populations, allowing for large responses to experimental selection. Individual flies can also inducibly increase their SR in response to mild nutritional stress (dietary restriction). Both the evolutionary change and the physiological plasticity involve increased accumulation of lipids, changes in carbohydrate and lipid metabolism and reduction in reproduction. They are also typically associated with greater resistance to desiccation and oxidative stress, and with prolonged development and lifespan. These responses are increasingly seen as facets of a shift of the physiology towards a 'survival mode', which helps the animal to survive hard times. The last decade has seen a great progress in revealing the molecular bases of induced responses to starvation, and the first genes contributing to genetic variation in SR have been identified. In contrast, little progress has been made in understanding the ecological significance of SR in Drosophila; in particular it remains unclear to what extent geographical variation in SR reflect differences in natural selection acting on this trait rather than correlated responses to selection on other traits. Drosophila offers a unique opportunity for an integrated study of the manifold aspects of adaptation to nutritional stress. Given that at least some major molecular mechanisms of response to nutritional stress seem common to animals, the insights from Drosophila are likely to apply more generally than just to dipterans or insects.

**Judge:** SUPPORTED: The abstract directly describes survival mode, lipid and metabolic changes, reduced reproduction, correlated traits, and unresolved ecological significance.

**Second reviewer (second LLM):** agree

**Human:** ?

---

## 25. tax02, PMID 14738315

**Claim:** Yes. **Drosophila simulans** and **Drosophila melanogaster** are both in the **D. melanogaster species subgroup**. NCBI Taxonomy lists their shared subgroup in each lineage; a phylogenetic study also identifies both among species of that subgroup. [PMID:14738315]

**Abstract:** *Molecular phylogeny of the Drosophila melanogaster species subgroup.* Although molecular and phenotypic evolution have been studied extensively in Drosophila melanogaster and its close relatives, phylogenetic relationships within the D. melanogaster species subgroup remain unresolved. In particular, recent molecular studies have not converged on the branching orders of the D. yakuba-D. teissieri and D. erecta-D. orena species pairs relative to the D. melanogaster-D. simulans-D. mauritiana-D. sechellia species complex. Here, we reconstruct the phylogeny of the melanogaster species subgroup using DNA sequence data from four nuclear genes. We have employed "vectorette PCR" to obtain sequence data for orthologous regions of the Alcohol dehydrogenase (Adh), Alcohol dehydrogenase related (Adhr), Glucose dehydrogenase (Gld), and rosy (ry) genes (totaling 7164 bp) from six melanogaster subgroup species (D. melanogaster, D. simulans, D. teissieri, D. yakuba, D. erecta, and D. orena) and three species from subgroups outside the melanogaster species subgroup [D. eugracilis (eugracilis subgroup), D. mimetica (suzukii subgroup), and D. lutescens (takahashii subgroup)]. Relationships within the D. simulans complex are not addressed. Phylogenetic analyses employing maximum parsimony, neighbor-joining, and maximum likelihood methods strongly support a D. yakuba-D. teissieri and D. erecta-D. orena clade within the melanogaster species subgroup. D. eugracilis is grouped closer to the melanogaster subgroup than a D. mimetica-D. lutescens clade. This tree topology is supported by reconstructions employing simple (single parameter) and more complex (nonreversible) substitution models.

**Judge:** SUPPORTED: The abstract explicitly lists both D. melanogaster and D. simulans among species of the melanogaster subgroup.

**Second reviewer (second LLM):** agree

**Human:** ?

---
