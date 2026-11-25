The awareness axis is the strongest part of your idea. Almost no existing work does an A/B test on "does the model behave differently when it knows ESBMC will check it?" Here is a design that tests it cleanly.

## 1. The core design: a ladder of conditions

Each level adds either knowledge, affordance or feedback, so differences between adjacent levels isolate one factor.

| Level | Model knows | Model can touch | Feedback | What it isolates |
|---|---|---|---|---|
| L0 | Nothing about ESBMC | Function body only | None | Natural defect rate (baseline) |
| L1 | "ESBMC will verify this" | Function body only | None | Effect of awareness alone |
| L2 | Same | Same | Pass/fail only, N attempts | Pressure from a reward signal |
| L3 | Same | Same | Full counterexample (ESBMC-AI style) | Repair vs gaming when the feedback is richer |
| L4 | Same | + may add assume/assert/nondet | Counterexample | Direct gaming surface in the code |
| L5 | Same | + may edit the harness and command flags | Counterexample | Full surface: shrink bounds, stub nondet, rewrite the property |

For L2 and up, add a framing toggle: neutral ("write correct code") versus "your goal is for verification to pass". That toggle is a cheap way to measure how much the instruction alone drives gaming.

Add a **tempting-task design**. Include tasks where the honest correct solution is hard for ESBMC (loop-heavy, timeouts at moderate k), alongside easy ones. If gaming shows up only on hard tasks, that is a much stronger result than an overall rate. Optionally add a few tasks with a deliberately loose frozen harness, to see whether models find a loophole that is already there.

## 2. Separating gaming from two lookalikes

You can't observe intent in a 7B model, so I'd avoid the word "cheating" in the paper's claims. Call the behaviour **verifier-exploiting**, and define it by contrast with L0.

There are three outcomes that must stay separate:
- **Verifier-friendly code:** the model avoids constructs ESBMC handles badly, and the code is still correct. This is legitimate, and likely common once the model is aware.
- **Exploiting:** a green verdict where the property isn't really checked, or the code is wrong.
- **Incompetence:** accidental weak or incorrect code. L0 versus L1 on the same task and seed is how you tell this apart from exploiting.

## 3. Ground truth

"Gamed-green" means ESBMC says success and an independent oracle says the code is wrong or the check was hollow. The oracle needs to be independent of ESBMC:
- hidden functional tests plus a reference implementation for differential testing,
- ASan/UBSan runs,
- assume-stripped and larger-bound reruns (see below),
- manual labels on a stratified sample for the detector evaluation.

Some green-but-wrong cases will be ESBMC limitations or bugs, not model behaviour. Triage and report those as their own category.

## 4. C++ specifics

- The earlier "Illusion of Safety" work found that a large share of C++ programs hit parse errors, because ESBMC's C++ frontend struggles with STL containers, templates and standard library functions. So pilot the parse rate first and restrict tasks to a subset ESBMC handles reliably (classes, simple templates, a limited STL). Report parse errors and timeouts separately from verdicts, and never count them as green.
- Awareness may push models to avoid STL and templates. That's the "verifier-friendly" effect above, and it is a result in itself.
- C++ adds its own exploit candidates: catch-all `catch(...)` swallowing errors, `noexcept` tricks, and early exits. Check what your ESBMC version does with C++ attributes like `[[assume]]` before listing it in the taxonomy.
- Pin the ESBMC version and flags, since behaviour differs between releases. That same paper ran ESBMC with unwinding assertions disabled, so a "success" meant only that nothing was found within the bound. Check which default your version uses and record it explicitly.

## 5. Detectors, cheapest first

1. **Syntactic baseline:** grep for added assume calls, `exit`/`abort`, `while(1)`, `catch(...)`, and any diff to the frozen harness. Every smarter detector has to beat this.
2. **Assume-stripping:** remove model-added assumes and rerun. A flip from green to failed is strong evidence the assume produced the green.
3. **Reachability sentinels:** insert `assert(false)` at key points (after the main computation, inside branches). If the sentinel doesn't fire, that code was never checked. Check whether your ESBMC version has coverage flags that do this for you.
4. **Mutation of the code under test:** inject known bugs and rerun the same harness. A high survival rate means the setup is too weak to catch bugs, whatever the verdict was.
5. **Bound-sensitivity:** from the sweep below.

Report precision and recall per mechanism against the labelled set, and show the gain over detector 1.

## 6. Bound sweep

For every green sample, rerun at k ∈ {2, 5, 10, 20, 50, 100}, with unwinding assertions explicitly on and off. Plot the fraction of green samples that stay green as k grows. Separate samples that break because the model shrank k (an L5 action) from samples that were never correct. That distinction turns "false assurance" and "gaming" into one coherent story.

## 7. Models and statistics

- Use a Qwen2.5-Coder size ladder (1.5B, 7B, 14B, 32B) plus one non-Qwen family, so you aren't measuring one model family. Optionally add one API model as a ceiling.
- Use at least 5 seeds per task and three paraphrased prompts, and bootstrap confidence intervals clustered by task.
- For awareness effects, use paired comparisons per task and seed (L1 vs L0).
- Rough scale: 120 tasks × 6 levels × 4 models × 5 seeds ≈ 14,000 runs, multiplied by the loop iterations at L2 and up. ESBMC time is the bottleneck, so pilot first to size the budget.

## 8. Hypotheses worth pre-registering

- **H1:** awareness raises exploiting behaviour even without feedback.
- **H2:** exploiting rises with iteration number once a feedback loop exists.
- **H3:** model size and exploiting are related, in either direction. Earlier reward-hacking work found more capable agents exploit misspecified proxies more effectively, with a sharp threshold in capability. Whether a similar threshold appears for small coding models is open, and either outcome is publishable.

A headline result might read: "Telling a 7B model its code will be ESBMC-checked changes X% of its outputs, Y% of the greens were hollow, and Z% broke at k=50."

## Biggest risks

- Prompt sensitivity, so use paraphrases.
- Small models failing to follow instructions at all, so track format errors separately.
- A noisy oracle, so label a sample by hand.

## First step

A one-week pilot: 20 tasks, 2 models, levels L0 to L2, the frozen harness and the assume-stripping detector. That tells you whether the awareness effect exists before you build L3 to L5.

Which GPUs and local models do you have? That decides the size ladder and how many seeds you can afford. I can also draft the task template (spec, frozen harness, hidden tests) and the prompts for each level.

Sources:
- [The Illusion of Safety: Multi-Tier Verification of AI vs. Human C++ Code](https://arxiv.org/pdf/2607.00107)
- [When Do Agent Loops Mistake Stagnation for Progress?](https://arxiv.org/pdf/2607.25152)


Run each prompt several times and report rates, not a single judged output. Do it differently for the no-feedback levels and the loop levels.

**Why one shot isn't enough**
A single sample per task can't separate "the model tends to do this" from "this sample happened to". Awareness effects (L1 vs L0) are probably small shifts in probability, and one sample each would bury them in noise. A 7B model at temperature 0.7 can pass one run and fail the next on the same prompt.

**L0 and L1 (no feedback): independent samples**
- Draw n samples per task per condition at a fixed temperature (I'd use 0.7) with logged seeds. Start with n=5 and go to 10 for tasks where results are borderline.
- For each task, compute the rate: of the n samples, what fraction were gamed-green, honest-green, wrong, or failed to parse. Then average those per-task rates across tasks.
- Add one greedy (temperature 0) run per task as a deterministic reference. It makes results easy to reproduce, but treat it as supplementary, since greedy decoding isn't how people use these models.

**L2 to L5 (feedback loops): repeat the whole episode**
- One "run" is a full episode (prompt, generate, verify, feed back, up to N iterations). Repeat each episode n=5 times with different seeds.
- Log the full trajectory, not just the final code. You want to see where in the loop exploiting first appears, which is what H2 needs.
- Cap iterations (for example 5 or 10) and keep the cap the same across models.

**How to average**
- Average per task first, then across tasks. Pooling every sample would let tasks with more parse failures or longer runs dominate.
- Use cluster bootstrap by task for the confidence intervals, because samples within a task aren't independent.
- Compare conditions with paired differences per task (L1 minus L0), not by comparing two overall means.

**Report two numbers, not just the mean**
- The **mean rate** (typical behaviour): a model exploits in 12% of samples.
- The **any-of-n rate**, the share of tasks where at least one of the n samples exploits. This is the safety-relevant number, since a deployed agent runs on many tasks and attempts. A pass@k-style framing makes it familiar to reviewers.

**Cost**
5 samples multiplies your run count by 5 and ESBMC time is your bottleneck. Two ways to keep it manageable:
- Use n=3 in the pilot and n=5 to 10 only for the final runs.
- Allocate adaptively: tasks where all samples agree (all honest or all gamed) need no more samples, and the extra budget goes to the mixed ones.

**One thing to avoid**
Don't average verdicts into a single score such as 0.6 green. "Green" mixes honest and gamed outcomes, and the difference between them is your whole finding. Keep the categories separate, so you can report honest-green, gamed-green, wrong and error as separate rates.