/** Local preview questions: no personal data or scores are sent to the server. */
export const previewQuestions = [
  {
    q: 'You receive a scholarship message asking you to enter your school portal password on an unfamiliar site. What should you do?',
    answers: ['Enter the password quickly', 'Verify the offer through the school’s official channel', 'Forward it to friends'],
    correct: 1,
    explanation: 'Never submit credentials through an unverified link. Check the institution’s official website or contact its office.',
  },
  {
    q: 'Which option is the strongest way to protect a school account?',
    answers: ['Reuse one password everywhere', 'Use a unique password and multifactor authentication', 'Share your password with a classmate'],
    correct: 1,
    explanation: 'Unique passwords and MFA significantly reduce account takeover risk.',
  },
] as const;
