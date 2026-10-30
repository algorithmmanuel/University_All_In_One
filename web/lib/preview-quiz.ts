/** Local preview questions: no personal data or scores are sent to the server. */
export const previewQuestions = [
  {
    q: "You receive a scholarship message asking you to enter your school portal password on an unfamiliar site. What should you do?",
    answers: [
      "Enter the password quickly",
      "Verify the offer through the school’s official channel",
      "Forward it to friends",
    ],
    correct: 1,
    explanation:
      "Never submit credentials through an unverified link. Check the institution’s official website or contact its office.",
  },
  {
    q: "Which option is the strongest way to protect a school account?",
    answers: [
      "Reuse one password everywhere",
      "Use a unique password and multifactor authentication",
      "Share your password with a classmate",
    ],
    correct: 1,
    explanation:
      "Unique passwords and MFA significantly reduce account takeover risk.",
  },
  {
    q: "A group chat asks you to post a photo of your identity document so everyone can confirm your name. What is the best next step?",
    answers: [
      "Post it publicly to finish quickly",
      "Check whether verification is needed and use an appropriate private, verified route",
      "Share another person’s document instead",
    ],
    correct: 1,
    explanation:
      "Verify the purpose and recipient, minimise the information shared and avoid exposing identity documents in an open group.",
  },
  {
    q: "An unexpected pop-up says you must disable protection to install an urgent update. What should you do?",
    answers: [
      "Disable protection and accept the download",
      "Ask friends to try the file first",
      "Close the pop-up and check updates through the device or publisher’s trusted route",
    ],
    correct: 2,
    explanation:
      "An urgent message does not establish that software is trustworthy. Use the normal verified update route.",
  },
  {
    q: "A backup job reports success. What provides stronger evidence that work can resume after an outage?",
    answers: [
      "A tested restoration that validates the required service and its dependencies",
      "A reassuring archive filename",
      "The number of backup jobs alone",
    ],
    correct: 0,
    explanation:
      "A successful copy is useful evidence, while tested usable restoration addresses a different recovery question.",
  },
  {
    q: "A colleague requests a change to payment details through a familiar account. What should settle the request?",
    answers: [
      "The familiar display name alone",
      "An independently verified change following the established approval process",
      "How urgent the message sounds",
    ],
    correct: 1,
    explanation:
      "A genuine account may be misused. Consequential changes need established independent verification and approval.",
  },
] as const;


/** Distinct authored introductions. Local practice only, never placement or a saved grade. */
export const pathwayPreviews = {
  "secondary": [
    {
      "q": "A friend sends a shortened link offering free game credits and asks for your account password. What should you do?",
      "answers": [
        "Enter the password before the offer ends",
        "Check the offer through the game’s official app or website",
        "Send the link to classmates"
      ],
      "correct": 1,
      "explanation": "An attractive offer and a familiar sender do not verify a destination. Use an independently trusted route and keep passwords private."
    },
    {
      "q": "Your social profile shows your school, daily route and live location. What is a useful first change?",
      "answers": [
        "Restrict unnecessary sharing and review who can see each detail",
        "Add your home address too",
        "Assume followers cannot copy anything"
      ],
      "correct": 0,
      "explanation": "Limit information to its purpose and intended audience. Privacy settings help reduce exposure but cannot prevent every copy."
    },
    {
      "q": "A new device update is available in the normal settings menu. What should guide installation?",
      "answers": [
        "Ignore every update permanently",
        "Disable all protection first",
        "Use the trusted update route and prepare for interruption or compatibility needs"
      ],
      "correct": 2,
      "explanation": "Trusted updates address known issues. Preserve important work and use the device or publisher’s supported process."
    },
    {
      "q": "Someone watching you use a shared computer asks you to save your password in its browser. What is safer?",
      "answers": [
        "Save it so the next person can help",
        "Avoid saving it and sign out when finished",
        "Leave the signed-in tab open"
      ],
      "correct": 1,
      "explanation": "Shared devices should not retain your login. Sign out and check that your session ended; closing a tab alone may leave access active."
    },
    {
      "q": "Your phone shows an unexpected sign-in approval. Which action is appropriate?",
      "answers": [
        "Deny it and review your account through official controls",
        "Approve it to stop the notifications",
        "Read the approval code to a caller"
      ],
      "correct": 0,
      "explanation": "Do not approve a sign-in you did not initiate or share codes. Investigate through the account’s official support and security controls."
    },
    {
      "q": "Your only copy of a school project is on one laptop. What would reduce the risk of losing it?",
      "answers": [
        "Rename the file backup",
        "Keep a second shortcut to the same file",
        "Maintain a separate protected copy and check that you can restore it"
      ],
      "correct": 2,
      "explanation": "A shortcut is not another copy. A protected separate copy plus a restoration check provides stronger recovery evidence."
    }
  ],
  "university": [
    {
      "q": "An application accepts a record identifier from its browser. Where must permission to read that record be checked?",
      "answers": [
        "Only in the hidden browser button",
        "On the server for the authenticated user and requested object",
        "Nowhere if identifiers are hard to guess"
      ],
      "correct": 1,
      "explanation": "Client controls can be bypassed. Enforce object-level authorisation on the server rather than relying on hidden controls or identifier secrecy."
    },
    {
      "q": "A broad network allow rule takes precedence over a later narrow deny. What should a technical review verify?",
      "answers": [
        "The effective permitted path and rule evaluation order",
        "Only that a deny appears somewhere",
        "Whether the diagram uses the right colours"
      ],
      "correct": 0,
      "explanation": "Rules must be evaluated as the system applies them. A written deny does not establish that the intended traffic is actually blocked."
    },
    {
      "q": "A cloud object is encrypted at rest but its policy allows public reads. What follows?",
      "answers": [
        "Encryption guarantees that no reader receives data",
        "The policy is irrelevant",
        "The service may return readable content to unauthorised readers"
      ],
      "correct": 2,
      "explanation": "At-rest encryption does not replace access control. Review effective identity and resource permissions and validate the resulting access."
    },
    {
      "q": "Two logs show events one hour apart, but the systems use different clock settings. What should you do before correlating them?",
      "answers": [
        "Declare the events unrelated",
        "Preserve originals and account for clock offsets and time zones",
        "Rewrite the original timestamps without a record"
      ],
      "correct": 1,
      "explanation": "Document time interpretation and transformations while retaining originals. A time difference alone neither proves nor disproves a connection."
    },
    {
      "q": "A state-changing request may have committed before its response was lost. How should a supported retry identify itself?",
      "answers": [
        "Reuse the original command identifier and payload",
        "Invent a fresh identifier on every retry",
        "Submit the desired final score"
      ],
      "correct": 0,
      "explanation": "Stable command identities let the server recognise the same operation. The server still validates ownership, state and any conflicting reuse."
    },
    {
      "q": "An isolated server stops communicating with the network. What does that establish by itself?",
      "answers": [
        "All malware has been removed",
        "Every dependent service remains available",
        "Connectivity has been restricted, while cleanliness and service impact still need checks"
      ],
      "correct": 2,
      "explanation": "Isolation changes communication and can disrupt dependencies. It is not proof of eradication or usable recovery."
    }
  ],
  "professional": [
    {
      "q": "A risk treatment is scheduled six weeks away while exposure remains. What should management require now?",
      "answers": [
        "A note saying the future date removes the risk",
        "An owned treatment plan, justified interim controls and monitoring",
        "Transfer all accountability to the auditor"
      ],
      "correct": 1,
      "explanation": "A future treatment date is not an interim control. Assign accountable ownership and assess exposure during the waiting period."
    },
    {
      "q": "A supplier provides a security assurance report. What determines how much reliance it supports?",
      "answers": [
        "Its scope, period, exceptions and relevance to the service being used",
        "The number of pages alone",
        "The supplier’s logo"
      ],
      "correct": 0,
      "explanation": "Assurance is bounded by what was examined and when. Match the report to relevant services, controls, dependencies and remaining gaps."
    },
    {
      "q": "Management assigns an owner and due date to a control finding. When is verified closure justified?",
      "answers": [
        "As soon as the owner accepts the task",
        "When the plan is written",
        "When suitable evidence and retesting demonstrate effective correction"
      ],
      "correct": 2,
      "explanation": "Ownership and milestones support follow-up. They do not demonstrate that the underlying control gap has been corrected."
    },
    {
      "q": "Operations wants a critical service reopened before containment checks finish. What is a defensible decision process?",
      "answers": [
        "Reopen solely because revenue matters",
        "Evaluate recovery gates, alternatives and documented approval of residual exposure",
        "Avoid recording the decision"
      ],
      "correct": 1,
      "explanation": "Business urgency matters alongside evidence and alternatives. Record accountable approval and remaining uncertainty rather than substitute urgency for validation."
    },
    {
      "q": "A recovery test restores one database, but the application cannot authenticate. What can leadership reasonably conclude?",
      "answers": [
        "The component restore worked, but usable service recovery remains unproven",
        "The full service met its recovery objective",
        "Identity is outside every recovery test"
      ],
      "correct": 0,
      "explanation": "Recovery claims must match the tested scope. Applications, identities, keys and other dependencies can prevent a restored component from delivering a service."
    },
    {
      "q": "An AI lending pilot has different error rates across customer groups with unequal sample sizes. What should governance require?",
      "answers": [
        "Suppress the group results",
        "Treat overall accuracy as final proof of fairness",
        "Investigate representativeness, uncertainty and customer impact with accountable follow-up"
      ],
      "correct": 2,
      "explanation": "A measurable gap warrants review. Sample limits affect interpretation; overall accuracy and nominal human review do not settle subgroup impact."
    }
  ]
} as const;

export function previewFor(pathway: string) {
  return pathway === "secondary" || pathway === "university" || pathway === "professional"
    ? pathwayPreviews[pathway] : previewQuestions;
}
