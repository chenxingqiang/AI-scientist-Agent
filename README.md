<div align="center">
  <h1>
    <b>🤖 AI Scientist Agent</b><br>
    <b>Cost-Effective Scientific Research Automation</b><br>
    <b>Powered by DeepSeek & Intelligent Literature Search</b>
  </h1>
</div>

<p align="center">
  🚀 <strong>80-85% Cost Reduction</strong> |
  🧠 <strong>DeepSeek Integration</strong> |
  📚 <strong>Smart Literature Search</strong> |
  🔄 <strong>Intelligent Fallback</strong>
</p>

<p align="center">
  📚 <a href="https://pub.sakana.ai/ai-scientist-v2/paper">[Original Paper]</a> |
  📝 <a href="https://sakana.ai/ai-scientist-first-publication/"> [Blog Post]</a> |
  🔧 <a href="#key-improvements">[Our Improvements]</a>
</p>

**AI Scientist Agent** is an enhanced version of the AI Scientist-v2 system, optimized for cost-effective scientific research automation. This system autonomously generates hypotheses, runs experiments, analyzes data, and writes scientific manuscripts with significant cost reductions and improved reliability.

Built upon the foundation of [AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2), our enhanced version integrates **DeepSeek models** as the default choice and implements **intelligent literature search** with automatic fallback mechanisms.

## 🚀 Key Improvements

### 💰 **Massive Cost Reduction (80-85%)**
- **Original Cost**: $15-25 per experiment
- **Our Cost**: $3-5 per experiment  
- **Annual Savings**: Thousands of dollars for active researchers

### 🧠 **DeepSeek Integration**
- **Default Models**: `deepseek-chat` and `deepseek-reasoner`
- **Performance**: Comparable quality to GPT-4 at fraction of cost
- **Compatibility**: Full backward compatibility with all existing models

### 📚 **Smart Literature Search**
- **Primary**: SerpAPI for Google Scholar access
- **Fallback**: Automatic switch to Semantic Scholar
- **Reliability**: Zero-downtime literature search with intelligent error handling

### 🔄 **Enhanced Reliability**
- **Intelligent Fallback**: Automatic API switching when rate limits hit
- **Error Handling**: Comprehensive error recovery mechanisms  
- **Zero Configuration**: Works out-of-the-box with minimal setup

> **Note:**
> This enhanced version maintains all capabilities of AI Scientist-v2 while dramatically reducing costs and improving reliability. Perfect for researchers who want high-quality automated research at accessible prices.

> **Caution!**
> This codebase will execute Large Language Model (LLM)-written code. There are various risks and challenges associated with this autonomy, including the potential use of dangerous packages, uncontrolled web access, and the possibility of spawning unintended processes. Ensure that you run this within a controlled sandbox environment (e.g., a Docker container). Use at your own discretion.

## Table of Contents

1.  [Requirements](#requirements)
    *   [Installation](#installation)
    *   [Supported Models and API Keys](#supported-models-and-api-keys)
2.  [Generate Research Ideas](#generate-research-ideas)
3.  [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments)
4.  [Citing The AI Scientist-v2](#citing-the-ai-scientist-v2)
5.  [Frequently Asked Questions](#frequently-asked-questions)
6.  [Acknowledgement](#acknowledgement)

## Requirements

This code is designed to run on Linux with NVIDIA GPUs using CUDA and PyTorch.

### Installation

```bash
# Create a new conda environment
conda create -n ai_scientist python=3.11
conda activate ai_scientist

# Install PyTorch with CUDA support (adjust pytorch-cuda version for your setup)
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia

# Install PDF and LaTeX tools
conda install anaconda::poppler
conda install conda-forge::chktex

# Install Python package requirements
pip install -r requirements.txt
```

### Supported Models and API Keys

#### DeepSeek Models (Recommended)

For cost-effective research automation, we recommend DeepSeek models as the default choice. The system uses the `DEEPSEEK_API_KEY` environment variable for DeepSeek models:
- `deepseek-chat`: Optimized for code generation, feedback evaluation, and general tasks
- `deepseek-reasoner`: Advanced reasoning model for complex analysis and paper writing

#### OpenAI Models

The system can use OpenAI models via the `OPENAI_API_KEY` environment variable. OpenAI GPT-4o is still required for vision-related tasks (VLM feedback) as DeepSeek doesn't currently support vision capabilities.

#### Gemini Models

By default, the system uses the `GEMINI_API_KEY` environment variable for Gemini models through OpenAI API.

#### Claude Models via AWS Bedrock

To use Claude models provided by Amazon Bedrock, install the necessary additional packages:
```bash
pip install anthropic[bedrock]
```
Next, configure valid [AWS Credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-envvars.html) and the target [AWS Region](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) by setting the following environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME`.

#### Literature Search APIs

Our code supports multiple APIs for literature search to ensure comprehensive coverage and reliability:

**SerpAPI (Recommended - Google Scholar Access)**

For the best literature search experience, we recommend using SerpAPI which provides access to Google Scholar results. Set your SerpAPI key (`SERPAPI_KEY`) for high-quality academic paper search with comprehensive coverage and up-to-date results. This is used during both the ideation and paper writing stages.

**Semantic Scholar API (Alternative)**

Our code can also use a Semantic Scholar API Key (`S2_API_KEY`) for literature search [if you have one](https://www.semanticscholar.org/product/api). The system will automatically fall back to Semantic Scholar if SerpAPI is not available. While Semantic Scholar works without an API key, having one provides higher throughput and better rate limits.

#### Setting API Keys

Ensure you provide the necessary API keys as environment variables for the models you intend to use. For example:
```bash
# DeepSeek API (recommended for cost-effective research automation)
export DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY_HERE"
# Literature search (recommended: SerpAPI for Google Scholar access)
export SERPAPI_KEY="YOUR_SERPAPI_KEY_HERE"
# OpenAI API (required for vision tasks, optional for alternatives)
export OPENAI_API_KEY="YOUR_OPENAI_KEY_HERE"
# Alternative: Semantic Scholar API (optional, used as fallback)
export S2_API_KEY="YOUR_S2_KEY_HERE"
# Set AWS credentials if using Bedrock
# export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
# export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_KEY"
# export AWS_REGION_NAME="your-aws-region"
```

## Generate Research Ideas

Before running the full AI Scientist-v2 experiment pipeline, you first use the `ai_scientist/perform_ideation_temp_free.py` script to generate potential research ideas. This script uses an LLM to brainstorm and refine ideas based on a high-level topic description you provide, interacting with literature search tools (Google Scholar via SerpAPI, or Semantic Scholar as fallback) to check for novelty.

1.  **Prepare a Topic Description:** Create a Markdown file (e.g., `my_research_topic.md`) describing the research area or theme you want the AI to explore. This file should contain sections like `Title`, `Keywords`, `TL;DR`, and `Abstract` to define the scope of the research. Refer to the example file `ai_scientist/ideas/i_cant_believe_its_not_better.md` for the expected structure and content format. Place your file in a location accessible by the script (e.g., the `ai_scientist/ideas/` directory).

2.  **Run the Ideation Script:** Execute the script from the main project directory, pointing it to your topic description file and specifying the desired LLM.

    ```bash
    python ai_scientist/perform_ideation_temp_free.py \
     --workshop-file "ai_scientist/ideas/my_research_topic.md" \
     --model gpt-4o-2024-05-13 \
     --max-num-generations 20 \
     --num-reflections 5
    ```
    *   `--workshop-file`: Path to your topic description Markdown file.
    *   `--model`: The LLM to use for generating ideas (ensure you have the corresponding API key set).
    *   `--max-num-generations`: How many distinct research ideas to attempt generating.
    *   `--num-reflections`: How many refinement steps the LLM should perform for each idea.

3.  **Output:** The script will generate a JSON file named after your input Markdown file (e.g., `ai_scientist/ideas/my_research_topic.json`). This file will contain a list of structured research ideas, including hypotheses, proposed experiments, and related work analysis.

4.  **Proceed to Experiments:** Once you have the generated JSON file containing research ideas, you can proceed to the next section to run the experiments.

This ideation step guides the AI Scientist towards specific areas of interest and produces concrete research directions to be tested in the main experimental pipeline.

## Run AI Scientist-v2 Paper Generation Experiments

Using the JSON file generated in the previous ideation step, you can now launch the main AI Scientist-v2 pipeline. This involves running experiments via agentic tree search, analyzing results, and generating a paper draft.

Specify the models used for the write-up and review phases via command-line arguments.
The configuration for the best-first tree search (BFTS) is located in `bfts_config.yaml`. Adjust parameters in this file as needed.

Key tree search configuration parameters in `bfts_config.yaml`:

-   `agent` config:
    -   Set `num_workers` (number of parallel exploration paths) and `steps` (maximum number of nodes to explore). For example, if `num_workers=3` and `steps=21`, the tree search will explore up to 21 nodes, expanding 3 nodes concurrently at each step.
    -   `num_seeds`: Should generally be the same as `num_workers` if `num_workers` is less than 3. Otherwise, set `num_seeds` to 3.
    -   Note: Other agent parameters like `k_fold_validation`, `expose_prediction`, and `data_preview` are not used in the current version.
-   `search` config:
    -   `max_debug_depth`: The maximum number of times the agent will attempt to debug a failing node before abandoning that search path.
    -   `debug_prob`: The probability of attempting to debug a failing node.
    -   `num_drafts`: The number of initial root nodes (i.e., the number of independent trees to grow) during Stage 1.

Example command to run AI-Scientist-v2 using a generated idea file (e.g., `my_research_topic.json`). Please review `bfts_config.yaml` for detailed tree search parameters (the default config includes `claude-3-5-sonnet` for experiments). Do not set `load_code` if you do not want to initialize experimentation with a code snippet.

```bash
python launch_scientist_bfts.py \
 --load_ideas "ai_scientist/ideas/my_research_topic.json" \
 --load_code \
 --add_dataset_ref \
 --model_writeup deepseek-reasoner \
 --model_citation deepseek-chat \
 --model_review deepseek-chat \
 --model_agg_plots deepseek-chat \
 --num_cite_rounds 20
```

Once the initial experimental stage is complete, you will find a timestamped log folder inside the `experiments/` directory. Navigate to `experiments/"timestamp_ideaname"/logs/0-run/` within that folder to find the tree visualization file `unified_tree_viz.html`.

## Citing The AI Scientist-v2

If you use **The AI Scientist-v2** in your research, please cite our work as follows:

```bibtex
@article{aiscientist_v2,
  title={The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search},
  author={Yamada, Yutaro and Lange, Robert Tjarko and Lu, Cong and Hu, Shengran and Lu, Chris and Foerster, Jakob and Clune, Jeff and Ha, David},
  journal={arXiv preprint arXiv:2504.08066},
  year={2025}
}
```

## Frequently Asked Questions

**Why wasn't a PDF or a review generated for my experiment?**

The AI Scientist-v2 completes experiments with a success rate that depends on the chosen foundation model, and the complexity of the idea. Higher success rates are generally observed when using powerful models like Claude 3.5 Sonnet for the experimentation phase.

**What is the estimated cost per experiment?**

The ideation step cost depends on the LLM used and the number of generations/reflections, but is generally low (a few dollars). With the new default DeepSeek models, costs are significantly reduced:

- **Using DeepSeek models (recommended)**: Approximately $3-5 per complete experiment run, including experimentation and writing phases
- **Using Claude 3.5 Sonnet**: Around $15-20 for experimentation + $5 for writing (higher quality but more expensive)
- **Mixed approach**: DeepSeek for most tasks + GPT-4o for vision tasks provides the best cost-performance balance

DeepSeek models offer excellent performance at a fraction of the cost, making research automation more accessible.

**How do I run The AI Scientist-v2 for different subject fields?**

First, perform the [Generate Research Ideas](#generate-research-ideas) step. Create a new Markdown file describing your desired subject field or topic, following the structure of the example `ai_scientist/ideas/i_cant_believe_its_not_better.md`. Run the `perform_ideation_temp_free.py` script with this file to generate a corresponding JSON idea file. Then, proceed to the [Run AI Scientist-v2 Paper Generation Experiments](#run-ai-scientist-v2-paper-generation-experiments) step, using this JSON file with the `launch_scientist_bfts.py` script via the `--load_ideas` argument.

**What should I do if I have problems with literature search APIs?**

The system uses literature search APIs to assess the novelty of generated ideas and to gather citations during the paper write-up phase. We recommend using SerpAPI for Google Scholar access as the primary option. If you encounter issues:

1. **SerpAPI problems**: The system will automatically fall back to Semantic Scholar API
2. **No API keys**: The system can still use Semantic Scholar without an API key, though with rate limits
3. **All APIs failing**: You may skip the citation phase during paper generation if needed

For the best experience, set up SerpAPI for comprehensive Google Scholar coverage.

**I encountered a "CUDA Out of Memory" error. What can I do?**

This error typically occurs when the AI Scientist-v2 attempts to load or run a model that requires more GPU memory than available on your system. To resolve this, you can try updating your ideation prompt file (`ai_scientist/ideas/my_research_topic.md`) to suggest using smaller models for the experiments.

## Acknowledgement

The tree search component implemented within the `ai_scientist` directory is built on top of the [AIDE](https://github.com/WecoAI/aideml) project. We thank the AIDE developers for their valuable contributions and for making their work publicly available.


## 🚀 Quick Start

### 1. Set up Environment Variables
```bash
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export SERPAPI_KEY="your-serpapi-key"  # Optional but recommended
```

### 2. Generate Research Ideas
```bash
python ai_scientist/perform_ideation_temp_free.py \
  --workshop-file "ai_scientist/ideas/your_topic.md" \
  --model deepseek-chat \
  --max-num-generations 5
```

### 3. Run Experiments
```bash
python launch_scientist_bfts.py \
  --load_ideas "ai_scientist/ideas/your_topic.json" \
  --load_code \
  --add_dataset_ref
```

### 4. Results
- 📊 Find experiment results in `experiments/timestamp_ideaname/`
- 📈 View tree visualization at `logs/0-run/unified_tree_viz.html`
- 📄 Generated paper will be in the experiment directory

---

## 💫 Support the Project

If this project helps your research, please:
- ⭐ Star this repository
- 🐛 Report issues or suggest improvements
- 🤝 Contribute enhancements
- 📖 Share with other researchers

**Repository**: [https://github.com/chenxingqiang/AI-scientist-Agent](https://github.com/chenxingqiang/AI-scientist-Agent)

---

*Built with ❤️ by researchers, for researchers. Making high-quality automated research accessible to everyone.*

