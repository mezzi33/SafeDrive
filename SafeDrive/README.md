# SafeDrive: A Knowledge- and Data-Driven Risk-Sensitive Decision-Making Framework for Autonomous Vehicles

SafeDrive is a groundbreaking framework that enhances autonomous vehicle (AV) decision-making by integrating large language model (LLM) based agent with a novel risk quantification model. SafeDrive consists of four core modules: Risk Quantification, Reasoning, Reflection, and Memory.

---

## Getting Started

## 1. Requirements 
To get started with SafeDrive:

```bash
pip install -r requirements.txt
```

## 2. Configuration
OPENAI_API_TYPE: 'openai' 
# OpenAI-specific settings
OPENAI_KEY: 'sk-xxxxxx'
OPENAI_CHAT_MODEL: 'gpt-4o'  # Alternative: 'gpt-4'


## 3. Running SafeDrive

```bash
python demo_run.py
```

## 4. Analyzing Results

A log file will be created after running the demo, recording the reasoning process.

## 5. Citation
@article{zhou2024safedrive,
  title={SafeDrive: A Knowledge- and Data-Driven Risk-Sensitive Decision-Making Framework for Autonomous Vehicles},
  author={Zhou, Zhiyuan and Huang, Heye and Shi, Guanya and Li, Boqi and Zhao, Shiyue},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2024}
}

## 6. License
