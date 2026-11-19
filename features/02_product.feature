Feature: Product page - add to cart, care guide and reviews

  @TC-13 @smoke
  Scenario: Add a product to the cart
    Given I open the product "kw-302"
    When I add 1 of it to the cart
    Then I should see a toast containing "Added to cart"
    And the cart badge should show 1

  @TC-14 @BUG-05
  Scenario: Quantity above stock is not allowed
    Given I open the product "kw-101"
    When I add 50 of it to the cart
    Then the cart should not hold more than the stock of "Cast Iron Kadai, 24cm"

  @TC-15 @BUG-06
  Scenario Outline: Zero or negative quantity is not added
    Given I open the product "kw-101"
    When I add <qty> of it to the cart
    Then the cart should be empty

    Examples:
      | qty |
      | -2  |
      | 0   |

  @TC-17 @BUG-26
  Scenario: Care guide modal can be closed with the Close button inside it and with Escape
    Given I open the product "kw-101"
    When I open the care and sizing guide
    Then the Close button should be inside the modal
    When I press Escape
    Then the modal should be closed

  @TC-18
  Scenario: Post a review
    Given I open the product "kw-202"
    When I post the review "Latch still tight after a year"
    Then I should see a toast containing "Review posted"
    And the review "Latch still tight after a year" should be listed

  @TC-20 @BUG-20 @security
  Scenario: HTML in a review is shown as plain text
    Given I open the product "kw-202"
    When I post the review "<b>bold-check</b>"
    Then the review "<b>bold-check</b>" should be listed as plain text
