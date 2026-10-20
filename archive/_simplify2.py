import json
from pathlib import Path
NB = Path(__file__).parent / "answer_structure_finetune.ipynb"
nb = json.load(open(NB))

for c in nb["cells"]:
    if c["cell_type"] == "code" and "def make_training_args" in "".join(c["source"]):
        s = "".join(c["source"])
        old = (
            "TRAIN_ARGS = dict(num_train_epochs=3, per_device_train_batch_size=8, gradient_accumulation_steps=2,\n"
            "                  learning_rate=2e-4, lr_scheduler_type='cosine', warmup_ratio=0.03,\n"
            "                  logging_steps=25, eval_strategy='epoch', save_strategy='no', bf16=True, report_to='none')\n"
            "import inspect\n"
            "def make_training_args(output_dir):\n"
            '    """Build TrainingArguments passing only kwargs this transformers version accepts.\n'
            '    Handles the eval_strategy/evaluation_strategy rename and any dropped args."""\n'
            "    sig = set(inspect.signature(TrainingArguments.__init__).parameters)\n"
            "    args = dict(TRAIN_ARGS)\n"
            "    # handle the eval_strategy <-> evaluation_strategy rename\n"
            "    if 'eval_strategy' not in sig and 'evaluation_strategy' in sig and 'eval_strategy' in args:\n"
            "        args['evaluation_strategy'] = args.pop('eval_strategy')\n"
            "    filtered = {k: v for k, v in args.items() if k in sig}\n"
            "    dropped = [k for k in args if k not in sig]\n"
            "    if dropped:\n"
            "        print('  (dropping unsupported TrainingArguments:', dropped, ')')\n"
            "    return TrainingArguments(output_dir=output_dir, **filtered)"
        )
        new = (
            "# Minimal, version-stable core args. make_training_args() filters anything this transformers\n"
            "# version does not accept, and adds the optional args only when supported. No eval_strategy:\n"
            "# short LoRA runs need no per-epoch validation (avoids the transformers-5.x eval API surface).\n"
            "TRAIN_ARGS = dict(num_train_epochs=3, per_device_train_batch_size=8, gradient_accumulation_steps=2,\n"
            "                  learning_rate=2e-4, logging_steps=25, save_strategy='no',\n"
            "                  bf16=True, report_to='none')\n"
            "OPTIONAL_TRAIN_ARGS = dict(lr_scheduler_type='cosine', warmup_ratio=0.03)  # added if supported\n"
            "import inspect\n"
            "def make_training_args(output_dir):\n"
            '    """Build TrainingArguments passing only kwargs this transformers version accepts.\n'
            '    Adds optional args when supported; handles eval_strategy/evaluation_strategy rename."""\n'
            "    sig = set(inspect.signature(TrainingArguments.__init__).parameters)\n"
            "    args = dict(TRAIN_ARGS)\n"
            "    for k, v in OPTIONAL_TRAIN_ARGS.items():\n"
            "        if k in sig: args[k] = v\n"
            "    if 'eval_strategy' not in sig and 'evaluation_strategy' in sig and 'eval_strategy' in args:\n"
            "        args['evaluation_strategy'] = args.pop('eval_strategy')\n"
            "    filtered = {k: v for k, v in args.items() if k in sig}\n"
            "    dropped = [k for k in args if k not in sig]\n"
            "    if dropped:\n"
            "        print('  (dropping unsupported TrainingArguments:', dropped, ')')\n"
            "    return TrainingArguments(output_dir=output_dir, **filtered)"
        )
        assert old in s, "OLD block not found exactly"
        c["source"] = [s.replace(old, new)]
        break

json.dump(nb, open(NB, "w"), indent=1)
print("applied")
