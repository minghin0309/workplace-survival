# Fresh Benchmark v3.1 Holdout Plan

- Methodology: benchmark v3 scorer plus v3.1 question-case construction contract.
- Runtime: `main@9d48b048d083507c20f2714b21053d36b68d6366`.
- Cases: 18.
- Turns: 24.
- Required-question candidates: 6 across six distinct concepts.
- Historical v1/v2/v3 case content is prohibited.

Pre-SUT gates:

- construction contract and all candidate mutations pass;
- required question concepts ≥3 across ≥3 adjudicated gold cases;
- required revision concepts ≥3 across ≥3 cases;
- accepted turns ≥1;
- gold uncertainty ≤20%.

If any gate fails, SUT, extraction, matching, and scoring stop. If all gates pass, every case executes in a distinct cloud context and the v3 scorer runs exactly once after output/evaluation freeze.

Thresholds remain those preregistered by Methodology v3.
