# Reflection: What Automation Missed

## What the automation did well

I wrote 18 test cases and automated all of them with pytest. The pipeline runs on every push and pull request. It gave me two clear results. The first run on `main` was green. It ran 21 tests in 17 seconds. Then I changed `MAX_FAILS` from 5 to 6 on a separate branch. The pull request turned red. TC13 failed because the login returned 200 instead of 423. This proved the pipeline catches a real change in behaviour. It also showed me that a small edit can break a security rule without anyone noticing by eye.

Automation is also fast and repeatable. The boundary tests for username and password length run in milliseconds. I do not want to type those inputs by hand each time. Coverage reached 100% of the app file. The state reset in `conftest.py` also made every test independent.

## What the automation missed

A green report does not mean the system is safe. My tests only check what I thought to check.

**Timing leak.** TC17 checks that a wrong password and an unknown user give the same 401 message. It passes. But my own report shows the unknown user test took 2 ms. The wrong password test took 38 ms. The code skips the password hash when the user does not exist. An attacker could measure this time and learn which usernames exist. The message is the same, but the behaviour is not. My test did not look at time, so it missed this.

**Registration leak.** The `/register` route returns 409 for a duplicate name. Anyone can use this to check if a username exists. I listed this as risk R3, but I only tested that the status code is 409. I did not ask if the 409 is a problem.

**Lockout as an attack.** The lockout works as designed, and TC13 and TC14 pass. But an attacker can now lock any account by sending five bad passwords. The test cannot say that the design itself is risky. It also never resets by time, so a locked user stays locked.

**Weak performance test.** TC18 sends one request to `/health` through the test client. It does not use a real network or many users. It says "under 500 ms", but it tells me almost nothing about load. It would still pass if the login route became very slow under load.

**Things I never tested.** Tokens never expire. Data is lost when the server restarts. The `failed` counter grows with every random username, so memory can fill up. No test checks any of these.

## Where human judgment was necessary

Choosing the risks was a human task. I had to decide that brute force matters more than slow responses. Scoring likelihood and impact needed thinking about how attackers behave. A tool cannot do that for me.

I also had to decide what the correct answer is. The test for lockout expects 423. But is 423 the right code? Some teams use 429. A test only checks that the code matches my choice. It cannot tell me if the choice is good.

Reading the results needed judgment too. The timing difference was visible in the report, but no test failed because of it. I only noticed it by reading the numbers and asking why they differ. Automation gave me the data. A person had to see the pattern.

Finally, a human has to decide what to do with a finding. Should I add a fake hash for unknown users? Should I add a rate limit by IP? Should lockout expire after 15 minutes? These are design and business choices, not test results.

## What I would do next

I would add a test that compares the response time for known and unknown users. I would add a real load test with a tool such as Locust. I would add token expiry and a time-based lockout, then write tests for them. I would also keep a short manual exploratory session in every release. Automation protects what I already know. People find what I do not know yet.
