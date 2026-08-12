#!/bin/bash
# Run all experimental conditions across all models.
# Usage:
#   cd /Users/core/Documents/GradSchool/CS699/rational-thinking
#   caffeinate -i bash experiments/run_all.sh
#
# To resume after interruption, just re-run — checkpoints handle it.
# Estimated time: ~35-50 hours total (sequential)

set -e

# Small tier (≤3.8B): 4 models, different architectures
# Medium tier (8B): 2 models
# Large tier (12B): 1 model
MODELS=("llama3.2:1b" "gemma2:2b" "llama3.2:3b" "phi3:mini" "llama3:8b" "qwen3:8b" "gemma3:12b")
CONDITIONS=(1 2 3 4 5 6 7 8)

echo "=========================================="
echo "FULL EXPERIMENT RUN"
echo "Models: ${MODELS[*]}"
echo "Conditions: ${CONDITIONS[*]}"
echo "Sample: experiments/sample_1000.json"
echo "=========================================="
echo ""

TOTAL=$((${#MODELS[@]} * ${#CONDITIONS[@]}))
CURRENT=0

for MODEL in "${MODELS[@]}"; do
    echo ""
    echo "=========================================="
    echo "MODEL: $MODEL"
    echo "=========================================="
    for COND in "${CONDITIONS[@]}"; do
        CURRENT=$((CURRENT + 1))
        echo ""
        echo "--- [$CURRENT/$TOTAL] $MODEL condition $COND ---"
        python3 experiments/run_condition.py --model "$MODEL" --condition "$COND"
        echo ""
    done
done

echo ""
echo "=========================================="
echo "ALL RUNS COMPLETE"
echo "=========================================="
