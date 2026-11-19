Feature: Sign in, sign out and protected pages

  @TC-44
  Scenario: Sign in with empty fields shows an error
    Given I am on the sign in page
    When I click "Sign in"
    Then I should see the text "Enter both an email address and a password."

  @TC-45 @smoke
  Scenario: Customer can sign in
    When I sign in as the customer
    Then the header should show "Sign out"
    And the account page should show the customer email

  @TC-46 @BUG-18
  Scenario Outline: Guest is sent to sign in for protected pages
    Given I am not signed in
    When I open "<page>"
    Then I should be on the sign in page

    Examples:
      | page      |
      | /checkout |
      | /orders   |

  @TC-47 @LBUG-01 @security
  Scenario: Signing out removes access to the account page
    Given I sign in as the customer
    When I sign out
    And I open "/account"
    Then I should not see the customer email
