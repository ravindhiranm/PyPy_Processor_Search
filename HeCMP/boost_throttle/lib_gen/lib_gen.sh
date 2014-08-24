#!/bin/bash

paste 1GHz_SPEC_RESULTS 2GHz_SPEC_RESULTS 3GHz_SPEC_RESULTS>results.csv

cat results.csv | tr "," " " | awk ' { print $1,$2, $3,$22,$41, $4,$5,$6,$7,$8,$9,$10,$11, $12, $13,$32,$51, $14,$33,$52, $35, $17,$36,$55, $18,$37,$56, $19,$38,$57}' | tr " " "," > SPEC_THROTTLE_BOOST
