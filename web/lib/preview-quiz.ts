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
