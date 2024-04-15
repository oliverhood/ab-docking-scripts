#!/usr/bin/perl -s
#*************************************************************************
#
#   Program:    listif
#   File:       listif.pl
#   
#   Version:    V1.0
#   Date:       16.11.21
#   Function:   Make a list of interface residues from a complex and
#               the two split files
#   
#   Copyright:  (c) Prof. Andrew C. R. Martin, UCL, 2021
#   Author:     Prof. Andrew C. R. Martin
#   Address:    Institute of Structural and Molecular Biology
#               Division of Biosciences
#               University College
#               Gower Street
#               London
#               WC1E 6BT
#   EMail:      andrew@bioinf.org.uk
#               
#*************************************************************************
#
#   This program is not in the public domain, but it may be copied
#   according to the conditions laid out in the accompanying file
#   COPYING.DOC
#
#   The code may be modified as required, but any modifications must be
#   documented so that the person responsible can be identified. If 
#   someone else breaks this code, I don't want to be blamed for code 
#   that does not work! 
#
#   The code may not be sold commercially or included as part of a 
#   commercial product except as described in the file COPYING.DOC.
#
#*************************************************************************
#
#   Description:
#   ============
#
#*************************************************************************
#
#   Usage:
#   ======
#
#*************************************************************************
#
#   Revision History:
#   =================
#
#*************************************************************************
use strict;

my $size=defined($::s)?($::s):8.0;

UsageDie() if(defined($::h) || (scalar(@ARGV) != 3));

# Get the command line arguments
my $complex  = shift(@ARGV);
my $antibody = shift(@ARGV);
my $antigen  = shift(@ARGV);

# Calculate the accessibilities
print STDERR "Calculating Complex accessibility...";
my %complexSA  = CalculateSA($complex);
print STDERR "done\nCalculating Antibody accessibility...";
my %antibodySA = CalculateSA($antibody);
print STDERR "done\nCalculating Antigen accessibility...";
my %antigenSA  = CalculateSA($antigen);
print STDERR "done\n";

# Find the interface residues
print STDERR "Finding Antibody interface residues...";
my @antibodyIF = FindIF(\%complexSA, \%antibodySA);
print STDERR "done\nFinding Antigen interface residues...";
my @antigenIF  = FindIF(\%complexSA, \%antigenSA);
print STDERR "done\n";

# Print the unexpanded interfaces if we aren't expanding
if(!defined($::x))
{
    print "# UNEXPANDED\n";
    PrintIF("Antibody", @antibodyIF);
    PrintIF("Antigen",  @antigenIF);
}
else
{
    # Expand an print the interfaces
    print STDERR "Expanding Antibody interface residues...";
    @antibodyIF = ExpandIF("$antibody.solv", $size, \@antibodyIF);
    print STDERR "done\nExpanding Antibody interface residues...";
    @antigenIF  = ExpandIF("$antigen.solv",  $size, \@antigenIF);
    print STDERR "done\n";

    print "# EXPANDED\n";
    PrintIF("Antibody", @antibodyIF);
    PrintIF("Antigen",  @antigenIF);
}

# Cleanup
unlink "$complex.solv";
unlink "$antigen.solv";
unlink "$antibody.solv";

#*************************************************************************
#  @expandedResidueList = ExpandIF($pdbFile, $size, \@residueList)
#  ---------------------------------------------------------------
#  Takes a .solv PDB file (with radius and accessibility data, an
#  expansion size and a reference to an array of residue IDs.
#  Calculates a patch of the required size around each residue in the
#  supplied list and extracts the residue IDs for the patch. The
#  unique set of residue IDs is then returned.
#
# 16.11.21 Original   By: ACRM
#
sub ExpandIF
{
    my($pdbFile, $size, $aResidues) = @_;
    my %residues = ();
    
    foreach my $centreRes (@$aResidues)
    {
        my $exe = "pdbmakepatch -r $size $centreRes CA $pdbFile";
        my $resultData = `$exe`;
        my @results = split(/\n/, $resultData);
        foreach my $result (@results)
        {
            if($result =~ /^ATOM  /)
            {
                my $bval = substr($result, 61, 5);
                if($bval > 0.5)
                {
                    my $resid = substr($result, 21, 6);
                    $resid =~ s/\s//g;
                    $residues{$resid} = 1;
                }
            }
        }
    }
    return(sort keys(%residues));
}


#*************************************************************************
# PrintIF($label, @residueList)
# ----------------------------
# Takes a label and an array of residue IDs. Prints the label preceded
# by a # followed by the residue list
#
# 16.11.21 Original   By: ACRM
#
sub PrintIF
{
    my($type, @residues) = @_;
    print("# $type\n");
    foreach my $residue (@residues)
    {
        print("$residue\n");
    }
    
}


#*************************************************************************
# @interface = FindIF(\%BoundAccessHash, \%FreeAccessHash)
# --------------------------------------------------------
# Takes a hash reference containing the accessibility for a complex and
# for a free member of the complex. Identifies residues where the
# accessibilty of at least 1A^2 greater in the free molecule.
#
# 16.11.21 Original   By: ACRM
#
sub FindIF
{
    my($hBoundSA, $hFreeSA) = @_;
    my @if = ();

    foreach my $freeRes (keys %$hFreeSA)
    {
        if(defined($$hBoundSA{$freeRes}) &&
           ($$hFreeSA{$freeRes} > $$hBoundSA{$freeRes} + 1))
        {
            push @if, $freeRes;
        }
    }
    return(sort @if);
}


#*************************************************************************
#  %access = CalculateSA($pdbFile)
#  -------------------------------
#  Obtains the relative accessibility for residues in a PDB file
#  as a hash keyed by the residue ID. Also writes a new PDB file
#  (with extension .solv) containing the atomic radii and
#  accessibility
#
# 16.11.21 Original   By: ACRM
#
sub CalculateSA
{
    my($pdbFile) = @_;
    my %access = ();
    if($pdbFile ne '')
    {
        my $exe = "pdbsolv -x -r stdout $pdbFile $pdbFile.solv";
        my $resultData = `$exe`;
        my @results = split(/\n/, $resultData);
        foreach my $result (@results)
        {
            if($result =~ /^RESACC/)
            {
                my $residue = substr($result, 8, 7);
                $residue =~ s/\s//g;
                $access{$residue} = substr($result, 30, 7);
            }
        }
    }
    return(%access);
}


#*************************************************************************
sub UsageDie
{
    print <<__EOF;

listif V1.0 (c) 2021 UCL, Prof. Andrew C.R. Martin.

Usage: listif [-x][-s=size] complex.pdb antibody.pdb antigen.pdb >reslist
       -x Expand the interface residues by patches of 'size' Angstroms
       -s Specify the expansion size [Default: 8A]

Takes a complex and the split files and identifies the interface residues
based on a difference of >1% relative accessibility. If -x is specified
expands the list of residues by looking at the surface and adding residues
within 'size' Angstroms.
    
__EOF
    exit 0;
}
