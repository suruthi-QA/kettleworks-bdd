Feature: Cart - totals, quantity, remove and promo codes

  Background:
    Given my cart has these items
      | id     | qty |
      | kw-201 | 2   |
      | kw-302 | 3   |
    And I am on the cart page

  @TC-22 @BUG-01
  Scenario: Line total is price multiplied by quantity
    Then the line total for "Loaf Tin, 900g" should be 1480

  @TC-23 @BUG-01
  Scenario: Subtotal is the sum of all lines
    Then the subtotal should be 2920

  @TC-24 @BUG-07
  Scenario: Changing quantity updates totals and the cart badge
    When I change the quantity of "Wooden Spatula Set of 3" to 1
    Then the subtotal should be 1960
    And the cart badge should show 3

  @TC-25 @BUG-04
  Scenario: Remove deletes the chosen item only
    When I remove "Wooden Spatula Set of 3" from the cart
    Then the cart should not contain "Wooden Spatula Set of 3"
    And the cart should contain "Loaf Tin, 900g"

  @TC-26 @BUG-02
  Scenario: SAVE10 gives 10 percent off the subtotal
    When I apply the promo code "SAVE10"
    Then the discount should be 10 percent of the subtotal

  @TC-27
  Scenario: An invalid promo code shows an error
    When I apply the promo code "FAKECODE"
    Then I should see a toast containing "That code is not valid on this order."

  @TC-30 @BUG-24
  Scenario: Cart prices use the rupee symbol
    Then the cart page should not show the "$" symbol
