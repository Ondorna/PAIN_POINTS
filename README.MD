## Progress Update

### Current Progress

I converted two failure patterns from the interviews into controlled evaluation tasks:

- **Missing / Insufficient Information** — based on Swapnil H. A.'s case
- **Conflicting Data Sources** — based on Thanvi S.'s case

For each failure pattern, I designed five task variants and tested them with DeepSeek, Gemini, and OpenAI. Detailed model outputs and PASS / PARTIAL / FAIL results are recorded in the Excel file.

I also reviewed several papers and resources on benchmark and evaluation design. I found Scale AI's *Research Rubrics* particularly relevant and am continuing to study how to design more reliable evaluation criteria.

### Preliminary Observation

So far, the models are generally able to recognize when information is missing or when sources conflict. However, the behavior changes when they are required to give a definitive answer.

In the **Forced Decision** setting, models sometimes introduce assumptions that are not supported by the provided evidence in order to resolve the uncertainty or conflict.

### Next Steps

- Add more test cases for the current failure categories and explore additional failure patterns.
- Refine the evaluation rubric and scoring criteria.
- Look for more real-world examples to complement the controlled tasks.

### Questions to Discuss

1. I currently have two directions: **Missing / Insufficient Information** and **Conflicting Data Sources**. Should I continue developing both, or focus on one first? If focusing on one, which direction would be more valuable considering both feasibility and practical relevance?

2. Is **PASS / PARTIAL / FAIL** sufficient at this stage, or should I define separate evaluation dimensions such as **uncertainty detection, uncertainty preservation, and unsupported inference**?

3. Should I continue using comparable low-cost models from the three providers, or also include stronger reasoning models for comparison?

4. When designing the tasks, how can I make the evaluation examples more rigorous and representative while still keeping the variables controlled?