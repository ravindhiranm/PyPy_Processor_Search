#!/bin/bash

paste SPEC_RESULTS_1GHz  SPEC_RESULTS_1500MHz  SPEC_RESULTS_2GHz SPEC_RESULTS_2500MHz  SPEC_RESULTS_3GHz > results.csv

                                                      ##Frequency                                         ##Cycles              ##IPC                     ##Peak_power        ##avg power           ##leak power
cat results.csv | tr "," " " | awk ' { print $1,$2,  $3,$22,$41,$60,$79,  $4,$5,$6,$7,$8,$9,$10,$11, $12, $13,$32,$51,$70,$89, $14,$33,$52,$71,$90, $35, $17,$36,$55,$74,$93, $18,$37,$56,$75,$94, $19,$38,$57,$76,$95}' | tr " " "," > SPEC_THROTTLE_BOOST
