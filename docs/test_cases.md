# Test Cases

18 test cases. All are automated. The function name is in `tests/`.

| ID | Technique | Test | Input | Expected | Automated in |
|----|-----------|------|-------|----------|--------------|
| TC01 | Equivalence (valid) | Register valid user | `alice_1` / `Passw0rd123` | 201 | `test_auth_api.py::test_tc01_register_valid_user` |
| TC02 | Boundary | Username min length | 3 chars | 201 | `test_boundaries` |
| TC03 | Boundary | Username below min | 2 chars | 422 | `test_boundaries` |
| TC04 | Boundary | Username max length | 20 chars | 201 | `test_boundaries` |
| TC05 | Boundary | Username above max | 21 chars | 422 | `test_boundaries` |
| TC06 | Boundary | Password below min | 7 chars | 422 | `test_boundaries` |
| TC07 | Boundary | Password at min | 8 chars | 201 | `test_boundaries` |
| TC08 | Equivalence (invalid) | Bad characters in username | `bob!@#` | 422 | `test_tc08_bad_characters_in_username` |
| TC09 | Decision table | Duplicate username | register same name twice | 409 | `test_tc09_duplicate_username` |
| TC10 | Decision table | Valid user, correct password | login | 200 + token | `test_tc10_login_success` |
| TC11 | Decision table | Valid user, wrong password | login | 401 | `test_tc11_wrong_password` |
| TC12 | Decision table | Unknown user | login | 401 | `test_tc12_unknown_user` |
| TC13 | State transition | 5 wrong logins, then correct password | login | 423 | `test_tc13_account_locks_after_five_failures` |
| TC14 | State transition | Fail 3 times, succeed, fail once more | login | 200 then 401, no lock | `test_tc14_failed_counter_resets_on_success` |
| TC15 | Error guessing | `/me` without token | none | 401 | `test_tc15_me_without_token` |
| TC16 | Error guessing | `/me` with fake token | `Bearer abc` | 401 | `test_tc16_me_with_fake_token` |
| TC17 | Security | Same error body for TC11 and TC12 | compare bodies | Identical | `test_security.py::test_tc17_...` |
| TC18 | Performance | `/health` response time | GET | < 500 ms | `test_security.py::test_tc18_...` |

## Extra automated checks

| Check | Risk | Function |
|-------|------|----------|
| Password is hashed, not stored as plain text | R1 | `test_r1_password_is_hashed` |
| Same password gives different hashes (salt) | R1 | `test_salt_gives_different_hashes` |
| Valid token works on `/me` | R5 | `test_me_with_valid_token` |
