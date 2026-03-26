# Debugging Checklist for AI Models

Follow these steps one by one. Do not skip any.

## 1. Understand the Error
- [ ] What is the exact error message?
- [ ] Where in the code did it happen? (Check line numbers)
- [ ] What was the program trying to do?

## 2. Reproduce the Issue
- [ ] Can you make the error happen again?
- [ ] What are the exact steps or inputs?
- [ ] Write a small script that only shows this error.

## 3. Use the Debugger (Step-by-Step)
- [ ] Insert `import pdb; pdb.set_trace()` before the error.
- [ ] Run the code.
- [ ] Use `p <variable>` to see what's actually there.
- [ ] Use `n` to see which line breaks the logic.
- [ ] Is it a type error? (e.g., is it a String when it should be a Number?)
- [ ] Is it empty or `None`?

## 4. Look for Simple Mistakes
- [ ] Any typos in variable names?
- [ ] Is the indentation correct?
- [ ] Are all brackets closed? `()` `[]` `{}`

## 5. Test Your Fix
- [ ] Change only ONE thing at a time.
- [ ] Run the code again.
- [ ] Did the error go away?
- [ ] Did a NEW error appear?
