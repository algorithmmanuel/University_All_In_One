"""Reviewed beginner curriculum. Examples are displayed as text, never executed.

Stable objective IDs link lesson teaching, low-stakes checks and assessment items.
Publishing is explicit; ordinary startup and legacy seeds never activate a release.
"""
REVISION = 'python-foundations-v1'
COURSE_TITLE = 'Introduction to Python'
ACADEMY_ID = 'university'
MARKER = 'educyber.lesson:' + REVISION + ':'

LESSONS = [
    {
        'key': 'values', 'title': 'Variables and data types',
        'legacy_content': "Python variables can reference strings, integers, floats and booleans. Example: student_name = 'Ada'.",
        'objectives': [
            {'id': 'PY-V1', 'text': 'Trace assignment and reassignment in order.'},
            {'id': 'PY-V2', 'text': 'Distinguish text, whole numbers, decimal numbers and Boolean values.'},
            {'id': 'PY-V3', 'text': 'Predict arithmetic, text operations and printed output.'},
        ],
        'sections': [
            {'title': 'A name refers to a value', 'body': "A variable is a name you use to refer to a value. Read statements from top to bottom. The = symbol assigns the value on its right to the name on its left. It does not ask whether two things are equal. print() displays a value. Quotes mark text; the quotes themselves are not printed.",
             'code': 'student_name = "Ada"\nprint(student_name)', 'output': 'Ada'},
            {'title': 'Choose the right type', 'body': 'str stores text such as "Ada" or "12". int stores whole numbers such as 12. float stores decimal numbers such as 12.5. bool stores True or False, with capital first letters. type(value) reports its type; type(12) gives int and type("12") gives str. A number inside quotes is text, not a quantity you can add to an integer.'},
            {'title': 'Worked example: a study budget', 'body': 'Start with 1000 naira and spend 250. The second assignment reads the current balance, subtracts the cost, and replaces the old balance. Values change only when a statement changes them.',
             'code': 'balance = 1000\ncost = 250\nbalance = balance - cost\nprint(balance)', 'output': '750'},
            {'title': 'Numbers, text and input', 'body': 'For numbers, + adds and * multiplies. For text, + joins strings: "Ada" + "!" gives "Ada!". int("12") converts digit text to a whole number, so int("12") + 3 gives 15. input() returns text even when someone types digits; convert valid digit text before arithmetic. Do not assume every input can be converted. We use supplied examples here; this page does not run Python.',
             'code': 'items = 3\nprice = 200\nprint(items * price)\nprint("Ada" + "!")', 'output': '600\nAda!'},
        ],
        'exercises': [
            {'id': 'trace-balance', 'objective': 'PY-V1', 'prompt': 'Predict the final printed value before checking.',
             'code': 'points = 4\npoints = points + 3\nprint(points)', 'options': ['4', '7', '3'], 'answer': 1,
             'feedback': ['4 is the starting value. The next assignment adds 3 before print runs.', 'Correct. Read top to bottom: 4 + 3 replaces points with 7.', '3 is the amount added, not the final total. Trace both assignments.']},
            {'id': 'text-number', 'objective': 'PY-V2', 'prompt': 'Which replacement makes this print 15?',
             'code': 'age_text = "12"\nprint(_____ + 3)', 'options': ['age_text', 'int(age_text)', '"age_text"'], 'answer': 1,
             'feedback': ['age_text still refers to text. Convert the digit text before adding a number.', 'Correct. int(age_text) converts "12" to 12, then 12 + 3 gives 15.', 'Quotes create literal text. They do not read the variable or convert it.']},
        ],
    },
    {
        'key': 'conditions', 'title': 'Conditional logic',
        'legacy_content': 'Use if, elif and else to branch based on conditions. Indentation determines code blocks.',
        'objectives': [
            {'id': 'PY-C1', 'text': 'Evaluate comparisons and tell assignment from equality.'},
            {'id': 'PY-C2', 'text': 'Trace if, elif and else in order, including threshold boundaries.'},
            {'id': 'PY-C3', 'text': 'Explain indentation and combine Boolean conditions.'},
        ],
        'sections': [
            {'title': 'Ask a question with a comparison', 'body': 'A comparison produces True or False. == asks whether values are equal; != asks whether they differ. > and < compare sizes; >= and <= include the boundary value. score = 50 assigns a value. score == 50 tests it. if runs its indented block only when its condition is true.'},
            {'title': 'Worked example: decide a result', 'body': 'Check if first, then each elif in order. In this single chain, only the first true branch runs; else is the fallback if none is true. The colon starts a block and consistent indentation groups its statements. Here 65 is below 70 but at least 50.',
             'code': 'score = 65\nif score >= 70:\n    print("Excellent")\nelif score >= 50:\n    print("Pass")\nelse:\n    print("Practise again")', 'output': 'Pass'},
            {'title': 'Test the boundary, not just the middle', 'body': 'With score >= 50, exactly 50 passes and 49 does not. If you used > 50 instead, exactly 50 would not pass. Trace one example on each side of a threshold. Two separate if statements are different from an if/elif chain: both independent conditions can run when both are true.'},
            {'title': 'Combine conditions and follow indentation', 'body': 'and requires both conditions to be true. or requires at least one to be true. not reverses a Boolean. The final print below is outside the if block, so it runs whether or not entry is allowed. This is a teaching example, not a real authorization system.',
             'code': 'has_ticket = True\nis_open = False\nif has_ticket and is_open:\n    print("Enter")\nelse:\n    print("Wait")\nprint("Check finished")', 'output': 'Wait\nCheck finished'},
        ],
        'exercises': [
            {'id': 'boundary', 'objective': 'PY-C2', 'prompt': 'What prints when the value equals the threshold?',
             'code': 'score = 50\nif score >= 50:\n    print("Pass")\nelse:\n    print("Try again")', 'options': ['Pass', 'Try again', 'Both messages'], 'answer': 0,
             'feedback': ['Correct. >= includes equality, so the first branch runs.', '>= includes 50. Compare it with >, which would exclude 50.', 'An if/else pair chooses one branch; it does not run both.']},
            {'id': 'two-rules', 'objective': 'PY-C3', 'prompt': 'Predict the output when both requirements must hold.',
             'code': 'ready = True\nconnected = False\nif ready and connected:\n    print("Start")\nelse:\n    print("Wait")', 'options': ['Start', 'Wait', 'True'], 'answer': 1,
             'feedback': ['and needs both values to be True; connected is False.', 'Correct. True and False is False, so the fallback prints Wait.', 'The condition selects a branch. The print call contains the text Wait, not the condition value.']},
        ],
    },
    {
        'key': 'loops', 'title': 'Loops',
        'legacy_content': 'Use for to iterate through sequences and while to repeat while a condition is true.',
        'objectives': [
            {'id': 'PY-L1', 'text': 'Trace a for loop over a list and range.'},
            {'id': 'PY-L2', 'text': 'Trace a changing while-loop condition and identify termination.'},
            {'id': 'PY-L3', 'text': 'Predict loop totals and distinguish break from continue.'},
        ],
        'sections': [
            {'title': 'Repeat once for each item', 'body': 'A list uses square brackets and keeps items in order. for assigns each item to the loop name in turn and runs the indented block. len(list) counts its items. range(3) supplies 0, 1, 2: it stops before 3. range(1, 4) supplies 1, 2, 3.',
             'code': 'names = ["Ada", "Emeka"]\nfor name in names:\n    print(name)\nprint(len(names))', 'output': 'Ada\nEmeka\n2'},
            {'title': 'Worked example: accumulate a total', 'body': 'Start the total before the loop. Each assignment adds the current item to the previous total. The values after each iteration are 2, then 5, then 9. The final print is outside the loop, so it displays one final total.',
             'code': 'total = 0\nfor value in [2, 3, 4]:\n    total = total + value\nprint(total)', 'output': '9'},
            {'title': 'Repeat while a condition holds', 'body': 'while checks its condition before each iteration. Update a value that can make the condition false; otherwise a loop can continue indefinitely. Below, attempts takes values 0 then 1 inside the loop. At 2, the condition is false and the loop stops. Never run untrusted code to explore a loop.',
             'code': 'attempts = 0\nwhile attempts < 2:\n    print(attempts)\n    attempts = attempts + 1\nprint("Done")', 'output': '0\n1\nDone'},
            {'title': 'Stop or skip one iteration', 'body': 'break leaves the nearest loop immediately. continue skips the rest of the current iteration, then moves to the next iteration. They do not mean the same thing. Trace the tested value before deciding which print calls run.',
             'code': 'for number in [1, 2, 3]:\n    if number == 2:\n        continue\n    print(number)', 'output': '1\n3'},
        ],
        'exercises': [
            {'id': 'range-total', 'objective': 'PY-L1', 'prompt': 'Which values are printed, in order?',
             'code': 'for number in range(1, 4):\n    print(number)', 'options': ['1, 2, 3, 4', '1, 2, 3', '0, 1, 2, 3'], 'answer': 1,
             'feedback': ['The stop value 4 is excluded by range.', 'Correct. Start at 1 and stop before 4.', 'This range explicitly starts at 1, not 0.']},
            {'id': 'while-stop', 'objective': 'PY-L2', 'prompt': 'What change makes the loop move towards stopping?',
             'code': 'count = 0\nwhile count < 3:\n    print(count)\n    _____', 'options': ['count = count + 1', 'count = 0', 'count == 3'], 'answer': 0,
             'feedback': ['Correct. The counter becomes 1, 2, then 3; count < 3 is then False.', 'Resetting to 0 keeps the condition true.', '== compares values; it does not change count.']},
        ],
    },
]

# Each item assesses one named objective explicitly taught above. Prompt variation
# tests application, not a second copy of the same definition question.
QUESTIONS = [
    ('PY-V1', 'What prints after x = 4; x = x + 2; print(x)?', ['4', '6', '2'], 1, 'Read in order: x starts at 4, then becomes 6. print displays the current value.'),
    ('PY-V1', 'Which statement assigns 8 to the variable points?', ['points == 8', 'points = 8', '8 = points'], 1, '= assigns a value to a name on its left. == compares; a number cannot be the assignment target.'),
    ('PY-V2', 'Which value is text rather than a whole number?', ['12', '"12"', 'True'], 1, 'Quotes make "12" a str. Unquoted 12 is an int; True is a bool.'),
    ('PY-V2', 'Which type represents True and False?', ['str', 'float', 'bool'], 2, 'bool represents Boolean truth values. str holds text and float holds decimal numbers.'),
    ('PY-V2', 'Which conversion makes the digit text "7" usable as a whole number?', ['str("7")', 'int("7")', 'print("7")'], 1, 'int converts valid digit text to an integer. str keeps text; print displays a value.'),
    ('PY-V3', 'A notebook costs 150 naira. What does print(3 * 150) display?', ['450', '153', '3150'], 0, '* multiplies numbers: 3 times 150 is 450. Joining digit text is a different operation.'),
    ('PY-V3', 'What does print("Ada" + "!") display?', ['Ada + !', 'Ada!', 'An integer'], 1, '+ joins two strings here. Quotes and the + operator are not part of the displayed text.'),
    ('PY-C1', 'Which comparison is True when score is exactly 50?', ['score > 50', 'score < 50', 'score >= 50'], 2, '>= includes equality. Both strict comparisons are false at exactly 50.'),
    ('PY-C1', 'Which expression checks equality without changing a value?', ['age = 18', 'age == 18', 'age + 18'], 1, '== compares. = assigns, and + performs addition.'),
    ('PY-C2', 'A chain checks score >= 70, then elif score >= 50. Which branch runs for 65?', ['The first branch', 'The elif branch', 'Both branches'], 1, '65 fails the first comparison and meets the second. One if/elif chain runs only its first true branch.'),
    ('PY-C2', 'When does else run in an if/elif/else chain?', ['Every time', 'When no earlier condition is true', 'Only when all earlier conditions are true'], 1, 'else is the fallback after every earlier condition in that chain is false.'),
    ('PY-C2', 'Two independent if statements both have true conditions. How many blocks can run?', ['Two', 'Only one', 'None'], 0, 'Independent if statements are each evaluated. Unlike an if/elif chain, both can run.'),
    ('PY-C3', 'ready is True and connected is False. What is ready and connected?', ['True', 'False', 'The text connected'], 1, 'and requires both Boolean values to be true. One false operand makes this result False.'),
    ('PY-C3', 'A print call is unindented after an if/else block. When does it run?', ['Only when if is true', 'After either chosen branch completes normally', 'Never'], 1, 'Indentation groups statements. An unindented statement after the block runs after either normal branch.'),
    ('PY-L1', 'Which values does range(3) provide?', ['1, 2, 3', '0, 1, 2', '0, 1, 2, 3'], 1, 'With one argument, range starts at 0 and excludes its stop value 3.'),
    ('PY-L1', 'names = ["Ada", "Emeka"]. What does len(names) return?', ['2', '1', 'The text names'], 0, 'len counts the two items. It does not return an item or the variable name.'),
    ('PY-L2', 'A while loop starts count at 0 and adds 1 while count < 2. Which values are printed before each update?', ['0, 1', '0, 1, 2', '1, 2'], 0, 'The condition is checked before each iteration. At 2 it is false, so only 0 and 1 are printed.'),
    ('PY-L2', 'Why can while count < 3 fail to stop when count starts at 0?', ['The counter never changes', 'The counter increases each iteration', 'The condition becomes false'], 0, 'Without a change, 0 stays below 3. Updating the counter can make the condition false.'),
    ('PY-L3', 'A loop adds each value in [2, 3, 4] to total starting at 0. What is the final total?', ['4', '9', '3'], 1, 'The successive totals are 2, 5 and 9. The last item and item count are different from the sum.'),
    ('PY-L3', 'Which statement skips the rest of one iteration without leaving the loop?', ['break', 'continue', 'else'], 1, 'continue moves to the next iteration. break leaves the nearest loop; else is not a skip instruction.'),
]
