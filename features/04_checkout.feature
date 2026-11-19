Feature: Checkout - placing orders and form validation

  Background:
    Given my cart has these items
      | id     | qty |
      | kw-201 | 1   |
    And I am on the checkout page

  @TC-31 @TC-42 @smoke
  Scenario: Place an order with valid details
    When I fill the checkout form with valid details
    And I click "Place order"
    Then I should see the order confirmation with a reference
    And the order should be listed on the Orders page

  @TC-33
  Scenario: Email without domain part is rejected
    When I fill the checkout form with valid details
    And I change "email" to "abc@"
    And I click "Place order"
    Then I should see the field error "Enter a valid email address."
    And the order should not be placed

  Scenario Outline: Invalid field values are rejected
    When I fill the checkout form with valid details
    And I change "<field>" to "<value>"
    And I click "Place order"
    Then the order should not be placed

    @TC-32 @BUG-12
    Examples: Blank or spaces-only required fields
      | field    | value  |
      | fullName | SPACES |
      | address  | SPACES |
      | city     | SPACES |

    @TC-34 @BUG-12
    Examples: Weak email
      | field | value |
      | email | a@b   |

    @TC-35 @BUG-12
    Examples: Letters in mobile number
      | field | value    |
      | phone | phoneABC |

    @TC-36 @BUG-12
    Examples: Wrong PIN code
      | field   | value |
      | pincode | 12ab  |
      | pincode | 123   |

  @TC-37 @BUG-13
  Scenario: Pressing Enter submits the form
    When I fill the checkout form with valid details
    And I press Enter in the "pincode" field
    Then I should see the order confirmation with a reference

  @TC-38 @BUG-14
  Scenario: Double clicking Place order creates only one order
    When I fill the checkout form with valid details
    And I double click "Place order"
    Then exactly 1 order should be saved

  @TC-39 @BUG-15
  Scenario: No success message when validation fails
    When I fill the checkout form with valid details
    And I change "email" to "abc@"
    And I click "Place order"
    Then I should not see a toast containing "Order placed"

  @TC-58 @BUG-25
  Scenario: No spelling mistakes in checkout and confirmation
    Then the page should not contain the word "adress"
    When I fill the checkout form with valid details
    And I click "Place order"
    Then the page should not contain the word "sucessfully"
