Abbe's section for testing
--------------------------
---
PhyKIT helps process and analyze multiple sequence alignments and phylogenies.

Generally, all functions are designed to help understand the contents of alignments (e.g., gc content or the number of parsimony informative sites) and the shape of trees (e.g., treeness, degree of violation of a molecular clock).

Some help messages indicate that summary statistics are reported (e.g., bipartition_support_stats). Summary statistics include mean, median, 25th percentile, 75th percentile, minimum, maximum, standard deviation, and variance. These functions typically have a verbose option that allows users to get the underlying data used to calculate summary statistics.

<br />

**Download and install**

To avoid permission errors, we will install PhyKIT and the dependencies using a virtual environment:
```shell
git clone https://github.com/JLSteenwyk/PhyKIT.git
cd PhyKIT/
python -m venv .venv
source .venv/bin/activate
make install
```
Note, the virtual environment must be activated to use phykit.

Test installation by launching the help message
```shell
phykit -h
```

The following sections are condensed versions of the tutorials. Download links will be provided via the website. For now, the raw data can be found in PhyKIT/docs/data/

<br /><br />

**Tutorial 1. Summarize information content**

This tutorial uses the sample data *Steenwyk_etal_mBio_2019_EOG091N44MS.aln.fa* and *Steenwyk_etal_mBio_2019_EOG091N44MS.tre*.

Implementing functions in PhyKIT follows this general structure
```shell
phykit <command> [optional command arguments]
```

Each *command* or *function* have aliases. For example, the function to calculate the length of an alignment is *alignment_length*. However, typing *alignment_length* everytime you want to use this function is a lot of key strokes. Thus, I have created shortcuts or aliases. The aliases for *alignment_length* are *aln_len* and *al*.

<br />

**Alignment length**
Calculate alignment length
```shell
phykit aln_len Steenwyk_etal_mBio_2019_EOG091N44MS.aln.fa
624
```

<br />

**Alignment length no gaps**
Calculate alignment length but exclude sites with gaps
```shell
phykit aln_len_no_gaps ./docs/data/Steenwyk_etal_mBio_2019_EOG091N44MS.aln.fa
321     624     51.4423
```

<br />

**Bipartition support statistics**
```shell
phykit bss Steenwyk_etal_mBio_2019_EOG091N44MS.tre
mean: 88.6437
median: 99
25th percentile: 83.0
75th percentile: 100.0
minimum: 28
maximum: 100
standard deviation: 18.5504
variance: 344.1157
```

<br />

**Treeness divided by relative composition variability**
```shell
phykit toverr -a Steenwyk_etal_mBio_2019_EOG091N44MS.aln.fa -t Steenwyk_etal_mBio_2019_EOG091N44MS.tre
3.9773  0.5136  0.1291
```

Other functions highlighted in the long form tutorial include *lb_score*, *pis*, *sat*, *tness*, *rcv*, and *vs*. It is totally optional but if you would like to try using these functions, please refer to each function's help message.

<br /><br />

**Tutorial 2. Evaluating gene-gene covariation**

PhyKIT implements a mirror-tree-based method to identify genes that covary with one another. In principle, PhyKIT determines if two trees have similar branch length properties throughout the phylogeny. Thus, each input phylogeny must have the same topology. However, there are other steps that must be done prior to evaluating covariation between two genes.

To provide a comprehensive tutorial, we will start with the sequence alignments for three genes and their constrained tree topologies that match the putative species tree from Shen et al. 2020.

The test data for this is in docs/data/gene_gene_covariation_tutorial.tar.gz

Abbe, this tutorial is almost a *copy and paste* of the full tutorial that will be provided in the full documentation.

<br />

**Step 0: Prepare data**

The mirror tree method for determining significant gene-gene covariation requires that both input phylogenies have the same topology. As a result, gene trees must be constrained to the species tree, which is typically inferred from whole genome or proteome data. In the present tutorial, the species tree has already been inferred. Additionally, the guide trees used to constrain the gene trees have been generated. These trees were generated by pruning the species tree to match the taxon representation of the sequences in the multiple sequence alignment.

<br />

**Step 1: Estimate gene tree branch lengths**

To infer the constrained tree, we will use IQ-TREE2. The species tree (or guide tree) is specified with the -g argument. Lastly, the best-fitting substitution model was specified according to what was reported in Shen et al. 2020 supplementary data; however, if the best-fitting model is unknown, this will have to be determined prior to estimating gene tree branch lengths.

Estimate the gene tree branch lengths using the following commands:
```shell
# infer constrain trees
iqtree2 -s Shen_etal_SciAdv_2020_NDC80.fa -g Shen_etal_SciAdv_2020_NDC80.constrained.tre -pre Shen_etal_SciAdv_2020_NDC80 -m JTT+G4+F
iqtree2 -s Shen_etal_SciAdv_2020_NUF2.fa -g Shen_etal_SciAdv_2020_NUF2.constrained.tre -pre Shen_etal_SciAdv_2020_NUF2 -m LG+G4
iqtree2 -s Shen_etal_SciAdv_2020_SEC7.fa -g Shen_etal_SciAdv_2020_SEC7.constrained.tre -pre Shen_etal_SciAdv_2020_SEC7 -m LG+G4
```

<br />

**Step 2: Evaluate gene-gene covariation**

When determining gene-gene covariation, it is best to use a high significance threshold for correlation coefficients. I consider a threshold of 0.825 to be very conservative and that 0.8 is often sufficiently conservative. I like to be cautious so I recommend using a threshold of 0.825.

To evaluate gene-gene covariation, execute the following commands:
```shell
# Evaluate gene-gene covariation between NUF2 and SEC7
phykit cover Shen_etal_SciAdv_2020_NUF2.treefile Shen_etal_SciAdv_2020_SEC7.treefile -r Shen_etal_SciAdv_2020_species_tree.tre
0.7496  0.0

# Evaluate gene-gene covariation between NDC80 and SEC7
phykit cover Shen_etal_SciAdv_2020_NDC80.treefile Shen_etal_SciAdv_2020_SEC7.treefile -r Shen_etal_SciAdv_2020_species_tree.tre
0.763   0.0
```

Given our thresholds, neither NUF2 nor NDC80 significantly covary with SEC7. Next, evaluate gene-gene covariation between NUF2 and NDC80.
```shell
# Evaluate gene-gene covariation between NUF2 and NDC80
phykit cover Shen_etal_SciAdv_2020_NUF2.treefile Shen_etal_SciAdv_2020_NDC80.treefile -r Shen_etal_SciAdv_2020_species_tree.tre
0.8448  0.0
```

These two genes significantly covary with one another. This raises the hypothesis that these two genes have shared function. A literature- based examination of these genes reveals the encoded proteins are part of the same kinetochore-associated complex termed the NDC80 complex. Thus, PhyKIT is useful for determining gene-gene covariation, which can be driven by shared function, coexpression, and/or are part of the same multimeric complexes.

<br /><br />

**Tutorial 3. Identifying signatures of rapid radiations**

Abbe, similar to tutorial 2, this is pretty much a *copy and paste* of the full tutorial.

Signatures of rapid radiations or diversification events can be identified by pinpointing polytomies in a putative species tree (Sayyari and Mirarab 2018; One Thousand Plant Transcriptomes Initiative 2019; Li et al. 2020).

PhyKIT uses a gene-based approach to evaluate polytomies. In other words, PhyKIT will determine what topology each gene supports. Thereafter, PhyKIT will conduct a chi-squared test to determine if there is equal support among gene trees for the various topologies. In the chi-squared test, the null hypothesis is that there is equal support among gene trees for the various topologies and the alternative hypothesis is that there is unequal support for the various topologies. Thus, failing to reject the null hypothesis would indicate that there is a polytomy where as rejecting the null hypothesis would indicate there is no polytomy. The various topologies examined by PhyKIT are determined by the groups file. Formatting this file will be explained later.

To demonstrate how to identify polytomies, we will use a subset of 250 gene phylogenies from Steenwyk et al. 2019.

This dataset is in docs/data/polytomy_tutorial.tar.gz

<br />

**Step 0: Prepare data**
For this tutorial, the data has already been formatted for the user. There are two input files for the polytomy testing function:

a file that specifies the location of gene trees

a file that specifies the groups to test

Thus, this tutorial assumes that gene phylogenies have already been inferred and the area of the phylogeny that the user wishes to test for a polytomy has already been identified.

Examination of the first file reveals that that it is a single column file that specifies the pathing of gene phylogenies to use during polytomy testing. Examination of the second file reveals that groups are specified using a tab-separated five column file.

column 1: an identifier for the test, which is not used by PhyKIT. Instead, this column is intended to be for the user to write any keywords or notes that can help remind them of what they were testing.

column 2-4: the tip names in the groups. Each column represents a single group to conduct polytomy testing for. If a group has multiple taxa, separate each tip name using a semi-colon ‘;’. For example, in groups_file0.txt there is one group with Aspergillus_persii;Aspergillus_sclerotiorum wherein this group has two taxa, Aspergillus_persii and Aspergillus_sclerotiorum.

column 5: the outgroup taxa. This column specifies the name of outgroup taxa, which are used to root the gene trees prior to determining what topology they support. 

<br />

**Step 1: Conduct polytomy test**
Among the groups that have already been predetermined for the user, we will first conduct a polytomy test for groups_file0.txt. To execute the polytomy test, use the following command:
```shell
phykit ptt -t filamentous_fungi_250_trees.txt -g groups_file0.txt
Gene Support Frequency Results
==============================
chi-squared: 19.425
p-value: 6.1e-05
total genes: 240
0-1: 103
0-2: 49
1-2: 88
```

Note, if you are getting an error, it may be due to improper pathing in filamentous_fungi_250_trees.txt. Please check this file and modify it accordingly.

We will now go over the output of PhyKIT. PhyKIT will report the chi-squared value, the p value, the total number of genes used, followed by the support of sister relationships examined. Here, the chi-squared value is very high and the p value is very low indicating that the null hypothesis was rejected and that there is no evidence of a polytomy. The total number of genes used during the polytomy test was 240. However, you may have noticed that there were 250 genes used as input. This discrepancy is not an error but may be caused by two different reasons. (1) 10 genes were unable to be used due to incomplete taxon representation in the groups and (2) PhyKIT can account for gene phylogenies uncertainty (i.e., gene phylogenies with collapsed bipartitions), which may render the support of a given gene tree to be uncertain and therefore not be used during polytomy testing.

Next, the section 0-1, 0-2, and 1-2 refers to the sister relationships between the groups. Group 0 is specified in column 2 of the groups file while group 1 and group 2 are specified in columns 3 and 4, respectively. Thus, 0-1 refers to the following topology (((0,1),2),outgroup); whereas 0-2 and 1-2 refers to the following topologies (((0,2),1),outgroup); and (((1,2),0),outgroup);, respectively. PhyKIT identified that 103 gene phylogenies support (((0,1),2),outgroup); whereas 49 and 88 gene phylogenies support the topologies (((0,2),1),outgroup); and (((1,2),0),outgroup);, respectively.

<br />

Next, conduct a polytomy test using the other group file using the following command:
```shell
phykit ptt -t filamentous_fungi_250_trees.txt -g groups_file1.txt
Gene Support Frequency Results
==============================
chi-squared: 0.129
p-value: 0.937521
total genes: 248
0-1: 84
0-2: 84
1-2: 80
```

In contrast to the previous test, the chi-squared value is very low and the p value is very high indicating a failure to reject the null hypothesis. Thus, there is a signature of rapid radiation or diversification event for these groups. Additional details provided by PhyKIT reveal 248 genes were used during the polytomy test and that there is nearly equal support for the various topologies.

Taken together, this tutorial reveals how to identify signatures of rapid radiation or diversification events in phylogenomic data.

<br />

END Abbe's section for testing
--------------------------
---

<p align="center">
  <a href="https://github.com/jlsteenwyk/phykit">
    <img src="https://raw.githubusercontent.com/JLSteenwyk/PhyKIT/master/docs/_static/img/logo.jpg" alt="Logo" width="400">
  </a>
  <p align="center">
    <a href="https://jlsteenwyk.com/PhyKIT/">Docs</a>
    ·
    <a href="https://github.com/jlsteenwyk/phykit/issues">Report Bug</a>
    ·
    <a href="https://github.com/jlsteenwyk/phykit/issues">Request Feature</a>
  </p>
    <p align="center">
        <a href="https://lbesson.mit-license.org/" alt="License">
            <img src="https://img.shields.io/badge/License-MIT-blue.svg">
        </a>
        <a href="https://pypi.org/project/phykit/" alt="PyPI - Python Version">
            <img src="https://img.shields.io/pypi/pyversions/phykit">
        </a>
        <a href="https://github.com/JLSteenwyk/PhyKIT/actions" alt="Build">
            <img src="https://img.shields.io/github/workflow/status/jlsteenwyk/phykit/CI/master">
        </a>
        <a href="https://codecov.io/gh/jlsteenwyk/phykit" alt="Coverage">
          <img src="https://codecov.io/gh/jlsteenwyk/phykit/branch/master/graph/badge.svg?token=0J49I6441V">
        </a>
        <a href="https://github.com/jlsteenwyk/phykit/graphs/contributors" alt="Contributors">
            <img src="https://img.shields.io/github/contributors/jlsteenwyk/phykit">
        </a>
        <a href="https://twitter.com/intent/follow?screen_name=jlsteenwyk" alt="Author Twitter">
            <img src="https://img.shields.io/twitter/follow/jlsteenwyk?style=social&logo=twitter"
                alt="follow on Twitter">
        </a>
    </p>
</p>

PhyKIT is a toolkit for processing and analyzing multiple sequence alignments and phylogenies.<br /><br />
If you found clipkit useful, please cite *MANUSCRIPT TITLE*. bioRxiv. doi: [BIORXIV LINK](NA).
<br /><br />


---
