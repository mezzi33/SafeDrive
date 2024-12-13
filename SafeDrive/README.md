# SafeDrive: A Knowledge- and Data-Driven Risk-Sensitive Decision-Making Framework for Autonomous Vehicles

<div class="content">
    <h2 class="section-title">Overview of the Framework</h2>
    <img src="../figures/Fig.1.png" alt="SafeDrive Framework Overview">
</div>
SafeDrive is a risk-sensitive decision-making framework for autonomous vehicles (AVs) that generates safe, real-time decisions based on real-world scene description inputs. It operates through a four-module cycle: the Risk Quantification Module, Memory Module, Reasoning Module, and Reflection Module, with large language models (LLMs) serving as the central agent.


# Getting Started

## 1. Requirements 
To get started with SafeDrive, we suggest using Python 3.11 with the following requirements:

```bash
pip install -r requirements.txt
```

## 2. Configuration
OPENAI_API_TYPE: 'openai'   
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
......
