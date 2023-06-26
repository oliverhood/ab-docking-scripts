#! /bin/sh

for file in ./*
  do
      ~/ab-docking-scripts/evaluate_megadock.py $file >> megadock_evaluation.txt
  done