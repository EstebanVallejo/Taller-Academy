# Day 1 Lab — Diagnose and Rebuild a Prompt

## Exercise 1 — The Assumption Audit

### Prompt v1

```text
Write an email declining a job interview because I decided to move forward with another opportunity.
```

### Response

```text
Hi [Name],

Thank you very much for the opportunity and for your time throughout the interview process.

I wanted to let you know that I’ve decided to move forward with another opportunity, so I’ll be withdrawing from the interview process.

I really appreciate your consideration and the chance to learn more about the role and the team. I hope we can stay in touch and potentially connect again in the future.

Best regards,
[Your Name]
```

### Assumption Audit

| Assumption | What the model guessed | Acceptable? |
| --- | --- | --- |
| **Tone** | I did not specify a tone. The model chose a professional, polite, and appreciative tone. | **Yes.** This fits the situation well. |
| **Length** | I did not specify a target length. The model produced one medium-length paragraph plus a greeting and closing. | **Yes.** It is concise enough for this type of email. |
| **Format** | I did not specify the email structure. The model added a greeting, body, and closing. | **Partially.** The email body is usable, but I would still need to create a subject line manually. |
| **Recipient identity** | I did not provide the recruiter’s name. The model did not invent one and used “[Recruiter’s Name]” instead. | **Yes.** A placeholder is better than guessing personal information. |
| **Sender identity** | I did not provide my name. The model used “[Your Name]” rather than inventing or inferring one. | **Yes.** The prompt did not contain enough information to fill this field. |
| **Future relationship** | I did not say whether I wanted to maintain contact with the company. The model assumed I did and added “I hope we can stay in touch and potentially connect again in the future.” | **Yes.** This is appropriate, but it was still a decision left to the model. |
| **Details about the other opportunity** | I did not specify how much to reveal. The model only said I was moving forward with “another opportunity” and gave no additional details. | **Yes.** This avoids unnecessary disclosure. |
| **Reason for declining** | I said I decided to move forward with another opportunity, but did not specify how directly this should be communicated. The model explicitly said that I was withdrawing from the interview process. | **Yes.** This makes the purpose of the email clear. |

## Exercise 2 — The Four-Block Rewrite

### Prompt v2

```text
Instruction:
Write a short email declining a scheduled job interview because I have decided to move forward with another opportunity.

Context:
The email is addressed to a recruiter. Use a professional, polite, and appreciative tone. Clearly communicate that I am withdrawing from the interview process while leaving the door open for future opportunities. Do not provide details about the other opportunity.

Input:
"""
My name: Esteban
Recruiter name: Sarah
I have a job interview scheduled with the company, but I have decided to move forward with another opportunity and will no longer continue with their hiring process.
"""

Output format:
Return a complete email in English with:

A subject line
A greeting using the recruiter's name
One short body paragraph of 3–5 sentences
A professional closing
Keep the complete email under 100 words
```

### Response

```text
Interview Withdrawal

Dear Sarah,

Thank you very much for the opportunity to interview and for your time throughout the process. I’ve decided to move forward with another opportunity and will therefore be withdrawing from the interview process. I truly appreciate your consideration and hope we can stay in touch for potential opportunities in the future.

Best regards,
Esteban
```

### Comparison of v1 and v2

#### Which single block made the biggest difference? How do you know?

**The Context block made the biggest difference.** In v1, I left the tone, audience, future relationship, and amount of detail up to the model. The first response happened to make good choices, but the Context block in v2 made those choices explicit and repeatable.

#### Which assumptions from Exercise 1 are now resolved, and which are still open?

The main assumptions from Exercise 1 are now resolved. Context covers the tone, audience, future relationship, and level of disclosure. Input supplies both names and the situation, Instruction states the purpose, and Output format controls the structure and length.

A few small choices are still open. I did not give an exact subject line or closing, so the model was free to choose “Interview Withdrawal” and “Best regards.”

### Ablation — v2 Without the Output Format Block

#### Prompt

```text
Instruction:
Write a short email declining a scheduled job interview because I have decided to move forward with another opportunity.

Context:
The email is addressed to a recruiter. Use a professional, polite, and appreciative tone. Clearly communicate that I am withdrawing from the interview process while leaving the door open for future opportunities. Do not provide details about the other opportunity.

Input:
"""
My name: Esteban
Recruiter name: Sarah
I have a job interview scheduled with the company, but I have decided to move forward with another opportunity and will no longer continue with their hiring process.
"""
```

#### Response

```text
Interview Process

Dear Sarah,

Thank you for the opportunity to interview with your company. I appreciate your time and consideration throughout the process.

I wanted to let you know that I’ve decided to move forward with another opportunity, so I’ll need to withdraw from the interview process.

Thank you again, and I hope we have the chance to connect about future opportunities.

Best regards,
Esteban
```

#### Manual Cleanup Required

This version needs almost no cleanup. It already has a subject, greeting, short body, and closing. To match v2 exactly, I would combine the body into one paragraph and probably change the generic subject “Interview Process” to something clearer, such as “Interview Withdrawal.” For a familiar task like an email, the model could infer most of the format on its own, although the Output format block still gave me more control.

## Exercise 3 — Token Budget and Variability

### Part A — Estimate Before You Send

#### Source

The original text was the [Executive Summary of the NIST Artificial Intelligence Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/0-ai-rmf-1-0/).

#### Original Text Estimate

```text
Source:            .\day-01\Articulo.txt
Characters:        8,021
Words:             1,198
Estimated tokens:  2,005  (~4 chars/token)
```

Using the rule of thumb of approximately four characters per token:

```text
8,021 ÷ 4 = 2,005.25 ≈ 2,005 estimated tokens
```

#### Specific Question

```text
What are the four core functions of the NIST AI Risk Management Framework, and how are they applied?
```

Only one paragraph from the original text was needed to answer this question.

#### Trimmed Text Estimate

```text
Source:            .\day-01\Articulo-recortado.txt
Characters:        488
Words:             76
Estimated tokens:  122  (~4 chars/token)
```

Using the same rule of thumb:

```text
488 ÷ 4 = 122 estimated tokens
```

#### Trimmed Prompt

```text
Answer the following question using only the provided text.

Question:
What are the four core functions of the NIST AI Risk Management Framework, and how are they applied?

Context:
"""
Part 2 comprises the “Core” of the Framework. It describes four specific functions to help organizations address the risks of AI systems in practice. These functions – govern, map, measure, and manage – are broken down further into categories and subcategories. While govern applies to all stages of organizations’ AI risk management processes and procedures, the map, measure, and manage functions can be applied in AI system-specific contexts and at specific stages of the AI lifecycle.
"""

Answer in one concise paragraph.
```

#### Token Reduction

```text
((2,005 - 122) ÷ 2,005) × 100 = 93.9%
```

The trimmed context went from **2,005 estimated tokens to 122**, a reduction of about **93.9%**. I removed roughly **1,883 tokens** while keeping the paragraph that directly answers the question.

### Part B — Observe Variability

#### Open-Ended Creative Prompt

The following prompt was run three times without modification:

```text
Suggest a genre for the new book I will write.
```

##### Run 1

I’d suggest **psychological mystery**—especially one built around an unreliable narrator.

It gives you room for:

- **A strong hook:** someone discovers something that contradicts their own memories.
- **Character depth:** the real mystery is partly inside the protagonist’s mind.
- **Twists:** secrets can be revealed gradually without relying on complicated world-building.
- **Emotional stakes:** the ending can change how readers interpret everything that came before.

A particularly fun premise: **a person receives messages from themselves dated one year in the future, warning them not to trust the person they love most.**

If you tell me what kinds of books you enjoy, I can suggest **3–5 genres tailored to your taste**.

##### Run 2

I’d suggest **psychological speculative fiction**—a story grounded in recognizable human emotions but built around one unsettling “what if?”

For example:

> **What if you could erase any memory you wanted—but every erased memory was transferred to someone else?**

It gives you room for mystery, relationships, moral dilemmas, and twists without locking you into hard science fiction.

A few other genres worth considering:

- **Cozy mystery** — clever, character-driven, low on gore.
- **Dark academia** — secrets, obsession, old institutions, intellectual rivalry.
- **Literary horror** — fear built through atmosphere and psychology rather than monsters.
- **Romantic fantasy** — emotional stakes combined with an imaginative world.
- **Near-future dystopia** — especially good for exploring AI, identity, or social control.

If you tell me **2–3 books you love**, I can suggest a genre—and a premise—that fits your taste.

##### Run 3

I’d suggest **psychological mystery**.

It gives you room for:

- A protagonist with a secret—even from themselves.
- An unreliable narrator readers can’t fully trust.
- A mystery that unfolds through memories, clues, and contradictions.
- Emotional stakes alongside the external plot.
- A twist that can completely reframe earlier chapters.

A strong hook could be: **The protagonist receives a letter from someone who supposedly died ten years ago—and the letter contains a secret only they could know.**

If you tell me what kinds of books, movies, or stories you like, I can suggest a genre that fits your taste more precisely.

#### Tightly Specified Prompt

The following prompt was run three times without modification:

```text
Return only the ISO 8601 date for the first day of April 2000. No other text.
```

##### Run 1

```text
2000-04-01
```

##### Run 2

```text
2000-04-01
```

##### Run 3

```text
2000-04-01
```

#### Consistency Analysis

The tightly specified prompt was more consistent: all three runs returned `2000-04-01`. The book prompt produced different genres, premises, alternatives, and response lengths. This was not just luck—the date prompt had one factual answer, required a specific format, and prohibited extra text, while the book prompt left almost every creative choice open.

## Reflection

### Which of your real tasks need consistency between runs, and which benefit from variety?

When I ask for code with fixed requirements or data in a specific format, I need consistent output because I want to use it with little editing. For brainstorming, architecture alternatives, or story ideas, variety is more useful because I want to compare options I may not have considered.

### What is the one habit from today you will apply to the next prompt you write, before you write it?

Before writing my next prompt, I will list the important decisions I might otherwise leave to the model. Then I will specify the ones that affect the result and leave the rest open only when variation would actually help.

## Stretch Goal — Audit and Rewrite a Public Prompt

### Source

I adapted this exercise from an engineering prompt published by [OpenAI Academy](https://academy.openai.com/en/public/clubs/work-users-ynjqu/resources/prompting): “Summarize recent code review feedback for the onboarding module, based on notes from the last sprint review, and provide a list of actionable items for the team.”

### Original Prompt

```text
Summarize recent code review feedback for the onboarding module, based on the notes from the last sprint review, and provide a list of actionable items for the team.

Notes:
"""
The registration endpoint accepts an email address without validating its format. Sarah mentioned that error messages currently expose internal field names. The team agreed that password validation should happen on both the client and server. Diego suggested adding unit tests for duplicate email registration and expired verification links. The welcome email is sent synchronously, which may slow down the request. Nobody was assigned to investigate moving email delivery to a background job. The current pull request also contains several unrelated formatting changes.
"""
```

### Response

#### Summary of recent code review feedback

The onboarding module has several correctness, security, reliability, and maintainability concerns:

- **Registration validation:** The registration endpoint does not validate email format.
- **Error handling:** Error messages expose internal field names and should be made user-facing without leaking implementation details.
- **Password validation:** Validation should be enforced on **both client and server**, with the server treated as authoritative.
- **Test coverage:** Add unit tests covering duplicate email registration and expired verification links.
- **Email delivery:** Welcome emails are sent synchronously, potentially increasing request latency. The team agreed this should be investigated for background/asynchronous delivery, but **no owner was assigned**.
- **PR scope:** The current PR includes unrelated formatting changes, which should be separated or removed to keep the review focused.

#### Actionable items

1. **Add server-side email format validation** to the registration endpoint.
2. **Review and sanitize error messages** so they don't expose internal field names.
3. **Implement password validation on both client and server**, ensuring server-side validation cannot be bypassed.
4. **Add unit tests** for:

   - Duplicate email registration.
   - Expired verification links.

5. **Investigate moving welcome-email delivery to a background job** and assign an owner.
6. **Remove or separate unrelated formatting changes** from the current onboarding PR.
7. **Before merging, rerun the onboarding test suite** and confirm the new validation and error-handling behavior is covered.

### Assumption Audit

| Assumption | What the model guessed | Acceptable? |
| --- | --- | --- |
| **Audience** | The prompt referred only to “the team.” The model assumed a technical engineering audience and used terms such as “server-side validation,” “request latency,” and “test suite.” | **Yes.** The terminology is appropriate for a software development team, but the intended audience was not explicitly defined. |
| **Length and detail** | No target length was provided. The model produced a medium-length summary followed by seven actionable items. | **Yes.** It is readable, although I might want a shorter version for sprint follow-up. |
| **Structure** | The prompt requested a summary and actionable items but did not define their exact structure. The model created two sections, used categorized bullets for the summary, and numbered the actions. | **Yes.** This makes the response easy to scan. |
| **Issue categories** | The notes did not classify the feedback. The model introduced “correctness, security, reliability, and maintainability.” | **Mostly.** The categories make sense, but they came from the model rather than the notes. |
| **Priority** | The prompt did not explain how to prioritize the feedback. The model kept roughly the same order as the notes and did not assign priorities. | **Partially.** The actions are there, but I still cannot tell which ones are most urgent. |
| **Decision status** | The notes distinguish an agreement, a suggestion, observations, and an unassigned investigation. The model turned most of them into equivalent action items. | **Partially.** The list is useful, but it hides which items were agreed and which were only suggestions or open questions. |
| **Owners** | The prompt did not request owners. The model retained that the background-job investigation had no owner but did not associate Sarah or Diego with other items. | **Yes.** It avoided incorrectly treating the people who raised issues as the people responsible for fixing them. |
| **Server authority** | The notes required password validation on the client and server. The model added that the server should be authoritative and impossible to bypass. | **Reasonable but unsupported.** I agree with it as an engineering practice, but it was not in the notes. |
| **Additional action** | The model added a requirement to rerun the onboarding test suite before merging. | **No.** It may be useful, but it goes beyond summarizing the notes. |
| **Deadlines** | No deadlines were provided, and the model did not invent any. | **Yes.** Missing scheduling information should remain unspecified rather than being guessed. |

### Four-Block Rewrite

```text
Instruction:
Summarize the sprint-review notes about the onboarding module and extract only the follow-up actions explicitly supported by the notes. Preserve whether each item is an observation, team agreement, suggestion, or open investigation.

Context:
The audience is the software engineering team preparing its next sprint. The purpose is to create an accurate follow-up record, not to perform a new code review. Use concise, professional language. Do not add engineering recommendations, priorities, deadlines, decisions, or owners that are not present in the notes. Do not assume that the person who raised an issue owns the action. If an owner or priority is missing, write “Unassigned” or “Not specified.”

Input:
"""
The registration endpoint accepts an email address without validating its format. Sarah mentioned that error messages currently expose internal field names. The team agreed that password validation should happen on both the client and server. Diego suggested adding unit tests for duplicate email registration and expired verification links. The welcome email is sent synchronously, which may slow down the request. Nobody was assigned to investigate moving email delivery to a background job. The current pull request also contains several unrelated formatting changes.
"""

Output format:
Return two sections:

1. Summary
   - Write no more than three sentences describing the main themes.

2. Follow-up items
   - Return a Markdown table with these columns:
     Item | Type | Action or finding | Owner | Priority
   - Type must be one of: Observation, Agreement, Suggestion, or Open investigation.
   - Use one row per distinct item.
   - Use “Unassigned” for a missing owner and “Not specified” for a missing priority.
```

### Four-Block Rewrite Response

#### 1. Summary

The notes identify validation and error-message concerns in the registration flow, along with agreed password validation coverage. They also capture suggested test coverage, a possible asynchronous email-delivery investigation, and unrelated formatting changes in the current pull request.

#### 2. Follow-up items

| Item | Type | Action or finding | Owner | Priority |
| --- | --- | --- | --- | --- |
| Registration email format | Observation | The registration endpoint accepts email addresses without format validation. | Unassigned | Not specified |
| Internal field names in errors | Observation | Current error messages expose internal field names. | Unassigned | Not specified |
| Password validation | Agreement | Password validation should occur on both the client and server. | Unassigned | Not specified |
| Duplicate/expired-link tests | Suggestion | Add unit tests for duplicate email registration and expired verification links. | Unassigned | Not specified |
| Background email delivery | Open investigation | Investigate moving welcome-email delivery to a background job; no one was assigned. | Unassigned | Not specified |
| Pull request formatting changes | Observation | The current pull request contains several unrelated formatting changes. | Unassigned | Not specified |

### Comparison

The rewrite stayed closer to the original notes. It kept observations, agreements, suggestions, and the open investigation separate instead of presenting everything as a confirmed task. It also marked missing owners and priorities clearly and did not add the two extra recommendations from the first response.
