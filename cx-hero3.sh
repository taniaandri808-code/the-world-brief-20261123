#!/bin/bash
cd /root/newsimg23-entry
export CHAIN_API_KEY=dummy
exec timeout 620 codex exec --sandbox danger-full-access --skip-git-repo-check -c model='"openai/gpt-oss-120b"' "Read /root/newsimg23-entry/heroes_spec.md and write /root/newsimg23-entry/heroes.py exactly to that spec. Do not read any other file. Verify with python3 -c 'import heroes'. End with DONE."
