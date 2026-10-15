| # | Info Item | T1 | T2 | T3 | T4 | T5 | Dimension |
|---|---|---|---|---|---|---|---|
| 1 | Project purpose | Present | Present | Present | Present | Present | D2 |
| 2 | Project lead | Missing | Missing | Missing | Missing | Missing | D1 |
| 3 | Current robot cost | Present | Present | Present | Present | Present | D2 |
| 4 | Target cost | Present | Present | Present | Present | Present | D2 |
| 5 | Technology stack | Partial | Partial | Partial | Present | Partial | D1 / D2 |
| 6a | Robotics meeting day | Missing | Missing | Partial | Partial | Missing | D1 |
| 6b | Robotics meeting time | Missing | Missing | Missing | Missing | Missing | D1 |
| 7 | Distribution/manufacturing plan | Present | Present | Present | Present | Present | D2 |

## Note

"Robotics group meeting day and time" appears as a single field in the prompt, but this rubric splits it into two independent Info_Items for scoring. Models may answer the day without the time (or vice versa). Splitting them allows the rubric to distinguish between "answered the day but missed the time" and "answered neither".