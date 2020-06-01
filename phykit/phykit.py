#!/usr/bin/env python

import logging
import sys
import textwrap
from argparse import (
    ArgumentParser,
    RawTextHelpFormatter,
    SUPPRESS,
    RawDescriptionHelpFormatter,
)

from .services.alignment.alignment_length import AlignmentLength
from .services.alignment.parsimony_informative_sites import ParsimonyInformative
from .services.alignment.variable_sites import VariableSites
from .services.alignment.alignment_length_no_gaps import AlignmentLengthNoGaps

from .services.tree.bipartition_support_stats import BipartitionSupportStats
from .services.tree.treeness import Treeness
from .services.tree.total_tree_length import TotalTreeLength
from .services.tree.internode_labeler import InternodeLabeler
from .services.tree.lb_score import LBScore
from .services.tree.dvmc import DVMC
from .services.tree.internal_branch_stats import InternalBranchStats

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class Phykit(object):
    def __init__(self):
        parser = ArgumentParser(
            add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                PhyKIT helps with all things phylogenetics and phylogenomics.

                Usage: phykit <command> [optional command arguments]

                Command specific help messages can be viewed by adding a 
                -h/--help argument after the command. For example, to see the
                to see the help message for the command 'treeness', execute
                phykit treeness -h or phykit treeness --help.

                Tree-based commands
                ===================
                bipartition_support_stats
                    - calculates summary statistics for bipartition support
                dvmc 
                    - reports the degree of violation of the molecular clock
                treeness
                    - reports treeness or stemminess, a measure of signal-to-
                      noise ratio in a phylogeny
                total_tree_length
                    - calculates total tree length
                lb_score
                    - calculates lb (long branch) score for taxa in a phylogeny
                internal_branch_stats
                    - calculates summary statistics for internal branch lengths 
                internode_labeler
                    - create labels at internodes in a phylogeny

                Alignment-based commands
                ========================
                alignment_length
                    - calculates alignment length
                alignment_length_no_gaps
                    - calculates alignment length after removing sites with gaps
                parsimony_informative_sites
                    - calculates the number and percentage of parsimony
                      informative sites in an alignment
                rcv
                    - calculates relative composition variability in an alignment
                    NOTE: NOT YET IMPLEMENTED
                variable_sites
                    - calculates the number and percentage of variable sites
                      in an alignment
                

                                        
                """
            ),
        )
        parser.add_argument("command", help=SUPPRESS)
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print("Invalid command option. See help for more details.")
            parser.print_help()
            sys.exit(1)

        getattr(self, args.command)()

    ## Tree functions
    def bipartition_support_stats(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link
                
                High bipartition support values are thought to be desirable because
                they are indicative of greater certainty in the tree topology.

                Calculate summary statistics for bipartition support. Summary
                statistics include mean, median, 25th percentile, 75th percentile,
                minimum, maximum, standard deviation, and variance. 

                To obtain all bipartition support values, use the -v/--verbose option.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            a tree file 
            
                -v, --verbose               optional argument to print
                                            all bipartition support
                                            values
                """
            ),
        )
        parser.add_argument("tree", type=str, help=SUPPRESS)
        parser.add_argument("-v", "--verbose", action="store_true", required=False, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        BipartitionSupportStats(args).run()

    def dvmc(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Lower DVMC (degree of violation of the molecular clock) values are
                thought to be desirable because they are indicative of a lower degree of
                violation in the molecular clock assumption.

                Typically, outgroup taxa are not included in molecular clock analysis. Thus,
                prior to calculating DVMC from a single gene tree, outgroup taxa are pruned
                from the phylogeny. PhyKIT will prune taxa using tip names from a single column
                file, which is specified using the -r/--root file. If the tip name does not
                exist in the input tree, rather than raising an error/warning message, the tip  
                name is skipped. If the user wants to calculate DVMC for phylogenies with incomplete
                taxa representation, this will allow the user to use one <root file> for all trees. 

                Calculate degree of violation of the molecular clock (or DVMC) in a tree
                following Liu et al., PNAS (2017), doi: 10.1073/pnas.1616744114.

                Options
                =====================================================
                -t, --tree <file>           input file tree name
            
                -r, --root <file>           single column file with
                                            tip names of root taxa
                """
            ),
        )
        parser.add_argument(
            "-r", "--root", type=str, required=True, help=SUPPRESS, metavar=""
        )
        parser.add_argument(
            "-t", "--tree", type=str, required=True, help=SUPPRESS, metavar=""
        )
        args = parser.parse_args(sys.argv[2:])
        DVMC(args).run()

    def treeness(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Higher treeness values are thought to be desirable because they
                represent a higher signal-to-noise ratio.

                Treeness describes the proportion of tree distance on internal
                branches. Treeness can be used as a measure of the signal-to-noise
                ratio in a phylogeny. 

                Calculate treeness (also referred to as stemminess) following
                Lanyon, The Auk (1988), doi: 10.1093/auk/105.3.565 and
                Phillips and Penny, Molecular Phylogenetics and Evolution
                (2003), doi: 10.1016/S1055-7903(03)00057-5.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            a tree file
                """
            ),
        )
        parser.add_argument("tree", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        Treeness(args).run()

    def total_tree_length(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Calculate total tree length, which is a sum of all branches. 

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            a tree file
                """
            ),
        )
        parser.add_argument("tree", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        TotalTreeLength(args).run()
    
    def lb_score(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Lower LB (long branch) scores are thought to be desirable
                because they are indicative of taxa or trees that likely do
                not have issues with long branch attraction.

                LB score is calculated from patristic distances (or the sum 
                of branches between to two taxa). More specifically, it is
                mean pairwise patristic distance of taxon i compared to
                all other taxa over the average pairwise patristic distance.
                Summary statistics reported include mean, median, 25th
                percentile, 75th percentile, minimum, maximum, standard 
                deviation, and variance of per taxon LB scores is reported.
                To obtain LB scores for each taxa, use the -v/--verbose option. 

                LB scores are calculated following Struck, Evolutionary 
                Bioinformatics (2014), doi: 10.4137/EBO.S14239.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            a tree file

                -v, --verbose               optional argument to print
                                            all LB score values            
                """
            ),
        )
        parser.add_argument("tree", type=str, help=SUPPRESS)
        parser.add_argument("-v", "--verbose", action="store_true", required=False, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        LBScore(args).run()

    def internal_branch_stats(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Internal branch lengths can be useful for tree diagnostics.

                Summary statistics of internal branch lengths include mean,
                median, 25th percentile, 75th percentile, minimum, maximum,
                standard deviation, and variance of per taxon LB scores is reported.
                To obtain all internal branch lengths, use the -v/--verbose option. 

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            a tree file

                -v, --verbose               optional argument to print
                                            all LB score values           
                """
            ),
        )
        parser.add_argument("tree", type=str, help=SUPPRESS)
        parser.add_argument("-v", "--verbose", action="store_true", required=False, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        InternalBranchStats(args).run()

    def internode_labeler(self):
        parser = ArgumentParser()
        parser.add_argument("tree", type=str)
        # TODO: add output option?
        args = parser.parse_args(sys.argv[2:])
        InternodeLabeler(args).run()

    ### Alignment functions
    def alignment_length(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Longer alignments are associated with strong phylogenetic signal.

                Length of the input alignment is calculated using this function.
                Association between alignment length and phylogenetic signal
                was determined by Shen et al., Genome Biology and Evolution (2016),
                doi: 10.1093/gbe/evw179.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            an alignment file           
                """
            ),
        )
        parser.add_argument("alignment", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        AlignmentLength(args).run()

    def alignment_length_no_gaps(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                Longer alignments when excluding sites with gaps is
                associated with strong phylogenetic signal.

                PhyKIT reports three tab delimited values:
                col1: number of sites without gaps
                col2: total number of sites
                col3: percentage of sites without gaps

                Association between alignment length when excluding sites
                with gaps and phylogenetic signal was determined by Shen 
                et al., Genome Biology and Evolution (2016), 
                doi: 10.1093/gbe/evw179.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            an alignment file          
                """
            ),
        )
        parser.add_argument("alignment", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        AlignmentLengthNoGaps(args).run()

    def parsimony_informative_sites(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                The number of parsimony informative sites in an alignment
                is associated with strong phylogenetic signal.

                PhyKIT reports three tab delimited values:
                col1: number of parsimony informative sites
                col2: total number of sites
                col3: percentage of parsimony informative sites

                Association between the number of parsimony informative
                sites and phylogenetic signal was determined by Shen 
                et al., Genome Biology and Evolution (2016), 
                doi: 10.1093/gbe/evw179.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            an alignment file          
                """
            ),
        )
        parser.add_argument("alignment", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        ParsimonyInformative(args).run()

    def rcv(self):
        raise NotImplementedError()

    def variable_sites(self):
        parser = ArgumentParser(add_help=True,
            usage=SUPPRESS,
            formatter_class=RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
                 _____  _           _  _______ _______ 
                |  __ \| |         | |/ /_   _|__   __|
                | |__) | |__  _   _| ' /  | |    | |   
                |  ___/| '_ \| | | |  <   | |    | |   
                | |    | | | | |_| | . \ _| |_   | |   
                |_|    |_| |_|\__, |_|\_\_____|  |_|   
                               __/ |                   
                              |___/   
                            
                Citation: Steenwyk et al. Journal, journal info, link

                The number of variable sites in an alignment is 
                associated with strong phylogenetic signal.

                PhyKIT reports three tab delimited values:
                col1: number of variable sites
                col2: total number of sites
                col3: percentage of variable sites

                Association between the number of variable sites and
                phylogenetic signal was determined by Shen et al.,
                Genome Biology and Evolution (2016), 
                doi: 10.1093/gbe/evw179.

                Options
                =====================================================
                <file>                      first argument after 
                                            function name should be
                                            an alignment file          
                """
            ),
        )
        parser.add_argument("alignment", type=str, help=SUPPRESS)
        args = parser.parse_args(sys.argv[2:])
        VariableSites(args).run()


if __name__ == "__main__":
    Phykit()
