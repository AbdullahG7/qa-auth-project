# Risk Analysis and Quality Criteria

**System under test:** Auth API (FastAPI) with `/register`, `/login`, `/me` and `/health`.
**Framework:** pytest with FastAPI `TestClient`.

## Scope

The feature is user registration and login. It handles passwords and tokens, so security risks matter most.

## Risk table

Likelihood (L) and Impact (I) are scored 1 to 3. Risk score = L x I.

| # | Risk | L | I | Score | Mitigation / test |
|---|------|---|---|-------|-------------------|
| R1 | Passwords stored in plain text | 1 | 3 | 3 | Check the stored value is not the password |
| R2 | Brute-force login attempts | 3 | 3 | 9 | Account lockout after 5 failures |
| R3 | Duplicate usernames | 2 | 2 | 4 | Expect 409 |
| R4 | Weak or invalid input accepted | 3 | 2 | 6 | Boundary tests on length and characters |
| R5 | Protected route open without a token | 2 | 3 | 6 | Test `/me` with no token and a fake token |
| R6 | Error messages leak whether a user exists | 2 | 2 | 4 | Same 401 for wrong user and wrong password |
| R7 | Slow response under load | 2 | 2 | 4 | Response-time check |

## Priority

R2 has the highest score (9), so lockout has the most tests (TC13, TC14). R4 and R5 come next (6).

## Functional quality criteria

- A valid user can register once.
- A valid user can log in and gets a token.
- A token gives access to `/me`.
- Invalid input is rejected with a clear status code.
- The account locks after 5 failed logins.

## Non-functional quality criteria

- **Security:** passwords are hashed and salted. Login errors do not show which field was wrong.
- **Performance:** `/health` responds in under 500 ms.
- **Reliability:** the same request gives the same status code.
- **Maintainability:** all tests run with one command: `pytest`.

## Known limits of this prototype

- Data is stored in memory and is lost on restart.
- Tokens never expire.
- The lockout never resets by time.
- There is no rate limit by IP address.

These are out of scope, but they are good points for the reflection.
