# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Wise Pugliese
- Step 0.12, results of the three runs without a session (optional): skipped
- Step 0.16, blocks of "how many of the three tools are excluded":
  - 0 tools excluded (`[]`)
  - 1 tool excluded (`["Knife"]`, `["Scissors"]`)
  - 2 tools excluded (`["Knife", "Scissors"]`)
  - 3 tools excluded (all of them), the block that gives 500

## Defect report
- Title: Excluding all three tools makes POST /api/pizza answer 500 with an empty body
- Request: `curl -i -H "@auth.txt" -d "@all_tools.json" https://quickpizza.grafana.com/api/pizza` with body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: status 400 and a JSON error message, because no pizza can satisfy the request
- Actual result: status 500 and an empty body
- Severity: Medium. The client cannot tell what went wrong, but it needs an unusual input and nothing is lost.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: read 404, change 400, delete 400. The owner's rating stayed unchanged after each attempt.

## Part B
1. Two failures a real server shows and a unit test with stubs cannot: the load balancer sending a request to a server that does not know the user (flaky 401), and the real server's rules and messages differing from what the code assumes (e.g. a Go JSON error for 3.5 stars, or a 500 under a rare input). A unit test with stubs is still worth writing because it runs in milliseconds, needs no network, is deterministic, and points at the exact function that broke.
2. Ratings of the public token belong to everyone, so another student could change or delete them while my test runs and make it fail for no reason. A new user per test gives data nobody else touches, and the test needs nothing from other tests. In Project 2 I will create my own cart, order or booking with a unique name in each test, delete it afterwards, and never touch data of other groups.
3. QuickPizza runs on several servers behind a load balancer, and each server keeps its own users. The session keeps the AWSALB cookie, so all requests of the run reach the same server that created the user. Step 0.12 was not done.
4. The block with all three tools excluded revealed the defect. A 500 with an empty body gives the calling app no reason and no way to react: it looks like a server crash, so the app may retry or show a generic error, while a 400 with a message says the request itself is wrong and what to fix. The test stays as xfail so the defect stays documented and visible, the suite stays green, and with strict=True the run fails when QuickPizza fixes it, which tells me to remove the mark.
5. Base choice: 1 base test + 2 (C1) + 3 (C2) + 1 (C3) + 2 (C4) = 9 tests, since each characteristic adds (blocks - 1) tests: (3-1)+(4-1)+(2-1)+(3-1) = 8, plus 1 base = 9. All combinations: 3 x 4 x 2 x 3 = 72 tests.
6. Read 404, change 400, delete 400. I would expect 403 Forbidden (or 404 for all three so the rating's existence is not revealed). The rating is protected in every case, so this is not a security defect, but it is an inconsistency: change and delete answer 400 "rating ID not found", which is a wrong code for a missing or not-owned resource, while read answers 404. It is a minor defect in API consistency.
7. The request answers 200 with a list of ratings that belong to other users (ids 1, 2, 3, ...). Yes, this is a defect: a made-up token was never issued by the server, so it should get 401. On a real system a stranger could read data of other users without logging in, and a token that is not checked could also be used to create or change data.
8. An API test checks better: the status codes, error messages and fields of every response, including refused requests, quickly and without the browser. Only a test through the web pages can check what the user sees: layout, text, buttons, and whether the page shows the error message correctly.
