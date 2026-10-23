# Unit Testing Execution Report

## Authentication

| Test Case ID | Test Scenario | Expected Result | Status |
| --- | --- | --- | --- |
| TC-01 | Login with valid username and password | Login succeeds and a token is returned | Pass |
| TC-02 | Login with an invalid username | Login is denied | Pass
| TC-03 | Login with an invalid password | Login is denied | Pass|
| TC-04 | Open a protected page without logging in | Access is denied | Pass|

## Room Booking

| Test Case ID | Test Scenario | Expected Result | Status |
| --- | --- | --- | --- |
| TC-05 | Book an available room for a valid time | Booking is created | Pass |
| TC-06 | Book a room that does not exist | Booking is denied | Pass |
| TC-07 | Choose an end time before the start time | Booking is denied | Pass |
| TC-08 | Book a time that overlaps an existing booking | Booking is denied | Pass |
| TC-09 | Cancel another user's booking | Cancellation is denied | Pass |
| TC-12 | End a booking at midnight using `24:00` | Booking is accepted | Pass |
| TC-13 | Use `24:00` as a booking start time | Booking is denied | Pass |

## Password Verification (Same Standard User)

| Test Case ID | Test Scenario | Expected Result | Status |
| --- | --- | --- | --- |
| TC-10 | Verify the standard user's entered password against its saved hash | Password is accepted | Pass |
| TC-11 | Try an incorrect password against the same saved hash | Password is rejected | Pass |

## Notes
.
- TC-10 and TC-11 test two login attempts for the same user. They do not add
another user or store multiple passwords.
- Booking cases check the booking rules. The valid login case was checked
  through the running API.
